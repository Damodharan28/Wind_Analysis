import pandas as pd
from dateutil import parser

# Custom date parser function
def parse_date(date_str):
    for fmt in ("%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return parser.parse(date_str)  # Fallback to dateutil.parser if formats don't match

# Load data
df = pd.read_csv('../excels/2018-2019-raw.csv', encoding='latin1')

# Print column names to check for any discrepancies
print("Column names in the DataFrame:")
print(df.columns)

# Convert 'Date/Time' column to datetime using the custom date parser
df['Date/Time'] = df['Date/Time'].apply(parse_date)

# Set 'Date/Time' as the index
df.set_index('Date/Time', inplace=True)

# Define the columns to interpolate
columns_to_interpolate = [
    '100m_N Avg [m/s]', 'Pressure 5m [mbar]', 
    '98m WV [°]', '78m WV [°]', '48m WV [°]', 
    'Temp 5m [°C]', 'Hum 5m'
]

# Check if all expected columns are present
missing_columns = [col for col in columns_to_interpolate if col not in df.columns]
if missing_columns:
    print(f"The following columns are missing from the DataFrame: {missing_columns}")
else:
    # Count missing values before interpolation
    missing_before = {col: df[col].isnull().sum() for col in columns_to_interpolate}

    # Interpolate missing values
    df[columns_to_interpolate] = df[columns_to_interpolate].interpolate(method='linear')

    # Count missing values after interpolation
    missing_after = {col: df[col].isnull().sum() for col in columns_to_interpolate}

    # Calculate the number of rows affected by interpolation
    rows_affected = {key: missing_before[key] - missing_after[key] for key in missing_before}

    # Reset index and select necessary columns
    df_reset = df.reset_index()
    columns_to_save = ['Date/Time'] + columns_to_interpolate
    new_data = df_reset[columns_to_save]

    # Save the cleaned data to a new CSV file
    new_data.to_csv('../excels/2018-2019-clean.csv', index=False)

    # Print the number of rows affected by interpolation for each column
    for column, count in rows_affected.items():
        print(f'Number of rows affected by interpolation ({column}): {count}')
