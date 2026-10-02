with source as (
    select * from {{ source('podcast_raw', 'episodes') }}
),

renamed as (
    select
        episode_id,
        podcast_id,
        episode_title,
        cast(publish_date as timestamp) as publish_date,
        duration_seconds
    from source
)

select * from renamed
