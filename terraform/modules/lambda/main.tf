data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ── IAM role for Lambda ───────────────────────────────────────────────────────
resource "aws_iam_role" "lambda" {
  name = "${var.name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "vpc_access" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Allow Lambda to read secrets from Secrets Manager
resource "aws_iam_role_policy" "secrets" {
  name = "${var.name}-secrets-access"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:${var.name}/*"
    }]
  })
}

# ── Security group for Lambda → RDS ──────────────────────────────────────────
resource "aws_security_group" "lambda" {
  name        = "${var.name}-lambda-sg"
  description = "Lambda function security group"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.name}-lambda-sg" })
}

# ── Lambda function ───────────────────────────────────────────────────────────
resource "aws_lambda_function" "this" {
  function_name    = var.name
  description      = var.description
  role             = aws_iam_role.lambda.arn
  filename         = var.package_path
  source_code_hash = filebase64sha256(var.package_path)
  handler          = var.handler
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = var.environment_variables
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}
