with downloads as (
    select * from {{ ref('fct_downloads') }}
),
impressions as (
    select * from {{ ref('fct_ad_impressions') }}
),
campaigns as (
    select * from {{ ref('stg_campaigns') }}
)

select
    date_trunc(d.download_date, month) as activity_month,
    count(distinct d.download_id) as total_downloads,
    count(distinct i.impression_id) as total_impressions,
    safe_divide(count(distinct i.impression_id), count(distinct d.download_id)) as fill_rate,
    avg(c.cpm_rate) as average_cpm
from downloads d
left join impressions i on d.download_id = i.download_id
left join campaigns c on i.campaign_id = c.campaign_id
group by 1
