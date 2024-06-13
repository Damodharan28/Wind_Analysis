import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('monthly_data_1.csv')

df = pd.read_csv('monthly_data_1.csv', encoding='latin1')
# df = pd.read_csv('monthly_data_1.csv', encoding='iso-8859-1')
# df = pd.read_csv('monthly_data_1.csv', encoding='cp1252')
# Summary statistics
summary_stats = df['100m_N Avg [m/s]'].describe()
print(summary_stats)

# Autocorrelation plot
pd.plotting.autocorrelation_plot(df['100m_N Avg [m/s]'].dropna())
plt.show()
