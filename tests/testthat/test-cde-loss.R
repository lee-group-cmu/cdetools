context("cde_loss")

test_that("Uniform density has correct CDE loss", {
  set.seed(1)

  n_grid <- 1000
  n_obs <- 1423

  z_grid <- seq(0, 1, length.out = n_grid)
  z_test <- runif(n_obs)
  cdes <- matrix(1.0, n_obs, n_grid)

  expect_equal(cde_loss(cdes, z_grid, z_test)$loss, -1.0,
               tolerance = 1e-2)
})

test_that("Normal density has correct CDE loss", {
  set.seed(20)
  n_grid <- 1000
  n_obs <- 1423

  z_grid <- seq(-5, 5, length.out = n_grid)
  z_test <- rnorm(n_obs)
  cdes <- t(matrix(dnorm(z_grid), n_grid, n_obs))

  expect_equal(cde_loss(cdes, z_grid, z_test)$loss,
               -10 * mean(dnorm(z_grid) ^ 2),
               tolerance = 1e-2)
})

test_that("CDE loss scales by multiplicative factor", {
  set.seed(3)

  n_grid <- 1000
  n_obs <- 1423

  scale <- 2

  z_grid <- seq(-5, 5, length.out = n_grid)
  z_test <- rnorm(n_obs)
  cdes <- t(matrix(dnorm(z_grid), n_grid, n_obs))

  scaled_z_grid <- seq(-5, 5, length.out = n_grid) * scale
  scaled_z_test <- z_test * scale
  scaled_cdes <- t(matrix(dnorm(scaled_z_grid, sd = scale), n_grid, n_obs))

  expect_equal(cde_loss(cdes, z_grid, z_test)$loss / scale,
               cde_loss(scaled_cdes, scaled_z_grid, scaled_z_test)$loss,
               tolerance = 1e-2)
})
