{% snapshot creator_rate_cards_snapshot %}

{{
    config(
      target_schema='podcast_snapshots',
      unique_key='creator_id',
      strategy='check',
      check_cols=['cpm_rate_preference']
    )
}}

-- Simulating a source table for creator rate cards
select
    {{ dbt_utils.generate_surrogate_key(['creator_name']) }} as creator_id,
    creator_name,
    -- Random CPM preference between 15 and 40
    25.0 as cpm_rate_preference
from {{ source('podcast_raw', 'podcasts') }}
group by 1, 2

{% endsnapshot %}
