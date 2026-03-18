variable "state_bucket_name" {
  description = "S3 bucket name for Terraform remote state"
  type        = string
}

variable "state_bucket_force_destroy" {
  description = "Allow destroying non-empty state bucket"
  type        = bool
  default     = false
}

variable "lock_table_name" {
  description = "DynamoDB table name for Terraform state locks"
  type        = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
