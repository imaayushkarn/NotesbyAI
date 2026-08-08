# Testing Strategy

## Approach
Tests use Flask's built-in test client and **mock the Gemini API call**,
so the full test suite runs in CI without needing a real `GEMINI_API_KEY`
or making network calls (network access in CI is unreliable and costs
quota).

## What is covered (`tests/test_app.py`)

| Test | What it verifies |
|---|---|
| `test_home_page_loads` | `/` returns 200 and serves the frontend HTML |
| `test_generate_rejects_empty_input` | `/generate` returns a 400 error with no text/file |
| `test_generate_rejects_short_text` | `/generate` rejects trivially short input |
| `test_generate_success_with_mocked_ai` | Given valid text and a mocked Gemini response, `/generate` returns well-formed JSON with all four expected keys |
| `test_clean_json_response_strips_markdown_fences` | The JSON-cleaning helper correctly strips ` ```json ` fences that models sometimes add |
| `test_missing_api_key_returns_clear_error` | If `GEMINI_API_KEY` isn't set, the app fails gracefully with a helpful message instead of crashing |

## Running tests locally

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Running the linter locally

```bash
pip install -r requirements-dev.txt
flake8 app.py tests/
```

## CI Pipeline
See `.github/workflows/ci.yml`. On every push and pull request, GitHub
Actions:
1. Installs Python and project dependencies
2. Runs `flake8` for code quality/linting
3. Runs the full `pytest` suite

If either step fails, the commit is marked failed in GitHub, so broken
code cannot silently merge.

## What is intentionally NOT covered by automated tests
- Real calls to the Gemini API (would require a live key and would be
  flaky/non-deterministic in CI)
- Frontend JavaScript (no test runner is set up for it in v1.0; this is
  listed as future scope)
- Vercel deployment itself (verified manually via the live URL)
