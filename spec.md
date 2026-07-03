# Dumb Charades Movie Generator — Spec

## 1. Overview

A single-player web app that gives a random movie title to act out for dumb charades. The user picks a **category** (Bollywood, Hollywood, Tollywood, Kollywood, Punjabi, Mixed-Indian, Random-All) and a **difficulty** (Easy = widely known, Hard = lesser-known but real). The app calls OpenRouter API, per request, to generate a single movie title that hasn't been shown yet this session, and displays it hidden-by-default with a tap-to-reveal.

No accounts, no scoring, no multi-device sync. Fully stateless backend — no database.

## 2. Architecture

```
┌─────────────┐      HTTPS       ┌───────────────────┐      HTTPS      ┌──────────┐
│  React App  │ ───────────────▶ │  API Gateway       │ ──────────────▶│  Lambda  │
│  (S3 + CF)  │ ◀─────────────── │  (HTTP API,        │ ◀───────────────│ (Python) │
└─────────────┘   JSON response  │   throttled)        │   JSON          └────┬─────┘
                                  └───────────────────┘                       │
                                                                              ▼
                                                                     ┌─────────────────┐
                                                                     │  Gemini API      │
                                                                     │  (Flash / Flash- │
                                                                     │   Lite, free tier)│
                                                                     └─────────────────┘
```

- **No DynamoDB, no persistent storage.** The "already shown" exclusion list lives entirely in the React app's session state and is sent up with every request.
- **No auth.** Public endpoint, protected only by throttling + input validation + graceful degradation (see §6).

## 3. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, plain CSS or Tailwind |
| Hosting (frontend) | S3 + CloudFront |
| Backend | Python 3.12 on AWS Lambda |
| API layer | API Gateway HTTP API (not REST API — cheaper, simpler) |
| LLM | Gemini API — `gemini-flash-lite` (or current free-tier Flash model) via `google-generativeai` / `google-genai` SDK |
| Secrets | AWS SSM Parameter Store (SecureString) for the Gemini API key |
| IaC | AWS SAM (`template.yaml`) |
| Local dev | `sam local start-api` |

## 4. API Contract

### `POST /movie`

**Request**
```json
{
  "category": "bollywood",
  "difficulty": "easy",
  "exclude": ["3 Idiots", "Dangal", "Sholay"]
}
```

- `category`: enum — `bollywood | hollywood | tollywood | kollywood | punjabi | mixed_indian | random`
- `difficulty`: enum — `easy | hard`
- `exclude`: array of strings already shown this session, max 40 items, each capped at 100 chars (truncate/reject longer — this is also the input-sanitization boundary, see §6)

**Response — success**
```json
{
  "movie": "Lagaan",
  "category": "bollywood",
  "source": "gemini"
}
```

**Response — fallback (Gemini quota/error)**
```json
{
  "movie": "Sholay",
  "category": "bollywood",
  "source": "fallback"
}
```

**Response — validation error (400)**
```json
{ "error": "invalid_category" }
```

**Response — rate limited (429)** — returned by API Gateway itself, not the Lambda body.

## 5. Gemini Prompt Design

System-style instruction, assembled server-side only from the validated enum + exclusion list — **never from raw free-text input**:

```
You are picking one movie for a game of dumb charades (acting out a movie title silently).

Category: {category_label}      e.g. "Bollywood (Hindi cinema)"
Difficulty: {difficulty_label}   e.g. "Easy — a very well-known blockbuster"

Rules:
- Return exactly ONE real, released movie title. No explanation, no quotes, no punctuation beyond what's in the title itself.
- The movie must NOT be any of these already-used titles: {exclude_list_joined}
- Prefer variety — avoid the single most obvious answer if it's in the exclude list already implies repetition; pick something different each time even across calls.
- Do not invent a title. It must be a real movie.
```

- Add a random nonce / current timestamp string into the prompt (not shown above) purely to discourage the model from caching the same "top of mind" answer every call.
- Lambda strips/validates the response: trim whitespace, reject if empty, reject if it exactly matches something in `exclude`, reject if longer than ~80 chars (guards against the model going off-script). One retry on a bad response, then fall back to the static list.

