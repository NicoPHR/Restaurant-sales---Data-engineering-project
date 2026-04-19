{{ config(
    materialized='table',
    partition_by={
      "field": "created_at",
      "data_type": "timestamp", 
      "granularity": "day"
    },
    cluster_by=['sale_type']
) }}

with sales as (
    select * from {{ ref('stg_sales_data') }} 
),

fact_sales_items as (
    select
        -- Core identifiers
        type,
        id,

        -- Timestamps
        closed_at,
        created_at,

        -- Sale attributes
        people_count,
        total_amount,
        sale_type,
        sale_state
    from sales

)

select * from fact_sales_items