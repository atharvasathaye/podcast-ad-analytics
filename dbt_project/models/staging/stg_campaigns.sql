with source as (
    select * from {{ source('podcast_raw', 'campaigns') }}
),

renamed as (
    select
        campaign_id,
        advertiser_id,
        campaign_name,
        cast(start_date as timestamp) as start_date,
        cast(end_date as timestamp) as end_date,
        budget,
        cpm_rate
    from source
)

select * from renamed
