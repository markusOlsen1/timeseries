import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import ccf
from statsmodels.regression.linear_model import OLS
from functions import ARX, ccfplot, lagdf, validate

# Source the files in the "functions" folder
# Assuming the functions are already imported or defined in the functions/__init__.py file

# Make plots
X = pd.read_csv("data/experiment1.csv", sep=",", header=0)
# Convert to t_1 = 0
X['t'] = X['t'] - X['t'][0]

plt.figure(figsize=(10, 15))
plt.subplot(511)
plt.plot(X['t'], X['Ta'])
plt.subplot(512)
plt.plot(X['t'], X['Tinner'])
plt.subplot(513)
plt.plot(X['t'], X['Touter'])
plt.subplot(514)
plt.plot(X['t'], X['Pinner'])
plt.subplot(515)
plt.plot(X['t'], X['Pouter'])
plt.show()

# ccfs
ccf(X['Tinner'], X['Pinner'], lag_max=50)
plt.title('CCF(Tinner, Pinner)')
plt.show()

# Use the lagdf to make lags
X_lagged = lagdf(X.iloc[:, 1:6], 1)

# Add the lags to X
maxlag = 10
for i in range(1, maxlag + 1):
    tmp = lagdf(X.iloc[:, 1:6], i)
    tmp.columns = [f'{col}.l{i}' for col in tmp.columns]
    X = pd.concat([X, tmp], axis=1)

# Fit an ARX
model_formula = "Tinner ~ Tinner_l1 + Pinner_l1 + Touter_l1"
fit = OLS.from_formula(model_formula, data=X).fit()
print(fit.summary())

# Function for making a formula for lm
print(ARX("Tinner", ["Touter"], 1))
print(ARX("Tinner", ["Touter", "Pouter"], list(range(1, 11))))

# Fit and print
fit = OLS.from_formula(ARX("Tinner", ["Touter"], 1), data=X).fit()
print(fit.summary())

# Validation plot
validate(fit)

# CCF plot
ccfplot(fit, X)

# Do you know the stepping function?
fit = OLS.from_formula(ARX("Tinner", ["Touter"], list(range(1, 6))), data=X).fit()
print(fit.summary())
# print(summary(step(fit)))  # Need to implement step function or use alternative

# The AIC
print(f"AIC: {fit.aic}")

# Use this to find a suitable ARX model and use it

# Use a modified version of the marima package!
# Install from file
# download.file("https://02417.compute.dtu.dk/material/marima2_0.1.tar.gz", "marima2_0.1.tar.gz")
# install.packages("marima2_0.1.tar.gz", repos=NULL)
# from marima2 import marima  # Assuming it's installed and imported

# ARMAX model example
X = X.iloc[:, :6]  # Assuming you only need the first 6 columns
fit = marima("Tinner ~ AR(1:2) + Touter(1:2) + MA(1:2)", data=X)
print(fit.summary())
validate(fit)

# Stepping in marima (always be careful...but very useful in many situations)
fit = marima("Tinner ~ AR(1:10) + Touter(1:10) + Pinner(1:10) + MA(1:10)", data=X, penalty=2)
print(fit.summary())

# Multi-step forecasts
val = fit.predict(nstep=len(X) - 1)
plt.plot(X['Tinner'])
plt.plot(val.forecasts[0], color='red')
plt.show()

# armax-simulate-step-response
input_col = "Pinner"
Xs = X.iloc[:, 1:6].copy()
Xs[input_col] = 0
Xs['Tinner'] = 20
Xs['Touter'] = 20
Xs['Ta'] = 20
Xs.iloc[1:11, Xs.columns.get_loc(input_col)] += 100
val = fit.predict(Xs, nstep=len(X) - 1)
yhat = val.forecasts[0]
se = np.sqrt(val.pred_var[0, 0])
plt.plot(yhat)
plt.plot(yhat[1:] - 1.96 * se[1:], linestyle='--')
plt.plot(yhat[1:] + 1.96 * se[1:], linestyle='--')
plt.show()

# Steady state gain (DC-gain)
def gain_marima(fit, output, input_col):
    tbl = fit.summary().tables[1]
    return -tbl[tbl['Name'].str.contains(input_col), 'Estimate'].values[0] / tbl[tbl['Name'].str.contains("AR"), 'Estimate'].sum()

print(gain_marima(fit, "Tinner", "Pinner"))

# Multi-output model (coupled system)
ARMAX = marima("Tinner ~ AR(1) + Touter(1) + MA(1)", "Touter ~ AR(1) + Tinner(1) + MA(1)", data=X, penalty=0)
print(ARMAX.summary())
validate(ARMAX)
