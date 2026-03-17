terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend config is passed via -backend-config flags in the workflow.
  # No bucket names, keys, or regions are hardcoded here.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "../../modules/vpc"

  name                 = "${var.project}-${var.env}"
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  azs                  = var.azs

  tags = local.tags
}

locals {
  tags = {
    Project     = var.project
    Environment = var.env
    ManagedBy   = "terraform"
    Pipeline    = "network"
  }
}
