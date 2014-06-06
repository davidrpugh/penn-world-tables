import numpy as np
from scipy import stats

import pwt

def _technology(capital, labor, output, alpha, rho):
    """Technology as a residual of the CES production function."""
    output_per_worker = output / labor
    capital_labor_ratio = capital / labor

    if abs(rho) < 1e-3:
        tech = (output_per_worker / capital_labor_ratio**alpha)**(1 / (1 - alpha))
    else:
        tech = ((1 / (1 - alpha)) * output_per_worker**rho + 
                (alpha / (1 - alpha)) * capital_labor_ratio**rho)**(1 / rho)

    return tech

def _epsilon(new_tech, old_tech):
    """Simple disturbance term."""
    eps = np.log(new_tech.values) - np.log(old_tech.values)
    return eps

def _individual_log_likelihood(g, sigma, epsilon):
    """Individual log-likelihood function assuming Normal disturbance."""
    log_likelihood = np.log(stats.norm.pdf(epsilon, loc=g, scale=sigma))
    return log_likelihood

def total_log_likelihood(params, ctry_code, data):
    """
    Computes the total log-likelihood for model.

    Args:

        params: (ndarray) Array of parameter values.
        ctry_code (str) ISO-3 Country code.
        data: (Panel) PWT data as a Pandas Panel object.

    Returns:

        total_ll: (float) Total log-likelihood.

    """
    # extract the parameters
    alpha, rho, sigma, g = params

    ctry_data = data.major_xs(ctry_code)
    capital = ctry_data['rkna']
    emp = ctry_data['emp']
    hc = ctry_data['hc']
    labor = emp * hc
    output = ctry_data['rgdpna']

    new_tech = _technology(capital, labor, output, alpha, rho)[1:]
    old_tech = _technology(capital, labor, output, alpha, rho)[:-1]

    eps = _epsilon(new_tech, old_tech)

    total_ll = np.sum(_individual_log_likelihood(g, sigma, eps))    

    return total_ll

if __name__ == '__main__':
    pwt_panel_data = pwt.load_pwt_data()

    alpha, rho, g, sigma = 0.5, 0.9, 0.03, 0.08
    initial_guess = np.array([alpha, rho, g, sigma])
    print total_log_likelihood(initial_guess, 'GBR', pwt_panel_data)

