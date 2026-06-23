with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        region_id,
        status,
        currency,
        order_amount::decimal(18, 2)   as order_amount,
        order_created_at::timestamp    as order_created_at,
        order_updated_at::timestamp    as order_updated_at,
        _loaded_at
    from source
    -- drop rows synced from a lower environment / seed data that predates real launch —
    -- threshold is a var, not hardcoded, so staging stays correct if the cutoff changes
    where order_created_at::date >= '{{ var("min_valid_order_date") }}'
)

select * from renamed
