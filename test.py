import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

ts = ts.cumsum()

x = False;
while (x == False):
    ts.plot()