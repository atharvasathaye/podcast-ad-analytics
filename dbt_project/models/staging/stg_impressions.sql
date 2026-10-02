with source as (
    select * from {{ source('podcast_raw', 'impressions') }}
),

renamed as (
    select
        impression_id,
        download_id,
        campaign_id,
        cast(impression_timestamp as timestamp) as impression_timestamp
    from source
)

select * from renamed
