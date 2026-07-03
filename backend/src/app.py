import json
import os
from pathlib import Path
from typing import Any, Dict

from validation import validate_request
from gemini_client import generate_movie_with_source


def _read_static_asset(path: str) -> tuple[int, dict, str] | None:
    env_dist = os.environ.get("FRONTEND_DIST_DIR")
    if env_dist:
        dist_dir = Path(env_dist)
    else:
        current_root = Path(__file__).resolve().parent
        local_dist = current_root / "frontend" / "dist"
        if local_dist.exists():
            dist_dir = local_dist
        else:
            dist_dir = current_root.parents[2] / "frontend" / "dist"

    asset_path = dist_dir / path.lstrip("/")

    if not asset_path.exists() or not asset_path.is_file():
        return None

    content_type = "text/html; charset=utf-8"
    if asset_path.suffix == ".css":
        content_type = "text/css; charset=utf-8"
    elif asset_path.suffix in {".js", ".mjs"}:
        content_type = "application/javascript; charset=utf-8"
    elif asset_path.suffix == ".json":
        content_type = "application/json; charset=utf-8"
    elif asset_path.suffix in {".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp"}:
        content_type = "image/" + asset_path.suffix.lstrip(".")

    return 200, {"Content-Type": content_type}, asset_path.read_text(encoding="utf-8")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda entrypoint for the movie picker API and frontend static assets."""
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
    }

    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("path") or event.get("rawPath") or event.get("requestContext", {}).get("http", {}).get("path") or "/"

    if method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    if method == "GET" and path != "/movie":
        asset_response = _read_static_asset(path if path != "/" else "/index.html")
        if asset_response is not None:
            status_code, response_headers, body = asset_response
            response_headers["Access-Control-Allow-Origin"] = "*"
            response_headers["Access-Control-Allow-Headers"] = "Content-Type"
            response_headers["Access-Control-Allow-Methods"] = "OPTIONS,GET,POST"
            return {"statusCode": status_code, "headers": response_headers, "body": body}

        index_path = Path(os.environ.get("FRONTEND_DIST_DIR") or str(Path(__file__).resolve().parents[2] / "frontend" / "dist")) / "index.html"
        if index_path.exists():
            return {
                "statusCode": 200,
                "headers": {**headers, "Content-Type": "text/html; charset=utf-8"},
                "body": index_path.read_text(encoding="utf-8"),
            }

    if method == "GET" and path == "/movie":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "method_not_allowed"}),
        }

    if isinstance(event.get("body"), str):
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            body = {}
    else:
        body = event.get("body") or {}

    is_valid, error, sanitized = validate_request(body)
    if not is_valid:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": error}),
        }

    movie, source = generate_movie_with_source(sanitized)
    categories = sanitized.get("category", [])
    if isinstance(categories, list):
        selected_category = categories[0]
    else:
        selected_category = categories

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({
            "movie": movie,
            "category": selected_category,
            "categories": categories,
            "source": source,
        }),
    }


if __name__ == "__main__":
    sample_event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "category": "bollywood",
            "difficulty": "easy",
            "exclude": ["Sholay"],
        }),
    }
    print(lambda_handler(sample_event, None))
