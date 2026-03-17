variable "name" {
  description = "Name prefix for all VPC resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC — supply via TF_VAR_vpc_cidr secret, never commit"
  type        = string
  sensitive   = true
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets — supply via TF_VAR_public_subnet_cidrs secret"
  type        = list(string)
  sensitive   = true
}

variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets — supply via TF_VAR_private_subnet_cidrs secret"
  type        = list(string)
  sensitive   = true
}

variable "azs" {
  description = "Availability zones (same length as subnet CIDR lists)"
  type        = list(string)
}

variable "tags" {
  description = "Common tags applied to every resource"
  type        = map(string)
  default     = {}
}
