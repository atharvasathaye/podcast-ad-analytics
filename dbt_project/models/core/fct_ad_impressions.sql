{{
    config(
        materialized='incremental',
        unique_key='impression_id',
        partition_by={
            "field": "impression_date",
            "data_type": "date",
            "granularity": "day"
        }
    )
}}

with impressions as (
    select * from {{ ref('stg_impressions') }}
)

select
    impression_id,
    download_id,
    campaign_id,
    impression_timestamp,
    cast(impression_timestamp as date) as impression_date
from impressions

{% if is_incremental() %}
  -- this filter will only be applied on an incremental run
  where impression_timestamp > (select max(impression_timestamp) from {{ this }})
{% endif %}
