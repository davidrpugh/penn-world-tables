import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
import sympy as sp 

import pwt

# load the Penn World Tables data
pwt_data = pwt.load_pwt_data()

plt.figure(figsize=(10,8))

# plot some labor shares
for ctry in pwt_data.major_axis:
    
    if ctry == 'USA':
        pwt_data.major_xs(ctry)['labsh'].plot(color='b', label=ctry)
    elif ctry == 'GBR':
        pwt_data.major_xs(ctry)['labsh'].plot(color='orange', label=ctry)
    elif ctry == 'JPN':
        pwt_data.major_xs(ctry)['labsh'].plot(color='purple', label=ctry)
    elif ctry == 'KOR':
        pwt_data.major_xs(ctry)['labsh'].plot(color='magenta', label=ctry)
    elif ctry == 'CHN':
        pwt_data.major_xs(ctry)['labsh'].plot(color='r', label=ctry)
    elif ctry == 'IND':
        pwt_data.major_xs(ctry)['labsh'].plot(color='g', label=ctry)
    else:    
        pwt_data.major_xs(ctry)['labsh'].plot(alpha=0.5, color='grey', 
                                              label='_nolegend_')
    
# demarcate the global average
pwt_data['labsh'].mean(axis=0).plot(color='k', label='World avg.')

# add labels, title, legend, etc
plt.ylabel(r"$1-\alpha_K(k)$", fontsize=20, rotation='horizontal', labelpad=20)
plt.xlabel("Year, t", fontsize=20, family='serif')
plt.title("Labor's share of real GDP", fontsize=25, family='serif')
plt.legend(loc=0, frameon=False, prop={'family':'serif'})
plt.savefig('images/labor-shares.png')
plt.show()

# define symbolic variables
sp.var('f, k')
sp.var('alpha, delta, sigma, n, g, s')

# define intensive production function
rho = (sigma - 1) / sigma
_f_ces = (alpha * k**rho + (1 - alpha))**(1 / rho)
_f_cd = k**alpha

# define equation of motion for k
_k_dot_ces = s * _f_ces - (n + g + delta) * k
_k_dot_cd = s * _f_cd - (n + g + delta) * k

# define the system of equations...
_sym_solow_sys_ces = sp.Matrix([_k_dot_ces])
_sym_solow_sys_cd = sp.Matrix([_k_dot_cd])

# ...compute the Jacobian...
_sym_solow_jac_ces = _sym_solow_sys_ces.jacobian((k,))
_sym_solow_jac_cd = _sym_solow_sys_cd.jacobian((k,))

# ...compute the Hessian!
_sym_solow_hess_ces = sp.hessian(_sym_solow_sys_ces, (k,))
_sym_solow_hess_cd = sp.hessian(_sym_solow_sys_cd, (k,))

# wrap the symbolic expressions as vectorized NumPy functions
args = (k, alpha, delta, sigma, n, g, s)
_num_solow_sys_ces = sp.lambdify(args, _sym_solow_sys_ces, 'numpy')
_num_solow_jac_ces = sp.lambdify(args, _sym_solow_jac_ces, 'numpy')
_num_solow_hess_ces = sp.lambdify(args, _sym_solow_hess_ces, 'numpy')

_num_solow_sys_cd = sp.lambdify(args, _sym_solow_sys_cd, 'numpy')
_num_solow_jac_cd = sp.lambdify(args, _sym_solow_jac_cd, 'numpy')
_num_solow_hess_cd = sp.lambdify(args, _sym_solow_hess_cd, 'numpy')

def solow_steady_state(k, params): 
    """
    Returns the steady state of the Solow model.

    Inputs:

        k: (float) Capital stock per effective worker

        params: (dict) Dictionary of model parameters.

    Returns:

        ss: (ndarray) Steady state value for capital stock per effective
            worker.

    """
    sigma = params['sigma']
    rho = (sigma - 1) / sigma

    # nest cobb-douglas production as special case
    if abs(rho) < 1e-6:
        ss = np.array(_num_solow_sys_cd(*k, **params))
    else:
        ss = np.array(_num_solow_sys_ces(*k, **params))

    return ss.flatten()

def solow_jacobian(k, params): 
    """
    Returns the Jacobian of the Solow model.

    Inputs:

        k: (float) Capital stock per effective worker

        params: (dict) Dictionary of model parameters.

    Returns:

        jac: (ndarray) Derivative of the equation of motion for capital per
             effective worker with respect to k.

    """
    sigma = params['sigma']
    rho = (sigma - 1) / sigma

    # nest cobb-douglas production as special case
    if abs(rho) < 1e-6:
        jac = np.array(_num_solow_jac_cd(*k, **params))
    else:
        jac = np.array(_num_solow_jac_ces(*k, **params))

    return jac

# define some model params
solow_params = {'alpha':0.479, 'delta':0.038, 'sigma': 0.789, 'n':0.016, 'g':0.017, 
                's':0.207}

res = optimize.root(solow_steady_state,
                    x0=np.array([5.0]),
                    args=(solow_params,),
                    jac=solow_jacobian,
                    method='hybr',
                    )



