from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('monthly_data_1.csv',encoding='latin1')
# Decompose the time series
result = seasonal_decompose(df['100m_N Avg [m/s]'].dropna(), model='additive', period=30)
result.plot()
plt.show()
