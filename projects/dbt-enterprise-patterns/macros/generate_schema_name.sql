{#
  Override dbt's default schema-naming behavior.

  Default dbt behavior concatenates the target schema and the custom schema
  (e.g. target schema `analytics` + custom schema `marts` -> `analytics_marts`),
  which means the same model lands in a different physical schema name depending on
  which environment ran it. That makes cross-environment debugging harder than it
  needs to be ("which schema is fct_orders actually in on staging?").

  This override makes the custom schema (set per-folder in dbt_project.yml, e.g.
  `staging`, `marts`) the schema name directly in every environment except CI, where
  keeping the env-specific suffix avoids collisions between concurrent CI runs sharing
  one database.
#}

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}

    {%- if target.name == 'ci' -%}
        {#- CI: keep dbt's default behavior so concurrent runs don't collide -#}
        {{ default_schema }}

    {%- elif custom_schema_name is none -%}
        {{ default_schema }}

    {%- else -%}
        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
