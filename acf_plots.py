import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

# Read the CSV file
df = pd.read_csv('monthly_data_1.csv', encoding='latin1')

# Summary statistics
summary_stats = df['100m_N Avg [m/s]'].describe()
print(summary_stats)

# Autocorrelation plot
plt.figure(figsize=(12, 6))
plot_acf(df['100m_N Avg [m/s]'].dropna(), lags=144)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Plot of 100m_N Avg [m/s]')
plt.grid(True)
plt.show()
