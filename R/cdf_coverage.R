#' Calculates coverage based upon the CDF
#'
#' @param cdes: A matrix of conditional density estimates; each row
#'   corresponds to an observation, each column corresponds to a grid
#'   point
#' @param z_grid: A vector/matrix of grid points at which the CDE is
#'   estimated
#' @param z_test: The true responses associated with the observations
#' @return A vector of "p-values"
#' @examples
#'   set.seed(12345)
#'   n_grid <- 10001
#'   n_test <- 73
#'   z_grid <- seq(-5, 5, length.out = n_grid)
#'   z_test <- rnorm(n_test)
#'   cdes <- matrix(dnorm(z_grid), nrow = n_test, ncol = n_grid, byrow = TRUE)
#'   pvals <- cdf_coverage(cdes, z_grid, z_test)
#'   ks.test(pvals, "punif")
#' @export
cdf_coverage <- function(cdes, z_grid, z_test) {
  stopifnot(nrow(cdes) == length(z_test))
  stopifnot(ncol(cdes) == length(z_grid))
  z_min <- min(z_grid)
  z_max <- max(z_grid)
  z_delta <- (z_max - z_min) / length(z_grid)

  n_test <- nrow(cdes)
  pvals <- rep(NA, n_test)
  for (ii in seq_len(n_test)) {
    pvals[ii] <- z_delta * sum(cdes[ii, z_grid > z_test[ii]])
  }

  return(pvals)
}
