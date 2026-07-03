# Movie Picker Makefile - Simple Version

PROJECT_ROOT := $(PWD)
BACKEND_DIR := backend
FRONTEND_DIR := frontend
TESTING_DIR := $(PROJECT_ROOT)/backend
TERRAFORM_DIR := $(PROJECT_ROOT)/terraform

# ===================== DEVELOPMENT COMMANDS ==================

.PHONY: dev frontend backend

# Start frontend development server
dev-frontend:
	@echo "🚀 Starting frontend development server..."
	@cd $(FRONTEND_DIR) && npm run dev

# Start backend development server
dev-backend:
	@echo "🐍 Starting backend development server..."
	@cd $(BACKEND_DIR) && poetry install --no-root && poetry run python src/local_server.py

# Start both frontend and backend servers
dev: dev-frontend dev-backend
	@echo "✅ Development servers running:"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend API: http://localhost:8000/movie"

# ===================== BUILD COMMANDS ==================

.PHONY: build-frontend build-backend build-lambda

# Build frontend for production
build-frontend:
	@echo "📦 Building frontend for production..."
	@cd $(FRONTEND_DIR) && npm ci --silent && npm run build

# Install backend dependencies
build-backend:
	@echo "📦 Installing backend dependencies..."
	@cd $(BACKEND_DIR) && poetry install --no-root

# Package Lambda function
build-lambda: build-frontend build-backend
	@echo "🧱 Packaging Lambda ZIP..."
	@mkdir -p .lambda-build/frontend/dist
	@cp -R backend/src/. .lambda-build/
	@cp -R frontend/dist/. .lambda-build/frontend/dist
	@python3 -m pip install -q -r backend/requirements.txt -t .lambda-build
	@cd .lambda-build && zip -rq ../terraform/lambda.zip . && cd ..

# ===================== DEPLOYMENT COMMANDS ==================

.PHONY: deploy destroy

# Deploy Lambda function
deploy: build-lambda
	@echo "✅ Deploying Lambda function..."
	@cd $(TERRAFORM_DIR) && terraform init -input=false && terraform apply -auto-approve

# Destroy Lambda function
destroy:
	@echo "🚀 Destroying Lambda function..."
	@cd $(TERRAFORM_DIR) && terraform destroy -auto-approve

# ===================== TESTING COMMANDS ==================

.PHONY: test

# Test deployed Lambda endpoint
test: deploy
	@echo "🌐 Testing deployed Lambda endpoint..."
	@API_URL=$$(cd $(TERRAFORM_DIR) && terraform output -raw api_url) && \
	curl -s -X POST "$$API_URL/movie" \
	  -H "Content-Type: application/json" \
	  -d '{"category":"bollywood","difficulty":"easy","exclude":["Sholay"]}' | jq

# ===================== UTILITY COMMANDS ==================

.PHONY: clean vars help

# Edit Terraform variables
vars:
	@echo "📝 Editing Terraform variables..."
	@code $(TERRAFORM_DIR)/terraform.tfvars || nano $(TERRAFORM_DIR)/terraform.tfvars || vi $(TERRAFORM_DIR)/terraform.tfvars

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf .lambda-build .terraform .terraform.lock.hcl terraform.tfstate* lambda.zip
	@cd frontend && rm -rf node_modules .vite dist
	@cd backend && rm -rf .venv __pycache__ */__pycache__ poetry.lock
	@echo "✅ Cleaned build artifacts"

# Display help
help:
	@echo ""
	@echo "🎬 Movie Picker Project - Makefile Commands"
	@echo ""
	@echo "📋 DEVELOPMENT:"
	@echo "  make dev-frontend      Start frontend dev server"
	@echo "  make dev-backend       Start backend dev server"
	@echo "  make dev               Start both dev servers"
	@echo ""
	@echo "📦 BUILD:"
	@echo "  make build-frontend    Build frontend for production"
	@echo "  make build-backend     Install backend dependencies"
	@echo "  make build-lambda      Package Lambda function"
	@echo ""
	@echo "🚀 DEPLOYMENT:"
	@echo "  make deploy            Deploy to AWS Lambda"
	@echo "  make destroy           Destroy AWS resources"
	@echo ""
	@echo "🧪 TESTING:"
	@echo "  make test              Test deployed Lambda endpoint"
	@echo ""
	@echo "🔧 UTILITIES:"
	@echo "  make vars              Edit Terraform variables"
	@echo "  make clean             Clean build artifacts"
	@echo "  make help              Show this help"
	@echo ""