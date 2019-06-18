import numpy as np


def _hpd_countour_level(prob_val, density, z_delta, n_grid, upper, lower,
                        max_iters=200, tol=1e-3):

    if max_iters <= 0:
        raise ValueError("Maximum Iterations needs to be positive."
                         "Currently %s" % (max_iters))

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

    if max_iters <= 0:
        raise ValueError("Maximum Iterations needs to be positive."
                         "Currently %s" % (max_iters))

    z_min = np.min(z_grid, axis=0)
    z_max = np.max(z_grid, axis=0)
    z_delta = np.prod(z_max - z_min)
    n_grid = z_grid.shape[0]
    lower = np.min(density)
    upper = np.max(density)

    levels = np.apply_along_axis(func1d=_hpd_countour_level, axis=0,
                                 arr=probs, z_delta=z_delta, density=density,
                                 max_iters=max_iters, tol=tol, n_grid=n_grid,
                                 upper=upper, lower=lower)

    return levels