# Restaurant Sales - Data Engineering Project

This project aims to build a data engineering pipeline for restaurant sales data, leveraging modern tools like Terraform, Kestra, and Google Cloud Platform (GCP).

## Infrastructure with Terraform

Terraform is used to provision and manage the cloud infrastructure required for this project.

### What is being provisioned?

The Terraform configuration in the `Terraform/` directory manages the following GCP resources:
- **Google Cloud Storage (GCS) Bucket**: Acts as the Data Lake for storing raw and processed files.
- **BigQuery Dataset**: Serves as the Data Warehouse for structured data analysis.

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