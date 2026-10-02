-- Test: Impressions should never exceed downloads for a given episode
-- If this returns any rows, the test fails

with downloads as (
    select episode_id, count(download_id) as download_count
    from {{ ref('fct_downloads') }}
    group by 1
),
impressions as (
    select d.episode_id, count(i.impression_id) as impression_count
    from {{ ref('fct_ad_impressions') }} i
    join {{ ref('fct_downloads') }} d on i.download_id = d.download_id
    group by 1
)

select
    d.episode_id,
    d.download_count,
    i.impression_count
from downloads d
join impressions i on d.episode_id = i.episode_id
where i.impression_count > d.download_count
