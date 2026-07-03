#!/usr/bin/env python3
"""Test OpenRouter integration locally"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ No API key found. Set OPENROUTER_API_KEY or GEMINI_API_KEY environment variable.")
    sys.exit(1)

try:
    from backend.src.gemini_client import generate_movie_with_source

    result = generate_movie_with_source({
        'category': 'bollywood',
        'difficulty': 'easy',
        'exclude': ['Sholay']
    })

    print(f"✅ Local test result: {result[0]} (source: {result[1]})")
    sys.exit(0)
except Exception as e:
    print(f"❌ Local test failed: {e}")
    sys.exit(1)