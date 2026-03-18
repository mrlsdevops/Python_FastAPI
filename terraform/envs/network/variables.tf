variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "env" {
  type = string
}

# ── Network variables — NO DEFAULTS intentionally ────────────────────────────
# All values must be supplied via GitHub Secrets (TF_VAR_*).
# Never commit real CIDR blocks to the repository.

variable "vpc_cidr" {
  type      = string
  sensitive = true
}

variable "public_subnet_cidrs" {
  type      = list(string)
  sensitive = true
}

variable "private_subnet_cidrs" {
  type      = list(string)
  sensitive = true
}

variable "azs" {
  description = "Availability zones — e.g. [\"us-east-1a\",\"us-east-1b\"]"
  type        = list(string)
}
