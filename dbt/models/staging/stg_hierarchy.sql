select
    *
from 
    {{ source('retail', 'product_hierarchy') }}
