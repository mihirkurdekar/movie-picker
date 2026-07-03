import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from validation import validate_request, validate_movie_response


def test_validate_request_accepts_valid_payload_and_sanitizes_exclude():
    payload = {
        'category': 'bollywood',
        'difficulty': 'easy',
        'exclude': ['Sholay', 'Dangal']
    }

    is_valid, error, sanitized = validate_request(payload)

    assert is_valid is True
    assert error is None
    assert sanitized['category'] == ['bollywood']
    assert sanitized['difficulty'] == 'easy'
    assert sanitized['exclude'] == ['Sholay', 'Dangal']


def test_validate_request_rejects_invalid_category_or_difficulty():
    invalid_category, _, _ = validate_request({'category': 'mystery', 'difficulty': 'easy', 'exclude': []})
    invalid_difficulty, _, _ = validate_request({'category': 'bollywood', 'difficulty': 'insane', 'exclude': []})

    assert invalid_category is False
    assert invalid_difficulty is False


def test_validate_movie_response_rejects_empty_or_excluded_titles():
    assert validate_movie_response('', ['Sholay'])[0] is False
    assert validate_movie_response('Sholay', ['Sholay'])[0] is False
    assert validate_movie_response('Lagaan', ['Sholay'])[0] is True
