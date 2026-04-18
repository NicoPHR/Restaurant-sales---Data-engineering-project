with source_data as (

    -- Replace with your actual configured dbt source or ref
    select * from {{ source('raw_data','items') }}

),

cleaned_data as (

    select
        -- Core identifiers
        type,
        id,

        -- Sale Item Attributes
        attributes_canceled as is_canceled,
        attributes_cancellationComment as cancellation_comment,
        attributes_createdAt as created_at,
        attributes_price as price,
        attributes_quantity as quantity,
        attributes_status as status,
        attributes_paid as is_paid,

        -- Relationships
        relationships_sale_data_id as sale_id

        -- Excluded columns:
        -- attributes_comment (removed as per previous logic)
        -- relationships_priceList_data
        -- relationships_product_data_type
        -- relationships_product_data_id
        -- relationships_subitems_data
        -- relationships_sale_data_type
    from source_data

)

select * from cleaned_data