output "state_bucket_name" {
  value = module.bootstrap.state_bucket_name
}

output "state_bucket_arn" {
  value = module.bootstrap.state_bucket_arn
}

output "lock_table_name" {
  value = module.bootstrap.lock_table_name
}

output "lock_table_arn" {
  value = module.bootstrap.lock_table_arn
}
