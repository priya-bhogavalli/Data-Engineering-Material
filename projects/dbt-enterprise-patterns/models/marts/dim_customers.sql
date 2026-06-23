-- Customer dimension. The lifetime_value / segment columns here are a dbt-native
-- equivalent of the gold.customer_ltv table built in ../lakehouse-medallion's
-- notebook 03 — same business logic, different execution engine (SQL/dbt vs PySpark),
-- deliberately, to show the same transformation expressed both ways.

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('fct_orders') }}
),

order_agg as (
    select
        customer_id,
        sum(order_amount)          as lifetime_value,
        count(*)                   as lifetime_orders,
        max(order_created_at)      as last_order_at,
        min(order_created_at)      as first_order_at
    from orders
    where status != 'cancelled'
    group by customer_id
),

final as (
    select
        customers.customer_id,
        customers.email,
        customers.country_code,
        customers.signup_at,
        coalesce(order_agg.lifetime_value, 0)   as lifetime_value,
        coalesce(order_agg.lifetime_orders, 0)  as lifetime_orders,
        order_agg.last_order_at,
        order_agg.first_order_at,
        datediff('day', order_agg.last_order_at, current_date()) as days_since_last_order,
        case
            when order_agg.last_order_at is null then 'never_ordered'
            when datediff('day', order_agg.last_order_at, current_date()) <= 30 then 'active'
            when datediff('day', order_agg.last_order_at, current_date()) <= 90 then 'at_risk'
            else 'churned'
        end as segment
    from customers
    left join order_agg on customers.customer_id = order_agg.customer_id
)

select * from final
