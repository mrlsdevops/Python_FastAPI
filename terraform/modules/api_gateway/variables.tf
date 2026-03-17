variable "name" {
  type = string
}

variable "description" {
  type    = string
  default = "FastAPI auth endpoint"
}

variable "lambda_invoke_arn" {
  type = string
}

variable "lambda_function_name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
