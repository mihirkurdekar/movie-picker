# -------------------------------------------------
# Makefile - Movie Picker Full Project Management
# -------------------------------------------------

# Directories
PROJECT_ROOT := $(shell pwd)
FRONTEND_DIR := frontend
BACKEND_DIR := backend
TERRAFORM_DIR := terraform
LAMBDA_BUILD_DIR := .lambda-build
VENV_DIR := $(BACKEND_DIR)/.venv
VENV_PYTHON := $(VENV_DIR)/bin/python3

# AWS Configuration
AWS_REGION ?= us-east-1
LAMBDA_FUNCTION_NAME ?= movie-picker

# Environment Variables
OPENROUTER_API_KEY ?= $(shell grep -m1 "OPENROUTER_API_KEY" .env 2>/dev/null | cut -d= -f2 || echo "")
GEMINI_API_KEY ?= $(shell grep -m1 "GEMINI_API_KEY" .env 2>/dev/null | cut -d= -f2 || echo "")

# -------------------------------------------------
# Development Targets
# -------------------------------------------------
## dev       : Start both frontend and backend servers
dev:
	@echo "🚀 Starting Movie Picker Development Environment..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8080/movie"
	@echo "Press Ctrl+C to stop all servers, or run 'make stop' in another terminal."
	@cd $(FRONTEND_DIR) && npm run dev &
	@$(VENV_PYTHON) $(BACKEND_DIR)/src/local_server.py &
	@wait

## stop      : Kill all development servers
stop:
	@echo "🛑 Stopping all Movie Picker servers..."
	@lsof -ti:3000 | xargs kill -9 2>/dev/null || true
	@lsof -ti:8080 | xargs kill -9 2>/dev/null || true
	@echo "✅ Servers stopped."

## dev-frontend  : Start only frontend development server
dev-frontend:
	@cd $(FRONTEND_DIR) && npm run dev

## dev-backend   : Start only backend development server
dev-backend:
	@$(VENV_PYTHON) $(BACKEND_DIR)/src/local_server.py

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
	@$(MAKE) env

## build-lambda   : Package Lambda function for deployment
build-lambda:
	@echo "🧱 Building Lambda package..."
	@rm -rf $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)
	@mkdir -p $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)
	@mkdir -p $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)/frontend/dist
	@cp -R backend/src/. $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)/
	@cp -R frontend/dist/. $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)/frontend/dist/
	@$(VENV_PYTHON) -m pip install -r $(BACKEND_DIR)/requirements.txt -t $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)
	@echo "✅ Lambda package ready at $(PROJECT_ROOT)/$(LAMBDA_BUILD_DIR)/"

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
## test-local: Test local backend endpoint
test-local:
	@echo "🔍 Testing local backend endpoint..."
	@curl -s -X POST http://localhost:8080/movie \
	      -H "Content-Type: application/json" \
	      -d '{"category":"bollywood","difficulty":"easy","exclude":[]}' | jq .

# -------------------------------------------------
# Utility Targets
# -------------------------------------------------
## clean     : Remove all build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(LAMBDA_BUILD_DIR)
	@rm -rf $(VENV_DIR)
	@rm -rf $(FRONTEND_DIR)/node_modules $(FRONTEND_DIR)/.vite $(FRONTEND_DIR)/dist
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete."

## env       : Install all dependencies
env:
	@echo "📦 Installing dependencies..."
	@cd $(FRONTEND_DIR) && npm install
	@echo "Creating Python virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@$(VENV_PYTHON) -m pip install --upgrade pip
	@$(VENV_PYTHON) -m pip install -r $(BACKEND_DIR)/requirements.txt
	@echo "✅ Dependencies installed in $(VENV_DIR)"

## help      : Show all available make commands
help:
	@echo "Movie Picker - Available make targets:"
	@echo ""
	@echo "🚀 Development:"
	@echo "  make dev           - Start frontend and backend dev servers"
	@echo "  make stop          - Kill all dev servers"
	@echo "  make dev-frontend  - Start only frontend server"
	@echo "  make dev-backend   - Start only backend server"
	@echo ""
	@echo "🔨 Build:"
	@echo "  make build         - Build everything for production"
	@echo "  make build-lambda  - Package Lambda function"
	@echo ""
	@echo "📤 Deployment:"
	@echo "  make deploy        - Build and deploy to AWS Lambda"
	@echo "  make destroy       - Remove all AWS resources"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test-local    - Test local backend endpoint"
	@echo ""
	@echo "🧹 Utilities:"
	@echo "  make clean         - Remove all build artifacts"
	@echo "  make env           - Install all dependencies"
	@echo "  make help         - Show this help message"

.PHONY: dev stop dev-frontend dev-backend build build-frontend build-backend build-lambda deploy destroy refresh test-local clean env help
