with campaigns as (
    select * from {{ ref('int_revenue_share') }}
),
impressions as (
    select * from {{ ref('fct_ad_impressions') }}
),
campaign_dates as (
    select * from {{ ref('stg_campaigns') }}
)

select
    c.campaign_id,
    c.campaign_name,
    c.advertiser_id,
    c.budget as booked_budget,
    c.cpm_rate,
    count(i.impression_id) as total_impressions_delivered,
    (count(i.impression_id) / 1000.0) * c.cpm_rate as delivered_value,
    case
        when current_date() > cast(cd.end_date as date) then 'Completed'
        when current_date() between cast(cd.start_date as date) and cast(cd.end_date as date) then 'Active'
        else 'Planned'
    end as campaign_status
from campaigns c
join campaign_dates cd on c.campaign_id = cd.campaign_id
left join impressions i on c.campaign_id = i.campaign_id
group by 1, 2, 3, 4, 5, cd.start_date, cd.end_date
