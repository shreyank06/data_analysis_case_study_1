import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
import duckdb
import subprocess


# ============================
# Helper Functions
# ============================

def load_data(conn, query):
    """Load data from DuckDB."""
    df = conn.sql(query).df()
    df['date'] = pd.to_datetime(df['date'])
    df = df.fillna(0)
    return df


def save_plot(filename):
    """Save the current plot to a file."""
    plt.savefig(f"plots_2/{filename}")
    plt.close()


def eda_summary(df):
    """Print summary statistics and check for missing values."""
    print("Summary Statistics:")
    summary = df.describe()
    print(summary)

    print("\nMissing Values:")
    missing = df.isnull().sum()
    print(missing)

    # Write insights to a file
    with open("eda_summary.txt", "w") as f:
        f.write("Summary Statistics:\n")
        f.write(summary.to_string())
        f.write("\n\nMissing Values:\n")
        f.write(missing.to_string())


def plot_correlation(df):
    """Generate and save a correlation heatmap."""
    correlation = df[['target', 'revenue', 'stock', 'total_promo_rate_1', 'total_promo_rate_2']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Key Variables")
    save_plot("correlation_matrix.png")


def plot_distributions(df, numeric_cols):
    """Generate and save histograms for numeric columns."""
    for col in numeric_cols:
        plt.figure(figsize=(10, 5))
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid()
        save_plot(f"{col}_distribution.png")


def apply_winsorization(df, col, limits=(0.01, 0.01)):
    """Apply Winsorization to handle outliers in the specified column."""
    print(f"Applying Winsorization on {col} with limits {limits}.")
    df[f"{col}_winsorized"] = winsorize(df[col], limits=limits)
    return df


# ============================
# Main Data Loading and EDA
# ============================

def main():
    # Connect to DuckDB and load data
    conn = duckdb.connect("../data/retail_sales.duckdb")
    df_meta_data = load_data(conn, """
        SELECT * 
        FROM dbt.data_for_forecasting
        ORDER BY date
    """)

    # Exclude rows where both target and revenue are 0
    df_meta_data = df_meta_data[(df_meta_data['target'] != 0) | (df_meta_data['revenue'] != 0)]

    # Apply Winsorization to the target variable
    df_meta_data = apply_winsorization(df_meta_data, 'target', limits=(0.01, 0.01))

    # # Apply Winsorization to promo rate columns (optional, if required)
    # df_meta_data = apply_winsorization(df_meta_data, 'total_promo_rate_1', limits=(0.01, 0.01))
    # df_meta_data = apply_winsorization(df_meta_data, 'total_promo_rate_2', limits=(0.01, 0.01))

    # EDA
    eda_summary(df_meta_data)
    plot_correlation(df_meta_data)
    plot_distributions(df_meta_data, ['target_winsorized', 'revenue', 'stock', 'total_promo_rate_1', 'total_promo_rate_2'])

    # Save data for further analysis
    df_meta_data.to_csv("data_for_forecast.csv", index=False)
    print("Data for forecasting saved to 'forecast.csv'.")

    # # Execute the second script
    # print("Executing the second script...")
    # subprocess.run(["python", "analysis_and_visualizations.py"])
    # print("Second script execution completed.")


if __name__ == "__main__":
    main()
