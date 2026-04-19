{{ config(
    materialized='table',
    partition_by={
      "field": "sale_created_at",
      "data_type": "timestamp", 
      "granularity": "day"
    },
    cluster_by=['sale_id']
) }}

with items as (
    select * from {{ ref('stg_items_data') }} 
),

sales as (
    select * from {{ ref('stg_sales_data') }} 
),

fact_sales_items as (

    select
        -- Primary Key for the grain of this table
        items.id as sale_item_id,
        
        -- Foreign Keys/Identifiers
        items.sale_id,
        
        -- Item Specifics
        items.type as item_type,
        items.status as item_status,
        items.price as unit_price,
        items.quantity,
        (items.price * items.quantity) as line_item_total,
        items.is_canceled,
        items.is_paid,
        items.cancellation_comment,

        -- Sale Context
        sales.sale_type,
        sales.sale_state,
        sales.people_count,
        sales.total_amount as sale_total_amount,
        
        -- Timestamps
        items.created_at as item_created_at,
        sales.created_at as sale_created_at,
        sales.closed_at as sale_closed_at

    from items
    left join sales 
        on items.sale_id = sales.id

)

select * from fact_sales_items