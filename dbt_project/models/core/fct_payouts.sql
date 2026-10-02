with payouts as (
    select * from {{ ref('stg_payouts') }}
)

select
    payout_id,
    campaign_id,
    podcast_id,
    amount,
    payout_date,
    status
from payouts
