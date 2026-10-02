with source as (
    select * from {{ source('podcast_raw', 'downloads') }}
),

deduped as (
    select
        download_id,
        episode_id,
        listener_id,
        cast(download_timestamp as timestamp) as download_timestamp,
        user_agent,
        country,
        -- Deduplicate based on download_id, keeping the latest if any difference
        row_number() over (partition by download_id order by download_timestamp desc) as rn
    from source
)

select 
    download_id,
    episode_id,
    listener_id,
    download_timestamp,
    user_agent,
    country
from deduped
where rn = 1
