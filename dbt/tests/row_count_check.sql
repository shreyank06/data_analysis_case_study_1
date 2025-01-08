SELECT
    CASE
        WHEN (SELECT COUNT(*) FROM {{ ref('target_time_series') }}) =
             (SELECT COUNT(*) FROM {{ ref('per_item_covariates') }})
        THEN 'PASS'
        ELSE 'FAIL'
    END AS result
