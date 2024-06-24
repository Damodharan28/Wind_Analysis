import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import plotly.graph_objs as go

# Load and preprocess the training dataset
train_df = pd.read_csv('../excels/2017-2018-clean.csv', parse_dates=['Date/Time'])

# Drop rows with NaN values
train_df = train_df.dropna()

# Rename columns for Prophet
train_df.rename(columns={
    'Date/Time': 'ds',
    '100m_N Avg [m/s]': 'y',
    '100m_N Std [m/s]': '100m_N_Std',
    'Pressure [mbar]': 'Pressure',
    '98m WV [°]': 'WV_98m',
    '78m WV [°]': 'WV_78m',
    '48m WV [°]': 'WV_48m',
    'Temp 5m [°C]': 'Temp_5m',
    'Hum 5m [%]': 'Hum_5m'
}, inplace=True)

# Prepare the data for Prophet
prophet_model = Prophet()
# prophet_model.add_regressor('100m_N_Std')
prophet_model.add_regressor('Pressure')
prophet_model.add_regressor('WV_98m')
prophet_model.add_regressor('WV_78m')
prophet_model.add_regressor('WV_48m')
prophet_model.add_regressor('Temp_5m')
prophet_model.add_regressor('Hum_5m')

# Fit the Prophet model
prophet_model.fit(train_df)

# Load and preprocess the testing dataset
test_df = pd.read_csv('../excels/2018-2019-clean.csv', parse_dates=['Date/Time'])

# Drop rows with NaN values
test_df = test_df.dropna()

# Rename columns for Prophet
test_df.rename(columns={
    'Date/Time': 'ds',
    '100m_N Avg [m/s]': 'y',
    'Pressure 5m [mbar]': 'Pressure',
    '98m WV [°]': 'WV_98m',
    '78m WV [°]': 'WV_78m',
    '48m WV [°]': 'WV_48m',
    'Temp 5m [°C]': 'Temp_5m',
    'Hum 5m': 'Hum_5m'
}, inplace=True)

# Make predictions on the test dataset
forecast_test = prophet_model.predict(test_df)

# Calculate accuracy metrics
y_true = test_df['y']
y_pred = forecast_test['yhat']

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
r_squared = r2_score(y_true, y_pred)

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"R-Squared: {r_squared}")

# Create interactive plot with Plotly
fig = go.Figure()

# Add actual data trace for training and testing datasets
fig.add_trace(go.Scatter(x=train_df['ds'], y=train_df['y'], mode='markers', name='Actual Train', marker=dict(color='black')))
fig.add_trace(go.Scatter(x=test_df['ds'], y=test_df['y'], mode='markers', name='Actual Test', marker=dict(color='red')))

# Add forecasted data trace for training and testing datasets
fig.add_trace(go.Scatter(x=forecast_test['ds'], y=forecast_test['yhat'], mode='lines', name='Forecast Test', line=dict(color='green')))

# Add confidence interval traces for training and testing datasets
fig.add_trace(go.Scatter(x=forecast_test['ds'], y=forecast_test['yhat_upper'], mode='lines', name='Upper Confidence Interval Test',
                         line=dict(color='lightgreen'), fill=None))
fig.add_trace(go.Scatter(x=forecast_test['ds'], y=forecast_test['yhat_lower'], mode='lines', name='Lower Confidence Interval Test',
                         line=dict(color='lightgreen'), fill='tonexty', fillcolor='rgba(144, 238, 144, 0.2)'))

# Update layout for interactivity
fig.update_layout(
    title='Wind Speed Forecast',
    xaxis_title='Date',
    yaxis_title='Wind Speed (m/s)',
    xaxis_rangeslider_visible=True,
    xaxis_rangeselector=dict(
        buttons=list([
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(step='all')
        ])
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode='x'
)

# Show the plot
fig.show()
