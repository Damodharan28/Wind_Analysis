import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('monthly_data_1.csv',encoding='latin1')
# # Moving average
# df['Moving_Avg'] = df['100m_N Avg [m/s]'].head().rolling(window=7).mean()

# # Plot moving average
# plt.figure(figsize=(10, 6))
# plt.plot(df.index, df['100m_N Avg [m/s]'], marker='o', linestyle='-', label='Original')
# plt.plot(df.index, df['Moving_Avg'], color='red', linestyle='-', label='7-day Moving Average')
# plt.title('Wind Speed with Moving Average')
# plt.xlabel('Date/Time')
# plt.ylabel('100m_N Avg [m/s]')
# plt.legend()
# plt.show()

#---------------------------------------------------------------------------------------------

# Read the CSV file
df = pd.read_csv('monthly_data_1.csv',encoding='latin1')

# Assuming 'Timestamp' is the column containing the timestamps and 'WindSpeed' is the column containing the wind speed data
# Convert 'Timestamp' to datetime format
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# Set 'Timestamp' as the index
df.set_index('Date/Time', inplace=True)

# Calculate a 1-hour (6 data points) moving average
df['1-hour MA'] = df['100m_N Avg [m/s]'].rolling(window=144).mean()

# Plot the original data and the moving average
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['100m_N Avg [m/s]'], label='Original Data', color='blue')
plt.plot(df.index, df['1-hour MA'], label='1-hour Moving Average', color='red')
plt.xlabel('Time')
plt.ylabel('100m_N')
plt.title('Wind Speed Data with 1-hour Moving Average')
plt.legend()
plt.show()
