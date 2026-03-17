output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_host" {
  value = module.rds.db_host
}

output "api_gateway_url" {
  description = "Base URL for the Lambda-backed auth API"
  value       = module.api_gateway.invoke_url
}
