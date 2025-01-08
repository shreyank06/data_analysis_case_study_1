-- Create the meta_data table
SELECT
    -- Generate the item_name by concatenating product_id and store_id
    CONCAT(sales.product_id, '-', sales.store_id) AS item_name,
    sales.date,
    sales.sales,
    sales.revenue,
    sales.stock,
    sales.price,
    
    -- Determine the applied promotion(s) based on the promo fields
    CASE
        WHEN sales.promo_type_1 IS NOT NULL AND sales.promo_type_2 IS NOT NULL THEN
            CONCAT(sales.promo_type_1, ', ', sales.promo_type_2)
        WHEN sales.promo_type_1 IS NOT NULL THEN
            sales.promo_type_1
        WHEN sales.promo_type_2 IS NOT NULL THEN
            sales.promo_type_2
        ELSE 'No Promotion'
    END AS promo_applied,

    -- Include discount information if applicable
    CASE
        WHEN sales.promo_type_2 IS NOT NULL THEN sales.promo_discount_2
        ELSE NULL
    END AS promo_discount,
    
    -- Dynamically determine and include only the highest relevant product hierarchy level
    CASE
        WHEN ph.hierarchy5_id IS NOT NULL THEN ph.hierarchy5_id
        WHEN ph.hierarchy4_id IS NOT NULL THEN ph.hierarchy4_id
        WHEN ph.hierarchy3_id IS NOT NULL THEN ph.hierarchy3_id
        WHEN ph.hierarchy2_id IS NOT NULL THEN ph.hierarchy2_id
        WHEN ph.hierarchy1_id IS NOT NULL THEN ph.hierarchy1_id
        ELSE NULL
    END AS hierarchy_id,

    -- Include product dimensions
    ph.product_length,
    ph.product_width,
    ph.product_depth,

    -- Include store details
    stores.store_id,
    stores.storetype_id,
    stores.store_size,
    stores.city_id

FROM
    {{ source('retail', 'sales') }} AS sales
JOIN
    {{ source('retail', 'product_hierarchy') }} AS ph
ON
    sales.product_id = ph.product_id
JOIN
    {{ source('retail', 'store_cities') }} AS stores
ON
    sales.store_id = stores.store_id
