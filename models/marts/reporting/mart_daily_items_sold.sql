{{ config(
    materialized='table',
    partition_by={
      "field": "sale_date",
      "data_type": "date", 
      "granularity": "day"
    },
    cluster_by=['item_type']
) }}

with fact_sales as (
    -- Make sure this ref matches the exact file name of your fact table
    select * from {{ ref('fct_sale_items') }} 
),

daily_aggregates as (
    select
        -- Convert the timestamp to a standard Date for clean partitioning
        date(sale_created_at) as sale_date,
        
        -- Including a dimension like item_type makes clustering useful
        item_type,
        
        -- Metrics
        sum(quantity) as total_items_sold,
        sum(line_item_total) as total_revenue,
        count(sale_item_id) as total_line_items

    from fact_sales
    -- It is best practice to exclude canceled items from "sold" metrics
    where is_canceled = false 
       or is_canceled is null
       
    group by 
        sale_date,
        item_type
)

select * from daily_aggregates