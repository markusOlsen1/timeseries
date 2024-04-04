import pandas as pd

def lagdf(x, lag):
    # Lag x, i.e. delay x lag steps
    if lag > 0:
        x.iloc[(lag+1):] = x.iloc[:(len(x)-(lag+1))].values
        x.iloc[:lag] = None
    elif lag < 0:
        # Lag x "ahead in time"
        x.iloc[:lag] = x.iloc[-lag:].values
        x.iloc[(len(x)+lag):] = None
    return x

# Test
# data = pd.DataFrame({'x': range(1, 11), 'y': range(10, 0, -1)})
# print(lagdf(data, 2))
# print(lagdf(data, -2))
