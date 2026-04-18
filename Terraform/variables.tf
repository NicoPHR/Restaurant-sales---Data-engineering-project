variable "credentials" {
  description = "My credentials"
  default     = "../my-creds.json"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "restaurant_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "restaurant-485023-terra-bucket"
}

variable "location" {
  description = "Project Location"
  default     = "US"
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