## 6. Misuse Protection & Rate Limiting (no DynamoDB)

Since there's no database, protection is entirely **stateless per-request** plus **infra-level throttling**:

1. **API Gateway stage throttling** — set `RateLimit` ~5 req/sec and `BurstLimit` ~10 on the route. This is the primary defense against scripted hammering; it's free and built into API Gateway.
2. **Lambda reserved concurrency** — cap at a low number (e.g. 5). Prevents a burst of concurrent requests from multiplying Gemini calls or Lambda cost simultaneously.
3. **Strict server-side enum validation** — `category` and `difficulty` are checked against allow-lists before they ever touch the Gemini prompt. Anything outside the enum is a 400, no Gemini call made. This is also what keeps the Gemini prompt injection-proof: nothing free-form from the client reaches the model except the exclude-list strings, which are length-capped and only ever used as plain "don't pick this" data, never as instructions.
4. **Graceful Gemini-quota degradation** — wrap the Gemini call in try/except:
   - On `429` / `RESOURCE_EXHAUSTED`: one retry with a short backoff (e.g. 300ms), then fall back to a static curated list bundled in the Lambda package (50–80 movies across categories, hand-picked). Response still returns `200` with `"source": "fallback"` so the UI never breaks.
   - On any other API error: same fallback behavior.
5. **No per-IP counters** (would need DynamoDB) — accepted trade-off given the no-DB constraint. The combination of (1) and (2) is the practical ceiling on abuse; the fallback list in (4) ensures the app degrades gracefully rather than failing even if the free tier is exhausted for the day.

## 7. Frontend Component Breakdown (React + Vite)

```
src/
  App.jsx                 — top-level state: category, difficulty, shownMovies[], currentMovie, revealed
  components/
    CategorySelector.jsx  — pills/buttons for category enum
    DifficultySelector.jsx— easy/hard toggle
    MovieCard.jsx          — shows "???" / blurred title until tapped, then reveals
    GetMovieButton.jsx     — calls API, appends result to shownMovies, resets revealed=false
    ResetButton.jsx        — clears shownMovies (new session)
  api/
    client.js              — fetch wrapper for POST /movie, handles 429/error states with a friendly message
```

State lives entirely in `App.jsx` (no backend persistence needed):
```js
const [shownMovies, setShownMovies] = useState([]); // capped at 40, oldest dropped
```

## 8. Project File Structure

```
charades-app/
  backend/
    template.yaml           # SAM template: Lambda + HTTP API + throttling config
    src/
      app.py                 # Lambda handler
      gemini_client.py        # Gemini call + retry/fallback logic
      validation.py           # enum checks, exclude-list sanitization
      fallback_movies.py      # static curated list by category
    requirements.txt
    tests/
      test_validation.py
      test_gemini_client.py
  frontend/
    (Vite React app, structure per §7)
  README.md
```

## 9. SAM Template Notes (`template.yaml`)

- One `AWS::Serverless::Function` (Python 3.12, `app.lambda_handler`), reserved concurrency set.
- One `AWS::Serverless::HttpApi` with a `POST /movie` route, `ThrottlingRateLimit` / `ThrottlingBurstLimit` set on the default stage, CORS configured for the CloudFront origin.
- Gemini API key referenced via SSM `{{resolve:ssm-secure:/charades-app/gemini-api-key}}` or read at runtime via `boto3` SSM client at cold start (cached on the Lambda execution context, not refetched per invocation).
- No DynamoDB resources.

## 10. Deployment Steps (outline)

1. `sam build && sam deploy --guided` for backend.
2. Note the API Gateway invoke URL.
3. `frontend/.env` → `VITE_API_URL=<invoke-url>`.
4. `npm run build` in `frontend/`, sync `dist/` to S3 bucket, invalidate CloudFront.

## 11. Out of Scope (for this version)

- Multiplayer / teams / scoring / timers
- Persistent history across sessions
- User accounts
- Per-IP rate limiting (would require DynamoDB or similar)
