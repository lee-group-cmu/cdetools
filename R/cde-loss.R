#' Calculate conditional density estimation loss.
#'
#' Estimates the CDE loss
#' \deqn{\int \int (\hat{f}(z \mid x) - f(z \mid x))^{2} dz dP(x)}
#' which can be written as
#' \deqn{E[\int \hat{f}(z \mid X) dz] - 2 E[\hat{f}(Z \mid X)] + C_{f}}
#' where \eqn{C_{f}} is an (unknown) constant. These expectations are
#' estimated using empirical expectations.
#'
#' @param cdes a matrix of conditional density estimates with each row
#'   corresponding to an observation, and each column corresponding to
#'   a grid point
#' @param z_grid a matrix of the grid points at which the conditional
#'   densities are estimated
#' @param z_test a matrix of the true responses
#' @examples
#' z_grid <- seq(0, 1, length.out = 99)
#' z_test <- runif(101)
#' cde <- matrix(dbeta(z_grid, 2, 2), nrow = 101, ncol = 99, byrow=TRUE)
#' cde_loss(cde, z_grid, z_test)
#' @export
cde_loss <- function(cdes, z_grid, z_test) {
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

  integrals <- z_delta * rowSums(cdes ^ 2)

  nn_ids <- cbind(seq_len(nrow(z_test)), FNN::knnx.index(z_grid, z_test, k = 1))
  likeli <- cdes[nn_ids]

  losses <- integrals - 2 * likeli

  return(list(loss = mean(losses),
              se = stats::sd(losses) / sqrt(nrow(cdes))))
}
