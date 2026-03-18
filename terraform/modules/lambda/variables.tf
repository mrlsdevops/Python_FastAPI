variable "name" {
  type = string
}

variable "description" {
  type    = string
  default = ""
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "package_path" {
  description = "Path to the Lambda zip package"
  type        = string
}

variable "handler" {
  type    = string
  default = "login_handler.handler"
}

variable "runtime" {
  type    = string
  default = "python3.12"
}

variable "timeout" {
  type    = number
  default = 30
}

variable "memory_size" {
  type    = number
  default = 256
}

variable "environment_variables" {
  description = "Non-secret env vars; secrets are pulled from Secrets Manager at runtime"
  type        = map(string)
  default     = {}
}

variable "tags" {
  type    = map(string)
  default = {}
}
