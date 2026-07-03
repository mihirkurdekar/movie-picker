# validation.py
# Enum validation and input sanitization for the movie-picker API

VALID_CATEGORIES = {
    'bollywood': 'Bollywood (Hindi cinema)',
    'hollywood': 'Hollywood (English cinema)',
    'tollywood': 'Tollywood (Telugu cinema)',
    'kollywood': 'Kollywood (Tamil cinema)',
    'punjabi': 'Punjabi cinema',
    'mixed_indian': 'Mixed-Indian cinema (all Indian categories)',
    'random': 'Random (any category)'
}

VALID_DIFFICULTIES = {
    'easy': 'Easy — a very well-known blockbuster',
    'hard': 'Hard — lesser-known but real movie'
}

MAX_EXCLUDE_COUNT = 40
MAX_EXCLUDE_LENGTH = 100
MAX_MOVIE_TITLE_LENGTH = 80

def validate_request(request_body):
    """Validate and sanitize the movie picker request.

    Args:
        request_body: Dict containing category, difficulty, exclude list

    Returns:
        tuple: (is_valid, error_message, sanitized_body)
    """
    # Validate difficulty
    difficulty = request_body.get('difficulty', '').lower()
    if difficulty not in VALID_DIFFICULTIES:
        return False, f"invalid_difficulty", None

    # Process category input, supporting either a single category string or a list
    raw_categories = request_body.get('category', [])
    if isinstance(raw_categories, str):
        raw_categories = [raw_categories]

    if not isinstance(raw_categories, list):
        return False, f"invalid_category", None

    categories = []
    for category in raw_categories:
        if not isinstance(category, str):
            continue
        category_key = category.lower()
        if category_key in VALID_CATEGORIES:
            categories.append(category_key)

    if not categories:
        return False, f"invalid_category", None

    # Deduplicate while preserving order
    categories = list(dict.fromkeys(categories))

    # Process exclude list
    exclude = request_body.get('exclude', [])
    if not isinstance(exclude, list):
        return False, f"invalid_exclude_format", None

    sanitized_exclude = []
    for movie in exclude:
        if not isinstance(movie, str):
            continue

        # Enforce length limit per movie
        if len(movie) > MAX_EXCLUDE_LENGTH:
            continue

        sanitized_exclude.append(movie)

    # Enforce count limit
    if len(sanitized_exclude) > MAX_EXCLUDE_COUNT:
        sanitized_exclude = sanitized_exclude[:MAX_EXCLUDE_COUNT]

    # Build sanitized request
    sanitized_body = {
        'category': categories,
        'difficulty': difficulty,
        'exclude': sanitized_exclude
    }

    return True, None, sanitized_body

def validate_movie_response(movie_title, exclude_list):
    """Validate a movie response from Gemini.

    Args:
        movie_title: The movie title to validate
        exclude_list: List of movies already shown

    Returns:
        tuple: (is_valid, error_reason)
    """
    if not movie_title or not isinstance(movie_title, str):
        return False, "empty_movie_title"

    movie_title = movie_title.strip()

    if len(movie_title) > MAX_MOVIE_TITLE_LENGTH:
        return False, "movie_title_too_long"

    if movie_title in exclude_list:
        return False, "movie_in_exclude_list"

    return True, None

def get_category_label(category):
    """Get the human-readable label for a category."""
    return VALID_CATEGORIES.get(category, category)

def get_difficulty_label(difficulty):
    """Get the human-readable label for a difficulty."""
    return VALID_DIFFICULTIES.get(difficulty, difficulty)