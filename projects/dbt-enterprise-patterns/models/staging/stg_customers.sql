with source as (
    select * from {{ source('raw', 'customers') }}
),

renamed as (
    select
        customer_id,
        email,
        country_code,
        signup_at::timestamp as signup_at,
        _loaded_at
    from source
    where customer_id is not null
)

select * from renamed
