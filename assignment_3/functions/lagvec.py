import numpy as np

def lagvec(x, lag):
    if lag > 0:
        # Lag x, i.e. delay x lag steps
        return np.concatenate((np.full(lag, np.nan), x[:-lag]))
    elif lag < 0:
        # Lag x, i.e. delay x lag steps
        return np.concatenate((x[-lag:], np.full(-lag, np.nan)))
    else:
        # lag = 0, return x
        return x

# Test
# x = np.array([1, 2, 3, 4, 5])
# print(lagvec(x, 2))
# print(lagvec(x, -2))
# print(lagvec(x, 0))
