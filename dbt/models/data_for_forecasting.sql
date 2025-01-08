WITH sales_data AS (
    SELECT
        DATE_TRUNC('week', sales.date) AS week_start,   -- Start of the week
        SUM(sales.sales) AS target,                    -- Weekly aggregated sales
        SUM(sales.revenue) AS total_revenue,           -- Weekly aggregated revenue
        AVG(sales.stock) AS avg_stock,                 -- Average stock over the week
        SUM(
            CASE 
                WHEN sales.promo_bin_1 = 'high' THEN 1.0
                WHEN sales.promo_bin_1 = 'medium' THEN 0.5
                WHEN sales.promo_bin_1 = 'low' THEN 0.0
                ELSE 0.0
            END
        ) AS total_promo_rate_1,  -- Total promo rate for promo_bin_1
        SUM(
            CASE 
                WHEN sales.promo_bin_2 = 'high' THEN 1.0
                WHEN sales.promo_bin_2 = 'medium' THEN 0.5
                WHEN sales.promo_bin_2 = 'low' THEN 0.0
                ELSE 0.0
            END
        ) AS total_promo_rate_2   -- Total promo rate for promo_bin_2
    FROM
        {{ source('retail', 'sales') }} AS sales
    GROUP BY
        DATE_TRUNC('week', sales.date)
)
SELECT
    sales_data.week_start AS date,         -- Weekly start date
    sales_data.target,                     -- Weekly aggregated sales
    sales_data.total_revenue AS revenue,   -- Weekly aggregated revenue
    sales_data.avg_stock AS stock,         -- Average stock over the week
    sales_data.total_promo_rate_1 AS total_promo_rate_1,  -- Weekly total promo rate for promo_bin_1
    sales_data.total_promo_rate_2 AS total_promo_rate_2   -- Weekly total promo rate for promo_bin_2
FROM
    sales_data
ORDER BY
    date
