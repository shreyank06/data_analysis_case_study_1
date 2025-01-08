select
    *
from 
    {{ source('retail', 'sales') }}
