from scipy.optimize import minimize


# Define the objective function
def objective_function(x):
    return (x - 3) ** 2


# Initial guess
initial_guess = [0]

# Define bounds: here, x is constrained between 0 and 10
bounds = [(0, 10)]

# Define options
options = {
    'xtol': 1e-4,
    'ftol': 1e-4,
    'maxiter': 100,
    'disp': True
}

# Perform optimization using Powell's method with bounds and options
result = minimize(
    objective_function,
    x0=initial_guess,
    method='Powell',
    bounds=bounds,
    options=options
)

optimized_x = result.x
optimized_function_value = result.fun
print(result.x)
print(optimized_function_value)
