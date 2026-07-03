import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import gemini_client
from fallback_movies import get_random_fallback_movie


def test_fallback_movie_is_not_in_exclude_list():
    payload = {'category': 'bollywood', 'exclude': ['Sholay', 'Dangal']}
    movie = get_random_fallback_movie('bollywood', payload['exclude'])

    assert movie is not None
    assert movie not in payload['exclude']


def test_get_movie_from_gemini_retries_with_alternate_model(monkeypatch):
    calls = []

    class FakeModels:
        def generate_content(self, model, contents):
            calls.append(model)
            if model == 'gemini-2.0-flash-lite':
                raise RuntimeError('429 RESOURCE_EXHAUSTED')
            return SimpleNamespace(text='Lagaan')

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(gemini_client, 'google_genai', SimpleNamespace(Client=FakeClient))
    monkeypatch.setattr(gemini_client, '_get_candidate_models', lambda: ['gemini-2.0-flash-lite', 'gemini-2.0-flash'])
    monkeypatch.setenv('API_KEY', 'test-key')

    result = gemini_client.get_movie_from_gemini({'category': 'bollywood', 'difficulty': 'easy', 'exclude': []})

    assert result == 'Lagaan'
    assert calls == ['gemini-2.0-flash-lite', 'gemini-2.0-flash']
