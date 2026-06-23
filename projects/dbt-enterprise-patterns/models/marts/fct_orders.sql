-- Order-grain fact table. This is the table referenced as fact_orders throughout
-- ../snowflake-cost-patterns — the clustering, materialization, and profiling work
-- documented there is the cost story for what this model builds.

with orders as (
    select * from {{ ref('stg_orders') }}
),

item_rollup as (
    select * from {{ ref('int_order_items_aggregated') }}
),

final as (
    select
        orders.order_id,
        orders.customer_id,
        orders.region_id,
        orders.status,
        orders.currency,
        orders.order_amount,
        orders.order_created_at,
        orders.order_updated_at,
        coalesce(item_rollup.line_item_count, 0)   as line_item_count,
        coalesce(item_rollup.total_quantity, 0)     as total_quantity,
        -- order_amount is the source of truth for revenue reporting (it's what the
        -- order was actually charged); line_items_total is kept alongside it purely
        -- as a reconciliation signal — a gap between the two usually means a discount,
        -- a partial refund, or a data-quality issue upstream, not a number to "fix" by
        -- picking whichever is more convenient.
        item_rollup.line_items_total,
        (orders.order_amount - coalesce(item_rollup.line_items_total, 0))
            as amount_vs_line_items_variance
    from orders
    left join item_rollup on orders.order_id = item_rollup.order_id
)

select * from final
