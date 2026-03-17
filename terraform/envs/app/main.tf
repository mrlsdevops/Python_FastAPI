terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }

  # Backend config passed via -backend-config flags — no values committed.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

# ── Pull VPC outputs from the network state ───────────────────────────────────
# State bucket/key passed via -backend-config in workflow (GitHub Secrets).
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = var.network_state_bucket
    key    = var.network_state_key
    region = var.aws_region
  }
}

locals {
  vpc_id             = data.terraform_remote_state.network.outputs.vpc_id
  public_subnet_ids  = data.terraform_remote_state.network.outputs.public_subnet_ids
  private_subnet_ids = data.terraform_remote_state.network.outputs.private_subnet_ids

  tags = {
    Project     = var.project
    Environment = var.env
    ManagedBy   = "terraform"
    Pipeline    = "app"
  }
}

module "ecr" {
  source = "../../modules/ecr"

  name         = "${var.project}-${var.env}"
  force_delete = var.env != "prod"
  tags         = local.tags
}

module "eks" {
  source = "../../modules/eks"

  name                = "${var.project}-${var.env}"
  vpc_id              = local.vpc_id
  public_subnet_ids   = local.public_subnet_ids
  private_subnet_ids  = local.private_subnet_ids
  node_instance_types = var.node_instance_types
  node_desired        = var.node_desired
  node_min            = var.node_min
  node_max            = var.node_max
  tags                = local.tags
}

module "rds" {
  source = "../../modules/rds"

  name               = "${var.project}-${var.env}"
  vpc_id             = local.vpc_id
  private_subnet_ids = local.private_subnet_ids
  allowed_security_group_ids = [
    module.eks.node_security_group_id,
    module.lambda.lambda_security_group_id,
  ]
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  multi_az            = var.env == "prod"
  deletion_protection = var.env == "prod"
  tags                = local.tags
}

module "lambda" {
  source = "../../modules/lambda"

  name               = "${var.project}-${var.env}-login"
  description        = "Stateless login handler backed by RDS PostgreSQL"
  vpc_id             = local.vpc_id
  private_subnet_ids = local.private_subnet_ids
  package_path       = var.lambda_package_path

  environment_variables = {
    SECRET_NAME = "${var.project}/${var.env}/app-secrets"
    DB_HOST     = module.rds.db_host
    DB_PORT     = tostring(module.rds.db_port)
    DB_NAME     = var.db_name
    ENVIRONMENT = var.env
  }

  tags = local.tags
}

module "api_gateway" {
  source = "../../modules/api_gateway"

  name                 = "${var.project}-${var.env}-apigw"
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
  tags                 = local.tags
}
