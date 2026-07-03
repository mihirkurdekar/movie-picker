# -------------------------------------------------
# Makefile - Movie Picker Local Development Setup
# -------------------------------------------------
# Directories
FRONTEND_DIR := frontend
BACKEND_DIR  := backend

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

# -------------------------------------------------
# Build & Test Targets
# -------------------------------------------------
## build      : Build frontend for production (uses `npm run build`)
build:
	@cd $(FRONTEND_DIR) && npm run build

## test-backend : Run a quick check against the local backend endpoint
test-backend:
	@echo "🔍 Testing backend endpoint..."
	@curl -s -X POST http://localhost:8080/movie \
	      -H "Content-Type: application/json" \
	      -d '{"category":"bollywood","difficulty":"easy"}' | jq .

# -------------------------------------------------
# Clean & Cleanup Targets
# -------------------------------------------------
## clean      : Remove build artifacts and dependency folders
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf frontend/node_modules frontend/.vite frontend/dist
	@rm -rf backend/.python_backend_backend
	@find . -type d -name "__pycache__" -exec rm -rf {} +

## env      : Install core dependencies for backend (Poetry)
env:
	@cd $(BACKEND_DIR) && poetry install

# -------------------------------------------------
# Utility Targets
# -------------------------------------------------
## help      : Show available make commands
help:
	@echo "Available make targets:"
	@echo "  make dev       - Start frontend and backend dev servers"
	@echo "  make build     - Build frontend for production"
	@echo "  make test-backend - Test backend endpoint locally"
	@echo "  make clean     - Remove build and dependency artifacts"
	@echo "  make env       - Install backend dependencies via Poetry"

.PHONY: dev build test-backend clean env help