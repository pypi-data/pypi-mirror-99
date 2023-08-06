# Copyright 2021 The NetKet Authors - All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import dataclasses
import orjson

import os
from os import path as _path
import numpy as np
import jax

from flax import serialization

from jax.tree_util import tree_map

from .runtime_log import RuntimeLog


def _exists_json(prefix):
    return _path.exists(prefix + ".log") or _path.exists(prefix + ".mpack")


def default(obj):
    if hasattr(obj, "to_json"):
        return obj.to_json()
    elif hasattr(obj, "to_dict"):
        return obj.to_dict()
    elif isinstance(obj, np.ndarray):
        if np.issubdtype(obj.dtype, np.complexfloating):
            return {"real": obj.real, "imag": obj.imag}
        else:
            if obj.ndim == 0:
                return obj.item()
            elif obj.ndim == 1:
                return obj.tolist()
            else:
                raise TypeError

    elif hasattr(obj, "_device"):
        return np.array(obj)
    elif isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}

    raise TypeError


class JsonLog(RuntimeLog):
    """
    Json Logger, that can be passed with keyword argument `logger` to Monte
    Carlo drivers in order to serialize the outpit data of the simulation.

    If the model state is serialized, then it is serialized using the msgpack protocol of flax.
    For more information on how to de-serialize the output, see
    `here <https://flax.readthedocs.io/en/latest/flax.serialization.html>`_.
    The target of the serialization is the variational state itself.

    Data is serialized to json as several nested dictionaries. You can deserialize by simply calling
    :code:`json.load(open(filename))`.
    Logged expectation values will be captured inside histories objects, so they will have a
    subfield `iter` with the iterations at which that quantity has been computed, then `Mean` and
    others.
    Complex numbers are logged as dictionaries :code:`{'real':list, 'imag':list}`.
    """

    def __init__(
        self,
        output_prefix: str,
        mode: str = "write",
        save_params_every: int = 50,
        write_every: int = 50,
        save_params: bool = True,
    ):
        """
        Construct a Json Logger.

        Args:
            output_prefix: the name of the output files before the extension
            save_params_every: every how many iterations should machine parameters be flushed to file
            write_every: every how many iterations should data be flushed to file
            mode: Specify the behaviour in case the file already exists at this output_prefix. Options are
                - `[w]rite`: (default) overwrites file if it already exists;
                - `[a]ppend`: appends to the file if it exists, overwise creates a new file;
                - `[x]` or `fail`: fails if file already exists;
            save_params: bool flag indicating whever parameters should be serialized
        """
        super().__init__()

        # Shorthands for mode
        if mode == "w":
            mode = "write"
        elif mode == "a":
            mode = "append"
        elif mode == "x":
            mode = "fail"

        if not ((mode == "write") or (mode == "append") or (mode == "fail")):
            raise ValueError(
                "Mode not recognized: should be one of `[w]rite`, `[a]ppend` or `[x]`(fail)."
            )

        file_exists = _exists_json(output_prefix)

        starting_json_content = {"Output": []}

        if file_exists and mode == "append":
            # if there is only the .mpacck file but not the json one, raise an error
            if not _path.exists(output_prefix + ".log"):
                raise ValueError(
                    "History file does not exists, but wavefunction file does. Please change `output_prefix or set mode=`write`."
                )

            starting_json_content = json.load(open(output_prefix + ".log"))

        elif file_exists and mode == "fail":
            raise ValueError(
                "Output file already exists. Either delete it manually or change `output_prefix`."
            )

        dir_name = _path.dirname(output_prefix)
        if dir_name != "":
            os.makedirs(dir_name, exist_ok=True)

        self._prefix = output_prefix
        self._write_every = write_every
        self._save_params_every = save_params_every
        self._old_step = 0
        self._steps_notflushed_write = 0
        self._steps_notflushed_pars = 0
        self._save_params = save_params

    def __call__(self, step, item, variational_state):
        old_step = self._old_step
        super().__call__(step, item, variational_state)

        if (
            self._steps_notflushed_write % self._write_every == 0
            or step == old_step - 1
        ):
            self._flush_log()
        if (
            self._steps_notflushed_pars % self._save_params_every == 0
            or step == old_step - 1
        ):
            self._flush_params(variational_state)

        self._old_step = step
        self._steps_notflushed_write += 1
        self._steps_notflushed_pars += 1

    def _flush_log(self):
        with open(self._prefix + ".log", "wb") as outfile:

            outfile.write(orjson.dumps(self.data, default=default))
            self._steps_notflushed_write = 0

    def _flush_params(self, variational_state):
        if not self._save_params:
            return

        binary_data = serialization.to_bytes(variational_state.variables)
        with open(self._prefix + ".mpack", "wb") as outfile:
            outfile.write(binary_data)

        self._steps_notflushed_pars = 0

    def flush(self, variational_state):
        """
        Writes to file the content of this logger.

        Args:
            variational_state: optionally also writes the parameters of the machine.
        """
        self._flush_log()

        if variational_state is not None:
            self._flush_params(variational_state)
