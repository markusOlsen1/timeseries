import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.regression.linear_model import RegressionResultsWrapper as OLS

def validate(fit,X):
    if isinstance(fit, OLS):  # Checking if the fit object is from statsmodels OLS
        i = fit.resid.index.astype(int)
        res = np.full(max(i), np.nan)
        res = fit.resid
    elif isinstance(fit, marima):  # Checking if the fit object is from marima (replace 'marima' with your module/class name)
        res = fit.residuals[0]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    ax1.plot(res, marker='o', linestyle='-')
    ax1.plot(X['Pinner'], color='red')  # Note: 'X' is not defined here, you need to define it or pass it as an argument
    ax1.set_xlim(0, len(res))
    ax1.legend(['Residuals', 'Power'])
    ax1.set_title('Residuals and Power')

    plot_acf(res, ax=ax2)
    ax2.set_title('ACF (residuals)')

    plot_pacf(res, ax=ax3)
    ax3.set_title('PACF (residuals)')

    plt.tight_layout()
    plt.show()

# Example usage:
# validate(fit)
