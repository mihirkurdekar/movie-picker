# movie-picker

An AI-powered movie recommendation system that suggests titles for the game *Dumb Charades*.
Deployed on AWS Lambda with a React frontend, this project combines AI-generated titles with a curated fallback list.

---

## 🎬 Overview

A lightweight web app that suggests a random Bollywood (or other regional) movie for gameplay of *Dumb Charades*.
AI-driven suggestions come from the **Google Gemini** API (fallback to a curated local list when the API is unavailable).

---

## 🎬 Features

- **Dynamic Category Picker** - Choose from Bollywood, Hollywood, Tollywood, etc.
- **Difficulty Levels** - Easy or Hard mode.
- **Exclusion List** - Avoid movies you've already seen.
- **Graceful Fallback** - When the AI API is unavailable, fallback to a curated local list.
- **Secure API Key Handling** - `.env` file keeps API keys out of source control.

## 📂 Repository Layout

```
movie-picker/
├─ backend/
│   ├─ src/
│   │   ├─ app.py          # Lambda handler
│   │   ├─ validation.py
│   │   └─ fallback_movies.py
│   │
├─ frontend/                     # React + Vite
├─ terraform/                # IaC for AWS Lambda + API Gateway
├─ Makefile                 # Development helpers
└─ README.md
```

## 🚀 Quick Deployment

```bash
# Build & Deploy (single command)
make deploy

# Test the deployed endpoint
make test
```

---

## 📦 Deployment Options

| Method              | Command                              | Description |
|-------------------|--------------------|----------------------|
| **Lambda URL**      | `make deploy`      | Deploys the latest code to AWS Lambda + API Gateway |
| **Manual Deploy**   | `terraform apply` (with `terraform.tfvars`) | Manual infrastructure provisioning |
| **Local Test**      | `make dev-server`   | Starts both frontend (Vite) and backend (Python) servers |

---

## 📦 Installation (Local Development)

```bash
# Install dependencies
cd backend && poetry install
cd frontend && npm install

# Start servers
make dev   # runs both frontend & backend

# Build for production
make build
```

### Environment Variables

Create a `.env` file in `backend/.env` (or set env vars manually):

```dotenv
OPENROUTER_API_KEY=your_api_key_here
GEMINI_API_KEY=your_gemini_key_here
```

---

## 📚 Usage

```bash
# Run both frontend & backend servers
make dev

# Test the deployed endpoint locally
make test-local
```

### Available Endpoints

| Endpoint               | Method | Description |
|------------------|-----------|----------------|
| `POST /movie` | Returns a random movie title based on category & difficulty |
| `GET /movie` (GET) | Returns a random movie from the curated list |
| `DELETE /movie` | Not implemented (reserved for future) |

**Example Request:**

```bash
curl -X POST http://localhost:8000/movie \
  -H "Content-Type: application/json" \
  -d '{"category":"bollywood","difficulty":"easy","exclude":[]}'
```

---

## 📦 Building & Testing

```bash
make build          # Build frontend
make test-local   # Invoke /movie endpoint locally
make test         # Deploy & test endpoint
```

---

## 📚 Contributing

1. Fork the repo
2. Create a feature branch
3. Open a Pull Request

*All contributions are welcome!*

---

## 🎉 Final Thoughts

The **movie-picker** project now combines AI-generated suggestions with a robust fallback library, offering a seamless user experience both locally and in production. With a single command (`make deploy`) you can spin up a fully functional API backend and instantly test the recommendation engine.

---

*Happy coding!*

---

## 📋 Makefile Commands Reference

```bash
make dev           # Start development servers
make build         # Build for production
make deploy        # Deploy to AWS Lambda
make test-local    # Test local endpoint
make test          # Test deployed endpoint
make clean         # Remove build artifacts
make help          # Show all commands
```