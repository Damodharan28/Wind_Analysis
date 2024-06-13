import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('monthly_data_1.csv')

df = pd.read_csv('monthly_data_1.csv', encoding='latin1')
# df = pd.read_csv('monthly_data_1.csv', encoding='iso-8859-1')
# df = pd.read_csv('monthly_data_1.csv', encoding='cp1252')

df.set_index('Date/Time', inplace=True)
one_day = df.iloc[144:288]
hourly_ticks = one_day.index[::6]

# Line plot
plt.figure(figsize=(10, 6))
plt.plot(one_day.index, one_day['100m_N Avg [m/s]'], marker='o', linestyle='-')
plt.title('Wind Speed over Time')
plt.xlabel('Date/Time')
plt.ylabel('100m_N Avg [m/s]')

plt.xticks(hourly_ticks, rotation=45)

plt.tight_layout()

plt.show()
