# Movie Picker Deployment Guide

## Current Status
- ✅ Frontend built (React/Vite)
- ✅ Backend code ready
- ✅ Terraform configuration updated
- ⏳ Ready for deployment

## Deployment Steps

### 1. Set API Keys
Edit `terraform/terraform.tfvars`:
```hcl
openrouter_api_key = "YOUR_OPENROUTER_KEY"
```

**Note**: Get your OpenRouter API key from https://openrouter.ai/. The free tier includes access to models like `meta-llama/Meta-Llama-3.1-8B-Instruct:free`.

### 2. Build and Package
```bash
make build-lambda
```

### 3. Deploy to AWS
```bash
make deploy
```

### 4. Test Deployment
```bash
make test
```

### 5. Verify Frontend Integration
The frontend should make API calls to `/movie` endpoint which will be served by the Lambda Function URL.

## Expected Results
```
✅ Lambda function deployed
✅ Function URL accessible
✅ API responds with movie suggestions
✅ Frontend can call API
```

## Troubleshooting
- If API returns 403: Check CORS headers in terraform/main.tf
- If API returns 404: Check Lambda handler path
- If Lambda times out: Increase timeout in terraform/main.tf
- If fallback to static list: API key may not be configured correctly

## API Endpoints
- POST /movie - Get movie suggestion
- GET / - Frontend static files
- GET /movie - Method not allowed (use POST)

## Security
- API keys should be stored in AWS SSM Parameter Store as SecureString
- Never commit `.env` files or API keys to version control
- The `.gitignore` file automatically excludes sensitive files