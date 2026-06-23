-- Rolls line items up to one row per order_id before fct_orders joins against it.
-- Kept as a separate (ephemeral) model rather than inlined into fct_orders so the
-- aggregation logic is unit-testable and reusable if another mart ever needs the same
-- per-order line-item rollup.

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

aggregated as (
    select
        order_id,
        count(*)                       as line_item_count,
        sum(quantity)                  as total_quantity,
        sum(line_amount)               as line_items_total
    from order_items
    group by order_id
)

select * from aggregated
