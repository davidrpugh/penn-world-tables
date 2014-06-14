import sympy as sp 

# define symbolic variables
sp.var('f, k')
sp.var('alpha, delta, sigma, n, g, s')

# define constant elasticity of substitution production function
rho = (sigma - 1) / sigma
f = (k**rho + (1 - alpha))**(1 / rho)

# define equation of motion for k
k_dot = s * f - (n + g + delta) * k

# define the system of equations...
_symbolic_solow_system = sp.Matrix([k_dot])

# ...compute the Jacobian...
_symbolic_solow_jacobian = _symbolic_solow_system.jacobian((k,))

# ...compute the Hessian!
_symbolic_solow_hessian = sp.hessian(_symbolic_solow_system, (k,))

# wrap the symbolic expressions as vectorized NumPy functions
args = (k, alpha, delta, sigma, n, g, s)
_numeric_solow_system = sp.lambdify(args, _symbolic_solow_system, 'numpy')
_numeric_solow_jacobian = sp.lambdify(args, _symbolic_solow_jacobian, 'numpy')
_numeric_solow_hessian = sp.lambdify(args, _symbolic_solow_hessian, 'numpy')


