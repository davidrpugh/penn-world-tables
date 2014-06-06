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

if __name__ == '__main__':
    pwt_panel_data = pwt.load_pwt_data()

    capital = pwt_panel_data.major_xs('GBR')['rkna']
    emp = pwt_panel_data.major_xs('GBR')['emp']
    hc = pwt_panel_data.major_xs('GBR')['hc']
    labor = emp * hc
    output = pwt_panel_data.major_xs('GBR')['rgdpna']

    alpha, rho = 0.5, 0.5
    new_tech = _technology(capital, labor, output, alpha, rho)[1:]
    old_tech = _technology(capital, labor, output, alpha, rho)[:-1]

    print _epsilon(new_tech, old_tech)

