# Restaurant Sales - Data Engineering Project

## Problem Statement

In the restaurant industry, operational efficiency and timing are critical. Currently, the client generates valuable daily transaction data across multiple channels (dine-in and delivery) but lacks a centralized, automated system to analyze it. Without clear visibility into these metrics, management is forced to make critical business decisions based on intuition rather than empirical evidence.

This data engineering project solves this gap by building an automated, end-to-end pipeline that extracts daily sales data directly from the restaurant's API, structures it, and prepares it for business intelligence reporting. 

By transforming raw JSON responses into a clean, dimensional data model, the project empowers the restaurant to drive continuous improvement across several key areas:

* **Demand Forecasting & Staffing:** Identifying peak sales days and times to optimize employee schedules, ensuring adequate coverage during rushes while minimizing idle labor costs.
* **Inventory Control:** Tracking item-level sales trends to predict how much stock is needed, reducing food waste and preventing stockouts.
* **Performance Monitoring:** Providing a clear, daily pulse on overall business health (revenue growth vs. decline) to evaluate the success of marketing efforts and operational changes.

Ultimately, this project delivers a robust, low-maintenance data architecture designed to eventually be handed over to the client, providing them with a permanent, self-sustaining system for making data-driven decisions.

# Steps followed in the project
In the following section I will describe what has been done in the project.
We will go through the technology applied and the steps followed to build the pipeline.

**This project is not replicable as it manages real sales data.**
## 1) Infrastructure with Terraform

Terraform is used to provision and manage the cloud infrastructure required for this project.

### What is being provisioned?

The Terraform configuration in the `Terraform/` directory manages the following GCP resources:
- **Google Cloud Storage (GCS) Bucket**: Acts as the Data Lake for storing raw and processed files.
- **BigQuery Dataset**: Serves as the Data Warehouse for structured data analysis. Here we have the raw data, staging tables and final tables.

### Prerequisites

1.  Ensure you have the [Terraform CLI](https://developer.hashicorp.com/terraform/downloads) installed.
2.  Have a GCP Service Account with the necessary permissions (Storage Admin, BigQuery Admin, etc.).
3.  Place your service account key file at `my-creds.json` in the root of the project (referenced as `../my-creds.json` from the Terraform directory).

### How to manage the Infrastructure

Navigate to the Terraform directory:
```bash
cd Terraform
```

#### 1. Initialize Terraform
Downloads the necessary providers (Google Cloud provider).
```bash
terraform init
```

#### 2. Create the Infrastructure
Apply the configuration to create the bucket and dataset.
```bash
terraform apply
```
*You will be prompted to confirm the action. Type `yes` to proceed.*

#### 3. Delete the Infrastructure
Removes all resources managed by Terraform.
```bash
terraform destroy
```

> [!CAUTION]
> **WARNING**: Running `terraform destroy` will permanently delete the GCS bucket (including all stored data) and the BigQuery dataset. This action is irreversible. Use with extreme caution!

*(Note: The flow used in terraform can be found in the `Terraform/` directory of this repository).*

## 2) Data ingestion and orchestration with Kestra

To automate the daily flow of data, this project uses **Kestra** as the core orchestration engine. A scheduled flow runs once a day, ensuring the data warehouse is consistently updated with the previous day's transactions without any manual intervention.

The automated ingestion pipeline executes the following sequence:

1. **API Extraction:** A Python task authenticates and queries the restaurant's sales API, pulling the raw transaction and item data for the preceding day.
2. **Cloud Storage (Data Lake):** The raw JSON response is immediately saved into a Google Cloud Storage (GCS) bucket. This preserves an exact, unmodified record of the API response for backup, historical auditing, and data recovery.
3. **Data Flattening:** Because the API returns nested JSON, a processing task uses the `pandas` library to parse, clean, and flatten the complex structures into separate, tabular formats.
4. **BigQuery Loading (Raw Layer):** Finally, the flattened data is loaded directly into Google BigQuery. This step populates two distinct raw tables—`sales` and `items`—acting as the foundational "Bronze Layer" for downstream transformations.

*(Note: The flow used in kestra can be found in the `kestra/` directory of this repository).*

## 3) Data Transformation (dbt)

Once the raw data is securely loaded into BigQuery, **dbt (data build tool)** takes over to handle the "Transform" phase of the pipeline. A daily automated job running on dbt Cloud executes a series of SQL-based transformations to clean, model, and aggregate the data.

This project strictly follows the **Kimball dimensional modeling methodology** to structure the data for analytical querying. The dbt pipeline performs the following steps:

1. **Staging:** Reads the raw "Bronze" tables from BigQuery and standardizes column names, data types, and core identifiers.
2. **Fact Tables:** Joins the normalized staging models to create a central, granular record of business events (e.g., individual sale items).
3. **Reporting Marts:** Rolls up the granular fact data into a specialized, highly aggregated reporting table (Data Mart) designed specifically for fast dashboard ingestion.

**Performance Optimization (Partitioning & Clustering)**
To ensure the pipeline is highly efficient and cost-effective, the final tables materialized in BigQuery are explicitly **partitioned** by date and **clustered** by key dimensional attributes (like sale IDs or item types). This architecture drastically reduces the amount of data scanned during queries, ensuring high performance when the data is eventually connected to a BI dashboard.

*(Note: All of the SQL transformation logic and configuration blocks can be found in the `models/` directory of this repository).*


