def predicted_labor_share(capital, g, n, s, delta, rho, sigma, omega):
    """Model predicted share of income going to labor."""
    if abs(rho) <= 1e-3:
        labor_share = omega
    else:
        labor_share = (1 - omega) / (omega * capital**rho + (1 - omega))

    return labor_share

if __name__ == '__main__':
    test_params = {'n':0.02, 'g':0.02, 's':0.15, 'delta':0.04, 'rho':1.5,
                    'sigma':0.01, 'omega':0.33}

    print predicted_labor_share(10.0, **test_params)