with source as (
    select * from {{ source('podcast_raw', 'advertisers') }}
),

renamed as (
    select
        advertiser_id,
        advertiser_name,
        industry
    from source
)

select * from renamed
