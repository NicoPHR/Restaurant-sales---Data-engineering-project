variable "credentials" {
  description = "My credentials"
  default     = "../my-creds.json"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "restaurant_dataset"
}

variable "bq_dbt_dataset_name" {
  description = "The dataset where dbt will store transformed models"
  default     = "dbt_restaurant"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "restaurant-485023-terra-bucket"
}

variable "location" {
  description = "Project Location"
  default     = "us-central1"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "project" {
  description = "Project"
  default     = "radiant-galaxy-491121-e0"
}

variable "region" {
  description = "region"
  default     = "us-central1"
}
