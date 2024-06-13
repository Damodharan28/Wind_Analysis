# import pandas as pd
# from prophet import Prophet

# Load your data
df = pd.read_csv('../main.csv')

# Convert the date column to datetime
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# training
train_df = df[(df['Date/Time'] >= '2017-11-01') & (df['Date/Time'] <= '2017-11-30')]

# Prophet requires columns to be named 'ds' and 'y'
train_df = train_df.rename(columns={'Date/Time': 'ds', '100m_N Avg [m/s]': 'y'})

#-------------------------------------------------------------------------------

# Initializeee the model
model = Prophet()

# Train the model
model.fit(train_df)

#--------------------------------------------------------------------------------

# Create a DataFrame with future dates for 2019
future_dates = pd.date_range(start='2018-11-01', end='2018-11-30', freq='D')
future_df = pd.DataFrame({'ds': future_dates})

# Make predictions
forecast = model.predict(future_df)

#--------------------------------------------------------------------------------

# Load the actual data for 2019
dff = pd.read_csv('../2018.csv')
actual_df = dff[(dff['Date/Time'] >= '2018-11-01') & (dff['Date/Time'] <= '2018-11-30')].rename(columns={'Date/Time': 'ds', '100m_N Avg [m/s]': 'y'})

# Merge the actual data with the predictions
comparison_df = actual_df[['ds', 'y']].merge(forecast[['ds', 'yhat']], on='ds')

# Calculate evaluation metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(comparison_df['y'], comparison_df['yhat'])
mse = mean_squared_error(comparison_df['y'], comparison_df['yhat'])
rmse = mean_squared_error(comparison_df['y'], comparison_df['yhat'], squared=False)
r2 = r2_score(comparison_df['y'], comparison_df['yhat'])

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')
print(f'R-squared: {r2}')

#----------------------------------------------------------------------------------