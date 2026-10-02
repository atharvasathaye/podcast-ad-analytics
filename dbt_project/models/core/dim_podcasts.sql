with podcasts as (
    select * from {{ ref('stg_podcasts') }}
)

select
    podcast_id,
    podcast_name,
    {{ dbt_utils.generate_surrogate_key(['creator_name']) }} as creator_id,
    primary_genre,
    release_date,
    country
from podcasts
