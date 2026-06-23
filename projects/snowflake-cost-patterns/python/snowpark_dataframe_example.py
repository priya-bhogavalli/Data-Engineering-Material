"""
Snowpark DataFrame API — pushing transformation logic into Snowflake's query engine
instead of pulling data out to a client for processing.

The pattern this demonstrates: a monthly cohort-retention report that used to run as a
pandas job (full table pulled to a worker, processed in memory, written back) now runs
entirely inside Snowflake via lazy DataFrame operations. The Snowpark DataFrame API
builds a query plan and only executes it on .collect()/.to_pandas() — nothing is pulled
out of Snowflake until the final, already-aggregated result.

Why this mattered for cost: pulling a multi-billion-row fact table to a Python worker to
compute a cohort retention curve meant paying for both the Snowflake warehouse compute
*and* a separately-provisioned compute worker, plus the network transfer between them.
Pushing the whole computation into Snowpark means only the warehouse pays, and the result
that crosses the network is a few thousand rows, not billions.
"""

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, count_distinct, date_trunc, min as sf_min
from snowflake.snowpark.window import Window


def get_session(connection_params: dict) -> Session:
    return Session.builder.configs(connection_params).create()


def build_cohort_retention(session: Session, fact_table: str = "fact_orders"):
    """
    For each monthly signup cohort, compute what fraction of that cohort placed an
    order in each subsequent month. Everything here is a lazy DataFrame transformation
    — no data leaves Snowflake until build_cohort_retention(...).to_pandas() is called
    by the caller.
    """
    orders = session.table(fact_table)

    # first order per customer = their cohort month
    first_order_window = Window.partition_by(col("customer_id"))
    cohorts = (
        orders.with_column(
            "cohort_month", date_trunc("month", sf_min(col("order_date")).over(first_order_window))
        )
        .select("customer_id", "cohort_month")
        .distinct()
    )

    activity = orders.with_column(
        "activity_month", date_trunc("month", col("order_date"))
    ).select("customer_id", "activity_month")

    joined = cohorts.join(activity, on="customer_id")

    # months_since_signup as an integer offset, computed in-warehouse via DATEDIFF
    retention = (
        joined.with_column(
            "months_since_signup",
            (col("activity_month").cast("date") - col("cohort_month").cast("date")),
        )
        .group_by("cohort_month", "months_since_signup")
        .agg(count_distinct("customer_id").alias("active_customers"))
        .sort("cohort_month", "months_since_signup")
    )

    return retention


def cohort_size(session: Session, fact_table: str = "fact_orders"):
    """Denominator for retention % — customers per cohort month."""
    orders = session.table(fact_table)
    first_order_window = Window.partition_by(col("customer_id"))
    return (
        orders.with_column(
            "cohort_month", date_trunc("month", sf_min(col("order_date")).over(first_order_window))
        )
        .select("customer_id", "cohort_month")
        .distinct()
        .group_by("cohort_month")
        .agg(count_distinct("customer_id").alias("cohort_size"))
    )


if __name__ == "__main__":
    # connection_params would come from environment variables / a secrets manager in
    # any real deployment — never hardcode account credentials in the script.
    import os

    connection_params = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": "ANALYTICS_WRITER",
        "warehouse": "etl_batch_wh",
        "database": "ANALYTICS",
        "schema": "PUBLIC",
    }

    session = get_session(connection_params)

    retention_df = build_cohort_retention(session)
    sizes_df = cohort_size(session)

    # only this final, small, already-aggregated result is materialized client-side
    retention_pd = retention_df.to_pandas()
    sizes_pd = sizes_df.to_pandas()

    print(f"Cohort-month rows: {len(sizes_pd)}, retention curve rows: {len(retention_pd)}")

    session.close()
