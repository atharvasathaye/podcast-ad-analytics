with advertisers as (
    select * from {{ ref('stg_advertisers') }}
)

select
    advertiser_id,
    advertiser_name,
    industry
from advertisers
