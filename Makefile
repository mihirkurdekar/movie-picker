# -------------------------------------------------
# Makefile - Movie Picker Full Project Management
# -------------------------------------------------

# Directories
PROJECT_ROOT := $(shell pwd)
FRONTEND_DIR := frontend
BACKEND_DIR := backend
TERRAFORM_DIR := terraform
LAMBDA_BUILD_DIR := .lambda-build

# AWS Configuration
AWS_REGION ?= us-east-1
LAMBDA_FUNCTION_NAME ?= movie-picker

# Environment Variables (set these in your shell or .env)
OPENROUTER_API_KEY ?= $(shell grep -m1 "OPENROUTER_API_KEY" .env 2>/dev/null | cut -d= -f2 || echo "")
GEMINI_API_KEY ?= $(shell grep -m1 "GEMINI_API_KEY" .env 2>/dev/null | cut -d= -f2 || echo "")

# -------------------------------------------------
# Development Targets
# -------------------------------------------------
## dev       : Start both frontend (React/Vite) and backend (Python) servers
dev:
	@echo "🚀 Starting frontend development server..."
	@cd $(FRONTEND_DIR) && npm run dev &
	@echo "🐍 Starting backend development server..."
	@cd $(BACKEND_DIR) && poetry install --no-root && poetry run python src/local_server.py &
	@echo "✅ Development servers started in background."
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend API: http://localhost:8080/movie"
	@echo "   Press Ctrl+C to stop both."
	@wait

## dev-frontend  : Start only frontend development server
dev-frontend:
	@cd $(FRONTEND_DIR) && npm run dev

## dev-backend   : Start only backend development server
dev-backend:
	@cd $(BACKEND_DIR) && poetry install --no-root && poetry run python src/local_server.py

# -------------------------------------------------
# Build Targets
# -------------------------------------------------
## build      : Build everything for production
build: build-frontend build-backend build-lambda
	@echo "✅ Production build complete!"

## build-frontend : Build frontend for production
build-frontend:
	@echo "📦 Building frontend..."
	@cd $(FRONTEND_DIR) && npm ci --silent && npm run build

## build-backend  : Install backend dependencies
build-backend:
	@echo "📦 Installing backend dependencies..."
	@cd $(BACKEND_DIR) && poetry install --no-root

## build-lambda   : Package Lambda function for deployment
build-lambda:
	@echo "🧱 Building Lambda package..."
	@rm -rf $(LAMBDA_BUILD_DIR)
	@mkdir -p $(LAMBDA_BUILD_DIR)/frontend/dist
	@mkdir -p $(LAMBDA_BUILD_DIR)/src
	@cp -R backend/src/. $(LAMBDA_BUILD_DIR)/src/
	@cp -R frontend/dist/. $(LAMBDA_BUILD_DIR)/frontend/dist/
	@cd $(BACKEND_DIR) && pip3 install -r requirements.txt -t $(PWD)/$(LAMBDA_BUILD_DIR)/src
	@echo "✅ Lambda package ready in $(LAMBDA_BUILD_DIR)/"

# -------------------------------------------------
# Deployment Targets
# -------------------------------------------------
## deploy    : Build and deploy to AWS Lambda
deploy: build-lambda
	@echo "🚀 Deploying to AWS Lambda..."
	@cd $(TERRAFORM_DIR) && \
	terraform init -input=false && \
	terraform apply -auto-approve \
		-var="openrouter_api_key=$(OPENROUTER_API_KEY)" \
		-var="gemini_api_key=$(GEMINI_API_KEY)" \
		-var="aws_region=$(AWS_REGION)"
	@echo "✅ Deployment complete!"
	@echo "   Function URL: $$(cd $(TERRAFORM_DIR) && terraform output -raw api_url 2>/dev/null || echo 'Check terraform output')"

## destroy   : Remove all deployed AWS resources
destroy:
	@echo "🗑️  Destroying AWS resources..."
	@cd $(TERRAFORM_DIR) && \
	terraform destroy -auto-approve \
		-var="openrouter_api_key=$(OPENROUTER_API_KEY)" \
		-var="gemini_api_key=$(GEMINI_API_KEY)" \
		-var="aws_region=$(AWS_REGION)"
	@echo "✅ Resources destroyed."

## refresh   : Update Lambda code without changing infrastructure
refresh: build-lambda
	@echo "🔄 Updating Lambda code..."
	@cd $(TERRAFORM_DIR) && \
	terraform apply -auto-approve \
		-var="openrouter_api_key=$(OPENROUTER_API_KEY)" \
		-var="gemini_api_key=$(GEMINI_API_KEY)" \
		-var="aws_region=$(AWS_REGION)" \
		-refresh-only
	@echo "✅ Lambda code updated."

