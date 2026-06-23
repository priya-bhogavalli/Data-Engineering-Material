with source as (
    select * from {{ source('raw', 'order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        sku,
        quantity::int               as quantity,
        unit_price::decimal(18, 2)  as unit_price,
        (quantity::int * unit_price::decimal(18, 2)) as line_amount
    from source
    where quantity > 0
)

select * from renamed
