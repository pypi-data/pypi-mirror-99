from numpy.typing import DTypeLike

from netket.hilbert import AbstractHilbert

from ._local_operator import LocalOperator as _LocalOperator


def destroy(
    hilbert: AbstractHilbert, site: int, dtype: DTypeLike = float
) -> _LocalOperator:
    """
    Builds the boson destruction operator :math:`\\hat{a}` acting on the `site`-th of the
     Hilbert space `hilbert`.

    If `hilbert` is a non-Bosonic space of local dimension M, it is considered
    as a bosonic space of local dimension M.

    Args:
        hilbert: The hilbert space
        site: the site on which this operator acts

    Returns:
        The resulting Local Operator
    """
    import numpy as np

    N = hilbert.size_at_index(site)

    D = np.array([np.sqrt(m) for m in np.arange(1, N)])
    mat = np.diag(D, 1)
    return _LocalOperator(hilbert, mat, [site], dtype=dtype)


def create(
    hilbert: AbstractHilbert, site: int, dtype: DTypeLike = float
) -> _LocalOperator:
    """
    Builds the boson creation operator :math:`\\hat{a}^\\dagger` acting on the `site`-th of the
     Hilbert space `hilbert`.

    If `hilbert` is a non-Bosonic space of local dimension M, it is considered
    as a bosonic space of local dimension M.

    Args:
        hilbert: The hilbert space
        site: the site on which this operator acts

    Returns:
        The resulting Local Operator
    """
    import numpy as np

    N = hilbert.size_at_index(site)

    D = np.array([np.sqrt(m) for m in np.arange(1, N)])
    mat = np.diag(D, -1)
    return _LocalOperator(hilbert, mat, [site], dtype=dtype)


def number(
    hilbert: AbstractHilbert, site: int, dtype: DTypeLike = float
) -> _LocalOperator:
    """
    Builds the number operator :math:`\\hat{a}^\\dagger\\hat{a}`  acting on the `site`-th of the
    Hilbert space `hilbert`.

    If `hilbert` is a non-Bosonic space of local dimension M, it is considered
    as a bosonic space of local dimension M.

    Args:
        hilbert: The hilbert space
        site: the site on which this operator acts

    Returns:
        The resulting Local Operator
    """
    import numpy as np

    N = hilbert.size_at_index(site)

    D = np.array([m for m in np.arange(0, N)])
    mat = np.diag(D, 0)
    return _LocalOperator(hilbert, mat, [site], dtype=dtype)


def proj(
    hilbert: AbstractHilbert, site: int, n: int, dtype: DTypeLike = float
) -> _LocalOperator:
    """
    Builds the projector operator :math:`|n\\rangle\\langle n |` acting on the `site`-th of the
    Hilbert space `hilbert` and collapsing on the state with `n` bosons.

    If `hilbert` is a non-Bosonic space of local dimension M, it is considered
    as a bosonic space of local dimension M.

    Args:
        hilbert: The hilbert space
        site: the site on which this operator acts
        n: the state on which to project

    Returns:
        the resulting operator
    """
    import numpy as np

    N = hilbert.size_at_index(site)

    if n >= N:
        raise ValueError("Cannot project on a state above the cutoff.")

    D = np.array([0 for m in np.arange(0, N)])
    D[n] = 1
    mat = np.diag(D, 0)
    return _LocalOperator(hilbert, mat, [site], dtype=dtype)


# clean up the module
del AbstractHilbert
