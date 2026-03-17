variable "name" {
  type = string
}

variable "force_delete" {
  description = "Allow deleting the repository even if it contains images"
  type        = bool
  default     = false
}

variable "tags" {
  type    = map(string)
  default = {}
}
