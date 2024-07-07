#%% -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:24:13 2024

@author: tai4t
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("enzyme_dataset.csv", encoding="utf-8")
df = df.reset_index(drop=True)

logKm = np.log10(df["KM"].values)
logKm_ = logKm[~np.isnan(logKm)]

logkcat = np.log10(df["TURNOVER"].values.astype(float))
logkcat_ = logkcat[~np.isnan(logKm)]

x = 2*logkcat_
y = logKm_

a = np.linspace(-10,10)
b = a

#plot
mod = LinearRegression()
mod_lin = mod.fit(x.reshape(-1, 1), y.reshape(-1, 1))
y_lin_fit = mod_lin.predict(x.reshape(-1, 1))
r2_lin = mod.score(x.reshape(-1, 1), y.reshape(-1, 1))

fig = plt.figure(figsize = (8, 8))
ax = fig.add_subplot(111)
ax.set_ylim(-2.5, 7)
ax.set_xlim(-2.5, 7)
ax.set_xlabel("2*log $k_\mathrm{cat}$", size = "x-large")
ax.set_ylabel("log $K_\mathrm{m}$", size = "x-large")
ax.scatter(x, y, s=8, c="limegreen", alpha=0.2)
ax.text(-2, 6, "correlation : " + str(np.corrcoef(x,y)[0,1]), size=15, horizontalalignment="left")
ax.text(-2, 5.5, "regression : "+str(mod.coef_[0][0]), size=15, horizontalalignment="left")
ax.plot(a, b, c="b")
ax.plot(x.reshape(-1, 1), y_lin_fit, c="r", linewidth=0.5)