# -------------------------------------------------
# Testing Targets
# -------------------------------------------------
## test      : Test the deployed Lambda endpoint
test:
	@echo "🌐 Testing deployed Lambda endpoint..."
	@API_URL=$$(cd $(TERRAFORM_DIR) && terraform output -raw api_url 2>/dev/null) && \
	if [ -z "$$API_URL" ]; then \
		echo "❌ No API URL found. Run 'make deploy' first."; \
		exit 1; \
	fi && \
	curl -s -X POST "$$API_URL/movie" \
	  -H "Content-Type: application/json" \
	  -d '{"category":"bollywood","difficulty":"easy","exclude":[]}' | jq .

## test-local: Test local backend endpoint
test-local:
	@echo "🔍 Testing local backend endpoint..."
	@curl -s -X POST http://localhost:8080/movie \
	      -H "Content-Type: application/json" \
	      -d '{"category":"bollywood","difficulty":"easy","exclude":[]}' | jq .

# -------------------------------------------------
# State Management Targets
# -------------------------------------------------
## init     : Initialize Terraform and import existing resources
init:
	@echo "🔧 Initializing Terraform state..."
	@cd $(TERRAFORM_DIR) && terraform init
	@terraform import -var="openrouter_api_key=$(OPENROUTER_API_KEY)" -var="gemini_api_key=$(GEMINI_API_KEY)" aws_iam_role.lambda_exec $(LAMBDA_FUNCTION_NAME)-lambda-role
	@terraform import -var="openrouter_api_key=$(OPENROUTER_API_KEY)" -var="gemini_api_key=$(GEMINI_API_KEY)" aws_lambda_function.movie_picker $(LAMBDA_FUNCTION_NAME)
	@terraform import -var="openrouter_api_key=$(OPENROUTER_API_KEY)" -var="gemini_api_key=$(GEMINI_API_KEY)" aws_lambda_function_url.movie_picker $(LAMBDA_FUNCTION_NAME)
	@echo "✅ Terraform state initialized."

## state-pull: Pull current Terraform state
state-pull:
	@cd $(TERRAFORM_DIR) && terraform state pull > terraform.tfstate
	@echo "✅ State saved to $(TERRAFORM_DIR)/terraform.tfstate"

# -------------------------------------------------
# Utility Targets
# -------------------------------------------------
## clean     : Remove all build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(LAMBDA_BUILD_DIR)
	@rm -rf $(FRONTEND_DIR)/node_modules $(FRONTEND_DIR)/.vite $(FRONTEND_DIR)/dist
	@rm -rf $(BACKEND_DIR)/.python_backend_backend
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete."

## env       : Install all dependencies
env:
	@echo "📦 Installing dependencies..."
	@cd $(FRONTEND_DIR) && npm install
	@cd $(BACKEND_DIR) && poetry install
	@echo "✅ Dependencies installed."

## logs      : Stream Lambda logs (requires AWS CLI)
logs:
	@echo "📋 Streaming Lambda logs..."
	@aws logs tail /aws/lambda/$(LAMBDA_FUNCTION_NAME) --follow --region $(AWS_REGION)

## help      : Show all available make commands
help:
	@echo "Movie Picker - Available make targets:"
	@echo ""
	@echo "🚀 Development:"
	@echo "  make dev           - Start frontend and backend dev servers"
	@echo "  make dev-frontend  - Start only frontend server"
	@echo "  make dev-backend   - Start only backend server"
	@echo ""
	@echo "🔨 Build:"
	@echo "  make build         - Build everything for production"
	@echo "  make build-frontend- Build frontend only"
	@echo "  make build-backend - Install backend dependencies"
	@echo "  make build-lambda  - Package Lambda function"
	@echo ""
	@echo "📤 Deployment:"
	@echo "  make deploy        - Build and deploy to AWS Lambda"
	@echo "  make destroy       - Remove all AWS resources"
	@echo "  make refresh       - Update Lambda code only"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test          - Test deployed Lambda endpoint"
	@echo "  make test-local    - Test local backend endpoint"
	@echo ""
	@echo "⚙️  State Management:"
	@echo "  make init          - Initialize Terraform and import resources"
	@echo "  make state-pull    - Pull Terraform state to file"
	@echo ""
	@echo "🧹 Utilities:"
	@echo "  make clean         - Remove all build artifacts"
	@echo "  make env           - Install all dependencies"
	@echo "  make logs          - Stream Lambda logs"
	@echo "  make help          - Show this help message"
	@echo ""
	@echo "🔐 Environment Variables:"
	@echo "  Set these before running 'make deploy':"
	@echo "    export OPENROUTER_API_KEY=your_key_here"
	@echo "    export GEMINI_API_KEY=your_key_here (optional)"
	@echo "    export AWS_REGION=us-east-1 (optional, defaults to us-east-1)"

.PHONY: dev dev-frontend dev-backend build build-frontend build-backend build-lambda deploy destroy refresh test test-local init state-pull clean env logs help