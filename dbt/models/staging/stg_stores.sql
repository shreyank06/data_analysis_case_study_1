select
    *
from 
    {{ source('retail', 'store_cities') }}
