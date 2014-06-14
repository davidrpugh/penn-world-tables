import sympy as sp 

# define symbolic variables
sp.var('f, k')
sp.var('alpha, delta, sigma, n, g, s')

# define constant elasticity of substitution production function
rho = (sigma - 1) / sigma
f = (k**rho + (1 - alpha))**(1 / rho)

# define equation of motion for k
k_dot = s * f - (n + g + delta) * k

