# gemini_client.py
# Google Gemini AI integration for movie suggestions

import os
import random
import time
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv

from fallback_movies import get_random_fallback_movie
from validation import validate_movie_response

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('OPENROUTER_API_KEY')
MAX_TITLE_LENGTH = 80

# Try new google.genai package first (recommended), fall back to old one
try:
    import google.genai as genai
    USE_NEW_SDK = True
except ImportError:
    try:
        import google.generativeai as genai
        USE_NEW_SDK = False
    except ImportError:
        genai = None
        USE_NEW_SDK = False

GEMINI_AVAILABLE = genai is not None and bool(GEMINI_API_KEY)

# Gemini model configuration
GEMINI_MODEL_NAME = "gemini-2.5-flash"

def build_movie_prompt(request_body: dict) -> str:
    """Build prompt for movie title generation."""
    nonce = str(random.randint(1000, 9999))
    categories = request_body.get("category", [])
    if isinstance(categories, str):
        categories = [categories]
    category_label = ", ".join(categories) if categories else "random"
    excluded = ", ".join(request_body.get("exclude", []))

    prompt = (
        "You are picking one movie for a game of dumb charades.\n"
        f"Categories: {category_label}\n"
        f"Difficulty: {request_body.get('difficulty', 'easy')}\n"
        f"Excluded movies: {excluded if excluded else 'None'}\n"
        f"Current nonce: {nonce}\n\n"
        "Rules:\n"
        "- Return exactly one real movie title.\n"
        "- No explanation, quotes, or punctuation beyond the title itself.\n"
        "- The title must be real and not in the excluded list.\n"
        "- Examples of good responses: '3 Idiots', 'Sholay', 'Dangal', 'PK', 'Lagaan'\n"
        "Return only the movie title:"
    )
    return prompt

def get_movie_from_gemini(request_body: dict) -> Optional[str]:
    """Call Google Gemini API to generate a movie title."""
    if not GEMINI_AVAILABLE:
        return None

    try:
        if USE_NEW_SDK:
            # New SDK (google.genai)
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=build_movie_prompt(request_body),
                config={
                    "temperature": 0.8,
                }
            )
            movie_title = response.text if response.text else ""
        else:
            # Old SDK (google.generativeai)
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL_NAME,
                generation_config={
                    "temperature": 0.8,
                    "max_output_tokens": 50,
                }
            )
            response = model.generate_content(build_movie_prompt(request_body))
            movie_title = response.text.strip() if response.text else ""

        if movie_title:
            # Clean up the response - extract just the title
            movie_title = movie_title.strip().strip('"').strip("'").strip()
            movie_title = movie_title.split('\n')[0]  # Take first line only
            if validate_movie_response(movie_title, request_body.get('exclude', [])):
                return movie_title[:MAX_TITLE_LENGTH]
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

    return None

def generate_movie(request_body: dict) -> Optional[str]:
    """Synchronous wrapper with retry."""
    for _ in range(3):  # Try 3 times
        result = get_movie_from_gemini(request_body)
        if result:
            return result
        time.sleep(0.5)
    return None

def generate_movie_with_source(request_body: dict) -> Tuple[str, str]:
    """Return a movie title and the source, preferring Gemini and falling back when needed."""
    movie = generate_movie(request_body)
    if movie:
        return movie, "gemini"

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