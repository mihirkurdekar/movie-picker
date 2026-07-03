# gemini_client.py
# OpenRouter API integration for movie suggestions

import os
import random
import time
import requests
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv

from fallback_movies import get_random_fallback_movie
from validation import validate_movie_response

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY') or os.getenv('GEMINI_API_KEY')
MAX_TITLE_LENGTH = 80


def _get_candidate_models() -> list[str]:
    return ["gemini-2.0-flash-lite", "gemini-2.0-flash"]


def _build_prompt(request_body: dict) -> str:
    nonce = str(random.randint(1000, 9999))
    categories = request_body.get("category", [])
    if isinstance(categories, str):
        categories = [categories]
    category_label = ", ".join(categories)
    excluded = ", ".join(request_body.get("exclude", []))
    return (
        "You are picking one movie for a game of dumb charades.\n"
        f"Categories: {category_label}\n"
        f"Difficulty: {request_body['difficulty']}\n"
        f"Excluded movies: {excluded}\n"
        f"Current nonce: {nonce}\n\n"
        "Rules:\n"
        "- Return exactly one real movie title.\n"
        "- No explanation, quotes, or punctuation beyond the title itself.\n"
        "- The title must be real and not in the excluded list."
    )


def get_movie_from_openrouter(request_body: dict) -> Optional[str]:
    """Call OpenRouter API to generate a movie title."""
    if not OPENROUTER_API_KEY:
        return None

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://localhost:3000",  # Your app URL
                "X-Title": "Movie Picker App"
            },
            json={
                "model": "meta-llama/Meta-Llama-3.1-8B-Instruct:free",  # Free model
                "messages": [{
                    "role": "user",
                    "content": _build_prompt(request_body)
                }],
                "max_tokens": 50,
                "temperature": 0.8
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            movie_title = data['choices'][0]['message']['content'].strip()

            if validate_movie_response(movie_title, request_body.get('exclude', [])):
                return movie_title[:MAX_TITLE_LENGTH]
    except Exception:
        return None

    return None


def generate_movie(request_body: dict) -> Optional[str]:
    """Synchronous wrapper with retry."""
    for _ in range(3):  # Try 3 times
        result = get_movie_from_openrouter(request_body)
        if result:
            return result
        time.sleep(0.5)
    return None


def generate_movie_with_source(request_body: dict) -> Tuple[str, str]:
    """Return a movie title and the source, preferring OpenRouter and falling back when needed."""
    movie = generate_movie(request_body)
    if movie:
        return movie, "openrouter"

    categories = request_body.get('category', [])
    if isinstance(categories, str):
        categories = [categories]

    fallback_movie = None
    for category in categories:
        fallback_movie = get_random_fallback_movie(category, request_body.get('exclude', []))
        if fallback_movie:
            break

    if fallback_movie:
        return fallback_movie, "fallback"

    return "No movie found", "fallback"