WITH weekly_covariates AS (
    SELECT
        tts.item_id,  -- Unique identifier for product-store combination
        tts.date,     -- Weekly start date

        -- Aggregated metrics from the source sales table
        AVG(sales.stock) AS avg_stock,    -- Average weekly stock
        SUM(sales.revenue) AS total_revenue, -- Total weekly revenue
        AVG(sales.price) AS avg_price    -- Average weekly price

    FROM
        {{ ref('target_time_series') }} AS tts
    JOIN
        {{ source('retail', 'sales') }} AS sales
    ON
        CONCAT(sales.product_id, '-', sales.store_id) = tts.item_id
        AND DATE_TRUNC('week', sales.date) = tts.date
    GROUP BY
        tts.item_id,
        tts.date
)
SELECT
    tts.item_id,       -- Unique identifier for product-store combination
    tts.date,          -- Weekly start date
    tts.target,        -- Weekly aggregated sales (from target_time_series)
    
    -- Additional covariates
    weekly_covariates.avg_stock,    -- Average weekly stock
    weekly_covariates.total_revenue, -- Total weekly revenue
    weekly_covariates.avg_price     -- Average weekly price
FROM
    {{ ref('target_time_series') }} AS tts
JOIN
    weekly_covariates
ON
    tts.item_id = weekly_covariates.item_id
    AND tts.date = weekly_covariates.date
ORDER BY
    tts.item_id, tts.date
