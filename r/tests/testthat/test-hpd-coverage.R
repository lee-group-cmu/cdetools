context("hpd_coverage")

test_that("True density has uniform HPD coverage", {
  set.seed(12345)
  n_grid <- 10001
  n_test <- 501
  z_grid <- seq(-5, 5, length.out = n_grid)
  z_test <- rnorm(n_test)
  cdes <- matrix(dnorm(z_grid), nrow = n_test, ncol = n_grid, byrow = TRUE)
  pvals <- hpd_coverage(cdes, z_grid, z_test)

  suppressWarnings(test <- ks.test(pvals, "punif")) # ties due to discretization
  expect_gt(test$p.value, 0.05)
})

test_that("True multivariate density hsa uniform HPD coverage", {
  set.seed(12345)
  n_grid <- 51
  n_test <- 701
  z_grid <- expand.grid(seq(0, 1, length.out = n_grid),
                        seq(0, 1, length.out = n_grid))
  z_test <- cbind(rbeta(n_test, 2, 3),
                  rbeta(n_test, 4, 1))

  cde <- dbeta(z_grid[, 1], 2, 3) * dbeta(z_grid[, 2], 4, 1)
  cdes <- matrix(cde, nrow = n_test, ncol = length(cde), byrow = TRUE)
  pvals <- hpd_coverage(cdes, z_grid, z_test)

  suppressWarnings(test <- ks.test(pvals, "punif")) # ties due to discretization
  expect_gt(test$p.value, 0.05)
})
