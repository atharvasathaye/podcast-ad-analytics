with payouts as (
    select * from {{ ref('fct_payouts') }}
),
podcasts as (
    select * from {{ ref('dim_podcasts') }}
),
creators as (
    select * from {{ ref('dim_creators') }}
),
campaigns as (
    select * from {{ ref('int_revenue_share') }}
),
advertisers as (
    select * from {{ ref('dim_advertisers') }}
)

select
    date_trunc(cast(p.payout_date as date), month) as revenue_month,
    a.advertiser_name,
    c.creator_name,
    sum(p.amount) as creator_revenue,
    sum(camp.marketplace_revenue) / count(distinct p.payout_id) as estimated_marketplace_revenue
from payouts p
join podcasts pod on p.podcast_id = pod.podcast_id
join creators c on pod.creator_id = c.creator_id
join campaigns camp on p.campaign_id = camp.campaign_id
join advertisers a on camp.advertiser_id = a.advertiser_id
where p.status = 'paid'
group by 1, 2, 3
