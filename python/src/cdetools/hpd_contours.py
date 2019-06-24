import numpy as np


def _hpd_countour_level(prob_val, density, z_delta, n_grid,
                        max_iters=200, tol=1e-3):
    """
    Calculate contour levels for HPD sets, for a single level

    @param density: A vector of density evaluations.
    @param z_grid: The grid on which the density is evaluated. Should be
        regularly spaced.
    @param prob_val: The probability level for the HPD sets
    @param z_delta: shrinking factor for the density;
    @param n_grid: number of points in the grid for evaluating the density
    @param max_iters: Optional; number of iterations of binary search
    @param tol: Optional; tolerance of binary search
    """

    if max_iters <= 0:
        raise ValueError("Maximum Iterations needs to be positive."
                         "Currently %s" % (max_iters))
    lower = np.min(density)
    upper = np.max(density)

    for _ in range(max_iters):
        mid = (upper + lower) / 2
        area = np.sum(density[np.where(density >= mid)]) * z_delta / n_grid

        if np.abs(area - prob_val) < tol:
            return mid
        elif area < prob_val:
            upper = mid
        else:
            lower = mid

    return mid


def hpd_contour_levels(probs, density, z_grid, max_iters=200, tol=1e-3):
    """
    Calculate contour levels for HPD sets - wrapper for `_hpd_countour_level`

    @param density: A vector of density evaluations.
    @param z_grid: The grid on which the density is evaluated. Should be
        regularly spaced.
    @param probs: The probability levels for the HPD sets
    @param max_iters: Optional; number of iterations of binary search
    @param tol: Optional; tolerance of binary search
    """

    if max_iters <= 0:
        raise ValueError("Maximum Iterations needs to be positive."
                         "Currently %s" % (max_iters))

    z_min = np.min(z_grid, axis=0)
    z_max = np.max(z_grid, axis=0)
    z_delta = np.prod(z_max - z_min)
    n_grid = z_grid.shape[0]

    levels = np.apply_along_axis(func1d=_hpd_countour_level, axis=0,
                                 arr=probs, z_delta=z_delta, density=density,
                                 max_iters=max_iters, tol=tol, n_grid=n_grid)

    return levels