def ARX(output, inputs, lags):
    lagged_vars = [f"{var}.shift({lag})" for var in [output] + inputs for lag in range(1, lags+1)]
    formula = f"{output} ~ 0 + {' + '.join(lagged_vars)}"
    return formula

# Example usage:
output_var = "Y"
input_vars = ["X1", "X2", "X3"]
lags = 3

formula = ARX(output_var, input_vars, lags)
print(formula)
