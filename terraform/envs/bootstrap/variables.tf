variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "env" {
  type = string
}

variable "state_bucket_name" {
  description = "Optional explicit S3 bucket name (overrides naming convention)"
  type        = string
  default     = null
}

variable "state_bucket_force_destroy" {
  description = "Allow destroying non-empty state bucket"
  type        = bool
  default     = false
}

variable "lock_table_name" {
  description = "Optional explicit DynamoDB table name (overrides naming convention)"
  type        = string
  default     = null
}
