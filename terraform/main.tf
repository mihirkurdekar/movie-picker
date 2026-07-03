terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/lambda.zip"

  excludes = [
    "test",
    "scripts",
    "terraform",
    ".git",
    ".gitignore",
    ".env",
    ".env.local",
    "README.md",
    "SPEC.md",
    "deploy.sh",
    "*.log",
    "npm-debug.log",
    ".DS_Store",
  ]
}

resource "aws_iam_role" "lambda_exec" {
  name = var.role_name

  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "movie_picker" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_exec.arn
  handler       = var.handler
  runtime       = var.runtime
  timeout       = 30
  memory_size   = 512

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      GEMINI_API_KEY = var.gemini_api_key
      OPENROUTER_API_KEY = var.openrouter_api_key
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function_url" "movie_picker" {
  function_name      = aws_lambda_function.movie_picker.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = var.allowed_origins
    allow_methods = ["GET", "POST"]
    allow_headers = ["Content-Type"]
  }
}

output "api_url" {
  value = aws_lambda_function_url.movie_picker.function_url
}