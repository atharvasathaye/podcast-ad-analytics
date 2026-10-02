with campaigns as (
    select * from {{ ref('stg_campaigns') }}
)

select
    campaign_id,
    advertiser_id,
    campaign_name,
    budget,
    cpm_rate,
    {{ calculate_marketplace_cut('budget', '0.30') }} as marketplace_revenue,
    budget - {{ calculate_marketplace_cut('budget', '0.30') }} as creator_revenue_pool
from campaigns
