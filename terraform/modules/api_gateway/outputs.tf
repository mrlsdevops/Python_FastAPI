output "api_id" {
  value = aws_apigatewayv2_api.this.id
}

output "invoke_url" {
  description = "Base URL for the HTTP API  — POST /login goes to: <invoke_url>/login"
  value       = aws_apigatewayv2_stage.default.invoke_url
}
