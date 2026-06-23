-- Singular test: fails (returns rows) if any non-cancelled order has zero or negative
-- revenue. Schema-level tests (schema.yml) cover single-column checks; this is a
-- cross-column business-rule check that doesn't fit the generic test syntax — exactly
-- the case singular tests exist for.

select
    order_id,
    status,
    order_amount
from {{ ref('fct_orders') }}
where order_amount <= 0
  and status != 'cancelled'
