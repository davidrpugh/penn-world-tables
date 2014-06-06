import numpy as np
from scipy import stats

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

