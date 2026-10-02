with source as (
    select * from {{ source('podcast_raw', 'podcasts') }}
),

renamed as (
    select
        podcast_id,
        podcast_name,
        creator_name,
        primary_genre,
        cast(release_date as timestamp) as release_date,
        country
    from source
)

select * from renamed
