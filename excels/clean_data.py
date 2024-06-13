import pandas as pd

df = pd.read_csv('actual_data_2018.csv',encoding='latin1')


# Convert the 'Date/Time' column to datetime
df['Date/Time'] = pd.to_datetime(df['Date/Time'])
#, format='%d-%m-%Y %H:%M'
# Set 'Date/Time' as the index (optional, but useful for time series data)
df.set_index('Date/Time', inplace=True)

missing_before = df['100m_N Avg [m/s]'].isnull().sum()
missing_before_s = df['100m_N Std [m/s]'].isnull().sum()

# Interpolate missing values
df['100m_N Avg [m/s]'] = df['100m_N Avg [m/s]'].interpolate(method='linear')
df['100m_N Std [m/s]'] = df['100m_N Std [m/s]'].interpolate(method='linear')
# df.to_csv('north_changed.csv')

# Count missing values after interpolation
missing_after = df['100m_N Avg [m/s]'].isnull().sum()
missing_after_s = df['100m_N Std [m/s]'].isnull().sum()

# Calculate the number of rows affected
rows_affected = missing_before - missing_after
rows_affected_s = missing_before_s - missing_after_s

print(df['100m_N Avg [m/s]'])
df_reset = df.reset_index()
new_column = ['Date/Time','100m_N Avg [m/s]','100m_N Std [m/s]','Pressure [mbar]','98m WV [°]','78m WV [°]','48m WV [°]','Temp 5m [°C]','Hum 5m [%]']

new_data = df_reset[new_column].reset_index()

new_data.to_csv('2018-wind-ftr.csv',index=False)

print(f'Number of rows affected by interpolation: {rows_affected}')
print(f'Number of rows affected by interpolation: {rows_affected_s}')