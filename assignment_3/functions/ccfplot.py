import numpy as np
import matplotlib.pyplot as plt

def ccfplot(fit, data):
    if fit.__class__.__name__ == "OLS":  # Checking if the fit object is from statsmodels OLS
        res = np.full(len(data), np.nan)
        res[fit.resid.index.astype(int)] = fit.resid
    elif fit.__class__.__name__ == "MARIMA":  # Checking if the fit object is from marima
        res = fit.residuals[0]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    i = fit.resid.index.astype(int)
    for ax, col in zip(axes, ["Pinner", "Touter", "Ta"]):
        ccf_res = np.correlate(fit.resid[i], data[col][i], mode='full')
        ax.plot(np.arange(-(len(ccf_res)//2), len(ccf_res)//2 + 1), ccf_res)
        ax.set_title(f"CCF(residuals,{col})")
        ax.axhline(0, color='black', lw=1)
        ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Example usage:
# ccfplot(fit, data)
