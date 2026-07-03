import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from app import lambda_handler


def test_serves_frontend_index_for_root_path(tmp_path, monkeypatch):
    index_html = tmp_path / 'index.html'
    index_html.write_text('<h1>Movie Picker</h1>', encoding='utf-8')

    monkeypatch.setenv('FRONTEND_DIST_DIR', str(tmp_path))

    response = lambda_handler({'httpMethod': 'GET', 'path': '/'}, None)

    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'].startswith('text/html')
    assert '<h1>Movie Picker</h1>' in response['body']


def test_serves_frontend_index_for_spa_route(tmp_path, monkeypatch):
    index_html = tmp_path / 'index.html'
    index_html.write_text('<h1>Movie Picker SPA</h1>', encoding='utf-8')

    monkeypatch.setenv('FRONTEND_DIST_DIR', str(tmp_path))

    response = lambda_handler({'httpMethod': 'GET', 'path': '/some/deep/link'}, None)

    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'].startswith('text/html')
    assert '<h1>Movie Picker SPA</h1>' in response['body']
