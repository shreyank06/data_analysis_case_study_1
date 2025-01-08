-- Replace with proper data preprocessing
-- select
    -- 1 as item_id,
    -- make_date(2024, 12, 30) as date,
    -- 20 as target
WITH weekly_sales AS (
    SELECT
        CONCAT(sales.product_id, '-', sales.store_id) AS item_id, -- Unique identifier per product-store
        DATE_TRUNC('week', sales.date) AS week_start, -- Start of the week
        SUM(sales.sales) AS target -- Weekly aggregated sales
    FROM
        {{ source('retail', 'sales') }} AS sales
    GROUP BY
        CONCAT(sales.product_id, '-', sales.store_id),
        DATE_TRUNC('week', sales.date)
)
SELECT
    item_id, -- Unique identifier for product-store combination
    week_start AS date, -- Weekly start date
    target -- Weekly aggregated sales
FROM
    weekly_sales
