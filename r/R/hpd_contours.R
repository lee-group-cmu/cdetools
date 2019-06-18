#' Calculate contour levels for HPD sets
#'
#' @param density A vector of density evaluations.
#' @param z_grid The grid on which the density is evaluated. Should be
#'   regularly spaced.
#' @param probs The probability levels for the HPD sets
#' @param max_iters Optional; number of iterations of binary search
#' @param tol Optional; tolerance of binary search
#'
#' @export
hpd_contour_levels <- function(density, z_grid, probs, max_iters = 200, tol = 1e-3) {
  z_min <- apply(z_grid, 2, min)
  z_max <- apply(z_grid, 2, max)

  z_delta <- prod(z_max - z_min)
  n_grid <- nrow(z_grid)

  levels <- sapply(probs, function(prob) {
    lower <- min(density)
    upper <- max(density)

    for (iter in seq_len(max_iters)) {
      mid <- (upper + lower) / 2
      area <- sum(density[density >= mid]) * z_delta / n_grid
      print(area)

      if (abs(area - prob) < tol) {
        return(mid)
      } else if(area < prob) {
        upper <- mid
      } else {
        lower <- mid
      }
    }
    return(mid)
  })

  return(levels)
}
