-- Test: Sum of payouts should not exceed the campaign budget
-- If this returns any rows, the test fails

with payouts as (
    select campaign_id, sum(amount) as total_payouts
    from {{ ref('fct_payouts') }}
    where status = 'paid'
    group by 1
),
campaigns as (
    select campaign_id, budget
    from {{ ref('stg_campaigns') }}
)

select
    p.campaign_id,
    p.total_payouts,
    c.budget
from payouts p
join campaigns c on p.campaign_id = c.campaign_id
where p.total_payouts > c.budget
