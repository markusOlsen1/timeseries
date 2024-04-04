def ARX(output, inputs, lags):
    lagged_vars = [f"{var}.l{lags}" for var in [output] + inputs]
    formula = f"{output} ~ 0 + {' + '.join(lagged_vars)}"
    return formula

# Example usage:
output_var = "Y"
input_vars = ["X1", "X2", "X3"]
lags = 3

formula = ARX(output_var, input_vars, lags)
print(formula)
