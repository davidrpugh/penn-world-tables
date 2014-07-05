"""Module for testing out new ideas and playing around."""

import numpy as np
from scipy import integrate, optimize, stats

import pwt

# load the Penn World Tables data
pwt_data = pwt.load_pwt_data()


def _ces_marginal_product_capital(capital, rho, omega):
    """Marginal product of capital (per effective worker)."""
    if abs(rho) < 1e-3:
        mpk = omega * capital**(omega - 1)
    else:
        mpk = ((omega * capital**(rho - 1)) / (omega * capital**rho + (1 - omega)) *
               _ces_output(capital, rho, omega))

    return mpk


def _ces_output(capital, rho, omega):
    """Constant elasticity of substitution (CES) production function."""
    if abs(rho) < 1e-3:
        output = capital**omega
    else:
        output = (omega * capital**rho + (1 - omega))**(1 / rho)

    return output


def solow_jacobian(time, capital, n, g, s, delta, rho, omega):
    """Jacobian for equation of motion for capital (per effective worker)."""
    marginal_benefit = s * _ces_marginal_product_capital(capital, rho, omega)
    marginal_cost = n + g + delta

    return marginal_benefit - marginal_cost


def solow_model(time, capital, n, g, s, delta, rho, omega):
    """Equation of motion for capital (per effective worker)."""
    actual_investment = s * _ces_output(capital, rho, omega)
    break_even_investment = (n + g + delta) * capital

    return actual_investment - break_even_investment


def _ces_technology(capital, labor, output, rho, omega):
    """Technology as a residual of the CES production function."""
    output_per_worker = output / labor
    capital_labor_ratio = capital / labor

    if abs(rho) < 1e-3:
        tech = (output_per_worker / capital_labor_ratio**omega)**(1 / (1 - omega))
    else:
        tech = ((1 / (1 - omega)) * output_per_worker**rho +
                (omega / (1 - omega)) * capital_labor_ratio**rho)**(1 / rho)

    return tech


def _initial_condition(ctry, start, rho, omega):
    """Initial condition for capital (per effective worker)."""
    initial_capital = pwt_data.major_xs(ctry)['rkna'][start]
    initial_labor = pwt_data.major_xs(ctry)['emp'][start]
    initial_output = pwt_data.major_xs(ctry)['rgdpna'][start]
    initial_technology = _ces_technology(initial_capital, initial_labor,
                                         initial_output, rho, omega)

    return initial_capital / (initial_technology * initial_labor)


def _predicted_labor_share(capital, rho, omega):
    """Model predicted share of income going to labor."""
    if abs(rho) <= 1e-3:
        labor_share = omega
    else:
        labor_share = (1 - omega) / (omega * capital**rho + (1 - omega))

    return labor_share


def _residual(capital, labor_share, rho, omega):
    """Difference between actual and model predicted labor share."""
    actual_labor_share = labor_share
    predicted_labor_share = _predicted_labor_share(capital, rho, omega)
    return actual_labor_share - predicted_labor_share


def _individual_ll(capital, labor_share, rho, sigma, omega):
    """Individual model log likelihood."""
    # residual is assumed to be drawn from Gaussian with mean zero!
    rv = stats.norm(0, sigma)

    # compute the individual log-likelihood
    residual = _residual(capital, labor_share, rho, omega)
    individual_likelihood = rv.pdf(residual)

    return np.log(individual_likelihood)


def objective(params, ctry, start, end):
    """Total negative log-likelihood for the model."""
    # unpack parameters
    g, n, s, delta, rho, sigma, omega = params

    # get relevant labor share data
    labor_share = pwt_data.major_xs(ctry)['labsh'][start:end]

    # solve for the time path of capital
    k0 = _initial_condition(ctry, start, rho, omega)

    # compute the total log-likelihood
    total_ll = np.sum(_individual_ll(k0, labor_share, rho, sigma, omega))

    return -total_ll


if __name__ == '__main__':

    # ordering is g, n, s, delta, rho, sigma, omega
    g, n, s, delta, rho, sigma, omega = 0.02, 0.02, 0.15, 0.04, 0.0, 0.05, 0.33
    test_params = np.array([g, n, s, delta, rho, sigma, omega])

    ctry = 'USA'
    N = pwt_data.major_xs(ctry)['labsh'].size
    test_capital = np.ones(N)

    # print individual_log_likelihood(test_capital, ctry, *test_params)
    print objective(test_params, ctry, '1950-01-01', '1950-01-01')

    result = optimize.minimize(objective,
                               x0=test_params,
                               args=(ctry, '1950-01-01', '1950-01-01'),
                               method='Nelder-Mead',
                               options={'maxfev': 1000},
                               )

    # play about with solving the Solow model...
    k0 = _initial_condition(ctry, '1950-01-01', rho, omega)
    r = integrate.ode(solow_model, solow_jacobian)
    r.set_integrator('dopri5', atol=1e-9, rtol=1e-9)
    r.set_initial_value(k0, 1950)
    r.set_f_params(*result.x)
    r.set_jac_params(*result.x)

    T = 2011
    dt = 1.0

    while r.successful() and r.t < T:
        r.integrate(r.t + dt)
        print("%g %g" % (r.t, r.y))
