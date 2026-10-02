with source as (
    select * from {{ source('podcast_raw', 'payouts') }}
),

renamed as (
    select
        payout_id,
        campaign_id,
        podcast_id,
        amount,
        cast(payout_date as timestamp) as payout_date,
        status
    from source
)

select * from renamed
