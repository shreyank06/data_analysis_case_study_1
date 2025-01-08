import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import os

# ============================
# Helper Functions
# ============================

def save_plot(filename):
    """Save the current plot to a file."""
    os.makedirs("plots_2", exist_ok=True)  # Ensure the "plots_2" directory exists
    plt.savefig(f"plots_2/{filename}")
    plt.close()


def seasonal_decomposition(df, column, period=52):
    """Perform and save overall seasonal decomposition."""
    seasonal_result = seasonal_decompose(df.set_index('date')[column], model='additive', period=period)
    seasonal_result.plot()
    save_plot(f"seasonal_decomposition_{column}.png")
    print(f"Saved overall seasonal decomposition plot for {column}.")


def pad_and_decompose_per_year(df, column, period=52):
    """
    Perform seasonal decomposition for each year with padded data to prevent edge truncation.
    """
    df['year'] = df['date'].dt.year  # Extract year from the date
    unique_years = df['year'].unique()

    for year in unique_years:
        yearly_data = df[df['year'] == year].set_index('date').resample('W').sum()

        # Pad the dataset with forward and backward values
        padded_df = yearly_data.copy()
        padded_df = padded_df.reindex(
            pd.date_range(start=yearly_data.index.min() - pd.Timedelta(weeks=period),
                          end=yearly_data.index.max() + pd.Timedelta(weeks=period),
                          freq='W')
        )

        # Fill missing values using interpolation and forward/backward fill
        padded_df[column] = padded_df[column].interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')

        # Perform decomposition on the padded dataset
        decomposition = seasonal_decompose(padded_df[column], model='additive', period=period)

        # Plot decomposition
        plt.figure(figsize=(12, 10))

        plt.subplot(411)
        plt.plot(decomposition.observed, label='Observed', color='blue')
        plt.title(f"{column.capitalize()} Decomposition for {year}: Observed")
        plt.legend()

        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend', color='orange')
        plt.title("Trend")
        plt.legend()

        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonal', color='green')
        plt.title("Seasonal")
        plt.legend()

        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residual', color='red')
        plt.title("Residual")
        plt.legend()

        plt.tight_layout()
        save_plot(f"decomposition_{column}_{year}.png")
        print(f"Saved decomposition plot for {column} in {year}.")


def yearly_visualizations(df, columns):
    """Generate and save yearly visualizations for weekly trends."""
    df['year'] = df['date'].dt.year  # Extract year
    df['week'] = df['date'].dt.isocalendar().week  # Extract week number

    for year in df['year'].unique():
        yearly_data = df[df['year'] == year]

        plt.figure(figsize=(15, 7))
        for column in columns:
            plt.plot(
                yearly_data['date'],
                yearly_data[column],
                marker='o',
                label=f"{column.capitalize()}"
            )

        plt.xticks(rotation=45)
        plt.title(f"Weekly Trends for {year}")
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.legend(title="Metrics")
        plt.grid()
        save_plot(f"weekly_trends_{year}.png")
        print(f"Saved yearly visualization for {year}: weekly_trends_{year}.png")


def quarterly_visualizations(df, column, title, ylabel):
    """Generate and save quarterly visualizations."""
    df['quarter'] = df['date'].dt.to_period('Q')  # Extract quarter information
    quarterly_data = df.groupby('quarter')[column].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x=quarterly_data['quarter'].astype(str), y=quarterly_data[column])
    plt.title(title)
    plt.xlabel("Quarter")
    plt.ylabel(ylabel)
    plt.grid(axis='y')
    save_plot(f"{column}_quarterly.png")
    print(f"Saved quarterly visualization for {column} as {column}_quarterly.png")

# ============================
# Main Analysis
# ============================

def main():
    # Load the dataset
    df_meta_data = pd.read_csv("data_for_forecast.csv")
    df_meta_data['date'] = pd.to_datetime(df_meta_data['date'])

    # Overall seasonal decomposition for target and promo rates
    seasonal_decomposition(df_meta_data, 'target', period=52)
    seasonal_decomposition(df_meta_data, 'total_promo_rate_1', period=52)
    seasonal_decomposition(df_meta_data, 'total_promo_rate_2', period=52)

    # Seasonal decomposition per year with padding
    pad_and_decompose_per_year(df_meta_data, 'target', period=52)
    pad_and_decompose_per_year(df_meta_data, 'total_promo_rate_1', period=52)
    pad_and_decompose_per_year(df_meta_data, 'total_promo_rate_2', period=52)

    # Yearly visualizations for target, revenue, stock, and promo rates
    yearly_visualizations(df_meta_data, ['target', 'revenue', 'stock', 'total_promo_rate_1', 'total_promo_rate_2'])

    # Quarterly visualizations for target, revenue, and promo rates
    quarterly_visualizations(df_meta_data, 'target', "Quarterly Sales Trends", "Total Sales")
    quarterly_visualizations(df_meta_data, 'revenue', "Quarterly Revenue Trends", "Total Revenue")
    quarterly_visualizations(df_meta_data, 'total_promo_rate_1', "Quarterly Promo Rate 1 Trends", "Promo Rate 1")
    quarterly_visualizations(df_meta_data, 'total_promo_rate_2', "Quarterly Promo Rate 2 Trends", "Promo Rate 2")


if __name__ == "__main__":
    main()
