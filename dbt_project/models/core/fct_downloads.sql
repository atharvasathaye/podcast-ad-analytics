with downloads as (
    select * from {{ ref('stg_downloads') }}
)

select
    download_id,
    episode_id,
    listener_id,
    download_timestamp,
    cast(download_timestamp as date) as download_date,
    user_agent,
    country
from downloads
