import numpy as np
import pwt

# load the Penn World Tables data
pwt_data = pwt.load_pwt_data()

def predicted_labor_share(capital, g, n, s, delta, rho, sigma, omega):
    """Model predicted share of income going to labor."""
    if abs(rho) <= 1e-3:
        labor_share = omega
    else:
        labor_share = (1 - omega) / (omega * capital**rho + (1 - omega))

    return labor_share

def residual(capital, ctry, params):
    """Difference between actual and model predicted labor share."""
    actual_labor_share = pwt_data.major_xs(ctry)['labsh']
    return actual_labor_share - predicted_labor_share(capital, **params)

if __name__ == '__main__':
    
    test_params = {'n':0.02, 'g':0.02, 's':0.15, 'delta':0.04, 'rho':1.5,
                    'sigma':0.01, 'omega':0.33}

    ctry = 'USA'
    N = pwt_data.major_xs(ctry)['labsh'].size
    test_capital = np.ones(N)

    print residual(test_capital, ctry, test_params)