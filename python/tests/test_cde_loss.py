import numpy as np
import scipy.stats as stats
import pytest
from python.cde_loss import cde_loss


def test__correct_cde_for_unif_density():
    n_grid = 1000
    n_obs = 1423
    z_grid = np.linspace(0, 1, n_grid)
    z_test = np.random.uniform(0, 1, size=(n_obs,))
    cdes = np.ones((n_obs, n_grid))
    assert cde_loss(cdes, z_grid, z_test)[0] == pytest.approx(-1.0, abs=1e-3)


def test__correct_cde_for_normal_density():
    n_grid = 1000
    n_obs = 1423
    z_grid = np.linspace(-5, 5, n_grid)
    z_test = np.random.normal(size=(n_obs,))
    dist = stats.norm()
    cdes = np.array([dist.pdf(z_grid) for _ in range(n_obs)]).reshape(n_obs, n_grid)
    expected = -10 * np.mean(dist.pdf(z_grid) ** 2)
    assert cde_loss(cdes, z_grid, z_test)[0] == pytest.approx(expected, abs=1e-2)


def test__cde_loss_scale_by_mult_factor():
    n_grid = 1000
    n_obs = 1423
    scale = 2

    z_grid = np.linspace(-5, 5, n_grid)
    z_test = np.random.normal(size=(n_obs,))
    dist = stats.norm()
    cdes = np.array([dist.pdf(z_grid) for _ in range(n_obs)]).reshape(n_obs, n_grid)

    scaled_z_grid = np.linspace(-5, 5, n_grid) * scale
    scaled_z_test = z_test * scale
    scaled_dist = stats.norm(scale=scale ** 0.5)
    scaled_cdes = np.array([
        scaled_dist.pdf(scaled_z_grid) for _ in range(n_obs)]).reshape(n_obs, n_grid)

    cde_scaled = cde_loss(cdes, z_grid, z_test)[0]/scale
    cde = cde_loss(scaled_cdes, scaled_z_grid, scaled_z_test)[0]

    assert cde_scaled == pytest.approx(cde, abs=1e-1)