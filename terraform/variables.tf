variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "source_dir" {
  description = "Path to the built Lambda source directory (includes backend + frontend/dist)"
  type        = string
  default     = "../.lambda-build"
}

variable "role_name" {
  description = "Name of the IAM role used by the Lambda function"
  type        = string
  default     = "movie-picker-lambda-role"
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "movie-picker"
}

variable "handler" {
  description = "Lambda handler entrypoint"
  type        = string
  default     = "app.lambda_handler"
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.12"
}

variable "gemini_api_key" {
  description = "Gemini API key for the Lambda environment (deprecated - kept for backward compatibility)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "openrouter_api_key" {
  description = "OpenRouter API key for the Lambda environment"
  type        = string
  sensitive   = true
}

variable "allowed_origins" {
  description = "Allowed CORS origins for the Lambda Function URL"
  type        = list(string)
  default     = ["*"]
}