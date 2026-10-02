with podcasts as (
    select * from {{ ref('stg_podcasts') }}
)

-- Simulate a dimension table for creators
select distinct
    {{ dbt_utils.generate_surrogate_key(['creator_name']) }} as creator_id,
    creator_name
from podcasts
where creator_name is not null
