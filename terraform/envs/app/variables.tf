variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "env" {
  type = string
}

# ── Remote state references (passed as GitHub Secrets) ───────────────────────
variable "network_state_bucket" {
  description = "S3 bucket holding the network Terraform state"
  type        = string
  sensitive   = true
}

variable "network_state_key" {
  description = "S3 key for the network state file"
  type        = string
  sensitive   = true
}

# ── EKS ───────────────────────────────────────────────────────────────────────
variable "node_instance_types" {
  type    = list(string)
  default = ["t3.small"]
}

variable "node_desired" {
  type    = number
  default = 2
}

variable "node_min" {
  type    = number
  default = 1
}

variable "node_max" {
  type    = number
  default = 3
}

# ── RDS ───────────────────────────────────────────────────────────────────────
variable "db_name" {
  type      = string
  sensitive = true
}

variable "db_username" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}

# ── Lambda ────────────────────────────────────────────────────────────────────
variable "lambda_package_path" {
  description = "Local path to the Lambda zip; overridden by CI after packaging"
  type        = string
  default     = "../../../lambda/login.zip"
}
