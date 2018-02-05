#' Calculate coverage based upon HPD regions.
#'
#' @param cdes: A matrix of conditional density estimates; each row
#'   corresponds to an observation, each column corresponds to a grid
#'   point
#' @param z_grid: A matrix of grid points at which the CDE is
#'   estimated
#' @param z_test: The true responses associated with the observations
#' @return A vector of "p-values"; under the true generating model
#'   these are Uniform(0, 1)
#' @examples
#'   set.seed(12345)
#'   n_grid <- 10001
#'   n_test <- 73
#'   z_grid <- seq(-5, 5, length.out = n_grid)
#'   z_test <- rnorm(n_test)
#'   cdes <- matrix(dnorm(z_grid), nrow = n_test, ncol = n_grid, byrow = TRUE)
#'   pvals <- hpd_coverage(cdes, z_grid, z_test)
#'   ks.test(pvals, "punif")
#' @export
hpd_coverage <- function(cdes, z_grid, z_test) {
  if (!is.matrix(z_grid)) {
    z_grid <- as.matrix(z_grid)
  }

  if (!is.matrix(z_test)) {
    z_test <- as.matrix(z_test)
  }

  stopifnot(nrow(cdes) == nrow(z_test))
  stopifnot(ncol(cdes) == nrow(z_grid))
  stopifnot(ncol(z_grid) == ncol(z_test))

  z_min <- apply(z_grid, 2, min)
  z_max <- apply(z_grid, 2, max)
  z_delta <- prod(z_max - z_min) / nrow(z_grid)

  n_test <- nrow(cdes)
  pvals <- rep(NA, n_test)
  for (ii in seq_len(n_test)) {
    nn_id <- FNN::knnx.index(z_grid, z_test[ii, , drop = FALSE], k = 1)
    cutoff <- cdes[ii, nn_id]
    pvals[ii] <- z_delta * sum(cdes[ii, cdes[ii, ] > cutoff])
  }

  return(pvals)
}
