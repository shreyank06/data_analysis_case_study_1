from nixtla import NixtlaClient
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================
# Configuration
# ============================

API_KEY = "nixak-DGN4s4hB7GFYPcGSH3uNCaJIIlRdzmnDAqdnEOfmowgUSw1LmmDw2C0EB7iHLuXV2Qwn69k1CDgKKRq2"

# Instantiate the NixtlaClient
nixtla_client = NixtlaClient(api_key=API_KEY)

# Validate the API key
nixtla_client.validate_api_key()
print("API key validated successfully!")

# ============================
# Load and Preprocess Data
# ============================

# Load the processed data
df_sales = pd.read_csv("data_for_forecast.csv")

# Ensure the date column is properly formatted
df_sales['date'] = pd.to_datetime(df_sales['date'])

# Rename columns to match NixtlaClient's expected format
df_sales = df_sales.rename(columns={'date': 'timestamp', 'target_winsorized': 'value'})

# Prepare exogenous variables
exogenous_features = ['revenue', 'stock', 'total_promo_rate_1', 'total_promo_rate_2']
X_df = df_sales[['timestamp'] + exogenous_features]

# ============================
# Forecast Sales for the Next 4 Weeks
# ============================

# Forecasting horizon (4 weeks)
forecast_horizon = 4

# Call the forecast function with exogenous variables
timegpt_fcst_df = nixtla_client.forecast(
    df=df_sales,
    h=forecast_horizon,
    time_col='timestamp',
    target_col='value',
    freq='W',  # Weekly frequency
    X_df=X_df,
    hist_exog_list=exogenous_features
)

# ============================
# Save and Display Forecast Results
# ============================

# Save the forecast to a CSV file
os.makedirs("forecast_results", exist_ok=True)
timegpt_fcst_df.to_csv("forecast_results/sales_forecast.csv", index=False)
print("Forecast saved to 'forecast_results/sales_forecast.csv'")

# Display the forecasted values
print("\nForecasted Sales for the Next 4 Weeks:")
print(timegpt_fcst_df)

# ============================
# Plot the Forecast
# ============================

# Combine historical and forecasted data for plotting
df_sales['type'] = 'Historical'
timegpt_fcst_df['type'] = 'Forecast'
timegpt_fcst_df = timegpt_fcst_df.rename(columns={'TimeGPT': 'value'})
combined_df = pd.concat([df_sales[['timestamp', 'value', 'type']], timegpt_fcst_df], ignore_index=True)

# Plot historical and forecasted values
plt.figure(figsize=(12, 6))
for label, df_segment in combined_df.groupby('type'):
    plt.plot(df_segment['timestamp'], df_segment['value'], label=label, marker='o')

# Add a vertical line for the start of the forecast
plt.axvline(x=df_sales['timestamp'].max(), color='red', linestyle='--', label='Forecast Start')

# Customize the plot
plt.title("Sales Forecast for the Next 4 Weeks")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.grid()

# Save and show the plot
plt.savefig("forecast_results/forecast_plot.png")
plt.show()
