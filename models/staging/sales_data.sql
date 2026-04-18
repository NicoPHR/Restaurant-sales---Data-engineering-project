with source_data as (
    select * from {{ source('raw_data','sales') }}
),

cleaned_data as (

    select
        -- Core identifiers
        type,
        id,

        -- Timestamps
        attributes_closedAt as closed_at,
        attributes_createdAt as created_at,

        -- Sale attributes
        attributes_people as people_count,
        attributes_total as total_amount,
        attributes_saleType as sale_type,
        attributes_saleState as sale_state,
        attributes_expectedPayments as expected_payments

        -- Excluded columns:
        -- attributes_comment
        -- attributes_customerName
        -- attributes_anonymousCustomer_name
        -- attributes_anonymousCustomer_phone
        -- attributes_anonymousCustomer_address
        -- attributes_anonymousCustomer
    from source_data

)

select * from cleaned_data