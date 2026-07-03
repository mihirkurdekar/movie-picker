# Dumb Charades Movie Picker

A single-player web app that suggests a movie title for dumb charades. The React frontend sends the current category, difficulty, and already-shown titles to a Python backend that validates the request, calls OpenRouter when available, and falls back to a curated list when the API is unavailable or rate-limited.

## Features

- Category selection: Bollywood, Hollywood, Tollywood, Kollywood, Punjabi, Mixed-Indian, and Random
- Difficulty selection: Easy or Hard
- Session-based exclusion list so the app avoids repeating the same title within a session
- Graceful fallback to a static movie list if OpenRouter is unavailable
- AWS Lambda-ready backend with a Terraform deployment scaffold

## Security Notice

⚠️ **Important**: Never commit `.env` files or any files containing API keys to version control. These files are automatically ignored by `.gitignore`. Always use `.env.example` files as templates for local development.

## Project Layout

- backend/: Python Lambda handler and supporting modules
- frontend/: Vite + React UI
- spec.md: product specification and API contract

## Local Development

### Prerequisites

- Python 3.12
- Poetry
- Node.js and npm

### Backend

Install Poetry if needed:

```bash
brew install poetry
```

Then run:

```bash
cd backend
poetry install
poetry run pytest -q
poetry run python src/local_server.py
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run build
```

### API Key Setup

Before running locally, create a `.env` file in the `backend/` directory with your OpenRouter API key:

```bash
# backend/.env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get an API key from [OpenRouter](https://openrouter.ai/). The free tier includes access to models like `meta-llama/Meta-Llama-3.1-8B-Instruct:free`.

### Local app

From the project root, run:

```bash
cd frontend && npm install && npm run build
cd ../backend && poetry run python src/local_server.py
```

This builds the frontend and serves it from the backend on http://127.0.0.1:8000/.

## Backend API

POST /movie

Request body:

```json
{
  "category": "bollywood",
  "difficulty": "easy",
  "exclude": ["Sholay"]
}
```

Response:

```json
{
  "movie": "Lagaan",
  "category": "bollywood",
  "source": "openrouter"
}
```

## AWS Deployment

### Terraform

The Terraform scaffold lives in the terraform/ directory. It provisions:

- an AWS Lambda function
- an API Gateway HTTP API route
- an IAM role for Lambda execution

### Prerequisites

- AWS CLI configured with credentials
- Terraform installed

### Deploy

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Set the OPENROUTER_API_KEY environment variable for the Lambda function before deployment.

## Development Notes

- The backend uses OpenRouter API instead of Gemini
- No DynamoDB, no persistent storage
- No authentication - public endpoint with throttling protection

---

Created by **Mihir K**.  
This repository: [movie-picker](https://github.com/mihirkurdekar/movie-picker)