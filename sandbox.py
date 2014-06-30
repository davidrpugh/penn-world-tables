import numpy as np
from scipy import stats

import pwt

# load the Penn World Tables data
pwt_data = pwt.load_pwt_data()

def _predicted_labor_share(capital, g, n, s, delta, rho, omega):
    """Model predicted share of income going to labor."""
    if abs(rho) <= 1e-3:
        labor_share = omega
    else:
        labor_share = (1 - omega) / (omega * capital**rho + (1 - omega))

    return labor_share

def _residual(capital, ctry, g, n, s, delta, rho, omega):
    """Difference between actual and model predicted labor share."""
    actual_labor_share = pwt_data.major_xs(ctry)['labsh']
    predicted_labor_share = _predicted_labor_share(capital, g, n, s, delta, rho, omega)
    return actual_labor_share - predicted_labor_share

def individual_log_likelihood(capital, ctry, g, n, s, delta, rho, sigma, omega):
    """Individual model log likelihood."""
    # residual is assumed to be drawn from Gaussian with mean zero!
    rv = stats.norm(0, sigma)

    # compute the individual log-likelihood
    residual = _residual(capital, ctry, g, n, s, delta, rho, omega)
    individual_likelihood = rv.pdf(residual)
    return np.log(individual_likelihood)


if __name__ == '__main__':
    
    # ordering is g, n, s, delta, rho, sigma, omega
    test_params = np.array([0.02, 0.02, 0.15, 0.04, 1.5, 0.01, 0.33])

    ctry = 'USA'
    N = pwt_data.major_xs(ctry)['labsh'].size
    test_capital = np.ones(N)

    print individual_log_likelihood(test_capital, ctry, *test_params)