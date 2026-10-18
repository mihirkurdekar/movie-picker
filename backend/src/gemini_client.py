# gemini_client.py
# Google Gemini AI integration for movie suggestions

import os
import random
import time
import logging
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv

from fallback_movies import get_random_fallback_movie
from validation import validate_movie_response

# Configure logging
logger = logging.getLogger(__name__)

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
GEMINI_MODEL_NAME = "gemini-3.8-flash"

def build_movie_prompt(request_body: dict) -> str:
    """Build prompt for movie title generation with strong diversity constraints."""
    # Use a random seed and current time to force the model out of its patterns
    seed = random.randint(1, 1000000)
    timestamp = int(time.time())
    
    categories = request_body.get("category", [])
    if isinstance(categories, str):
        categories = [categories]
    category_label = ", ".join(categories) if categories else "random"
    excluded = request_body.get("exclude", [])
    excluded_str = ", ".join(excluded) if excluded else "None"

    prompt = (
        f"System Request ID: {seed}-{timestamp}\n"
        "You are a movie expert for a game of dumb charades.\n"
        f"Categories: {category_label}\n"
        f"Difficulty: {request_body.get('difficulty', 'easy')}\n"
        f"ALREADY SHOWN (Do NOT pick these): {excluded_str}\n\n"
        "CRITICAL RULES:\n"
        "1. Pick a movie that is NOT in the 'ALREADY SHOWN' list.\n"
        "2. AVOID the most obvious common picks (e.g., avoid 'Sholay' or '3 Idiots' if they appear too often).\n"
        "3. Pick a variety of movies from different eras and genres within the category.\n"
        "4. Return ONLY the real movie title. No quotes, no explanation, no punctuation.\n"
        "5. The movie must be real and fit the requested difficulty.\n\n"
        "Return only the movie title:"
    )
    return prompt

def get_movie_from_gemini(request_body: dict) -> Optional[str]:
    """Call Google Gemini API to generate a movie title."""
    if not GEMINI_AVAILABLE:
        logger.warning("Gemini not available: Missing API key or SDK")
        return None

    try:
        if USE_NEW_SDK:
            client = genai.Client(api_key=GEMINI_API_KEY)
            model_id = f"models/{GEMINI_MODEL_NAME}" if not GEMINI_MODEL_NAME.startswith("models/") else GEMINI_MODEL_NAME
            
            response = client.models.generate_content(
                model=model_id,
                contents=build_movie_prompt(request_body),
                config={
                    "temperature": 1.0, # Increased temperature for more randomness/diversity
                }
            )
            movie_title = response.text if response.text else ""
        else:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL_NAME,
                generation_config={
                    "temperature": 1.0,
                    "max_output_tokens": 50,
                }
            )
            response = model.generate_content(build_movie_prompt(request_body))
            movie_title = response.text.strip() if response.text else ""

        if movie_title:
            movie_title = movie_title.strip().strip('"').strip("'").strip()
            movie_title = movie_title.split('\n')[0]
            
            # Double check exclusion list locally
            if validate_movie_response(movie_title, request_body.get('exclude', [])):
                return movie_title[:MAX_TITLE_LENGTH]
            else:
                logger.info("Gemini suggested an excluded movie: %s", movie_title)
    except Exception as e:
        logger.error("Gemini API error: %s", e, exc_info=True)
        return None

    return None

def generate_movie(request_body: dict) -> Optional[str]:
    """Synchronous wrapper with retry and fallback detection."""
    for i in range(3):
        result = get_movie_from_gemini(request_body)
        if result:
            return result
        logger.info("Gemini attempt %d failed, retrying...", i + 1)
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
