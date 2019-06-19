context("cdf_coverage")

test_that("True density has uniform CDF coverage", {
  set.seed(12345)
  n_grid <- 10001
  n_test <- 501
  z_grid <- seq(-5, 5, length.out = n_grid)
  z_test <- rnorm(n_test)
  cdes <- matrix(dnorm(z_grid), nrow = n_test, ncol = n_grid, byrow = TRUE)
  pvals <- cdf_coverage(cdes, z_grid, z_test)

  suppressWarnings(test <- ks.test(pvals, "punif")) # ties due to discretization
  expect_gt(test$p.value, 0.05)
})
