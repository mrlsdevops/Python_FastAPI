terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Intentionally local backend for one-time bootstrap.
  # This avoids circular dependency when creating the remote backend itself.
  backend "local" {}
}

provider "aws" {
  region = var.aws_region
}

module "bootstrap" {
  source = "../../modules/bootstrap"

  state_bucket_name          = local.state_bucket_name
  state_bucket_force_destroy = var.state_bucket_force_destroy
  lock_table_name            = local.lock_table_name

  tags = local.tags
}

locals {
  state_bucket_name = coalesce(var.state_bucket_name, "${var.project}-${var.env}-tf-state")
  lock_table_name   = coalesce(var.lock_table_name, "${var.project}-${var.env}-tf-locks")

  tags = {
    Project     = var.project
    Environment = var.env
    ManagedBy   = "terraform"
    Pipeline    = "bootstrap"
  }
}
