# Changelog

All notable changes to this repository will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning where applicable.

## [Unreleased]

### Added
- Initialize `CHANGELOG.md` to track ongoing migration and fixes.

### Changed
- Planned modernization of toolchain (venv, pytest, ruff, black, mypy) targeting Python 3.11/3.12.

## [2025-08-29] - Audit Kickoff

### Fixed
- `src/tdd/checkout.py`: Use integer division for discount calculation to avoid float totals on modern Python.
- `src/tdd/syntax_examples/mock_test.py`: Import `Mock`, add missing helpers, and correct `monkeypatch` usage so tests pass.
- `src/gui-weather/weather_app.py`:
  - Switch HTTP endpoints to HTTPS (NOAA/NWS and OpenWeatherMap icon/API URLs).
  - Add request timeouts to `urlopen` calls to prevent hangs on network issues.
  - Replace `is` with `==` for string comparison in visibility handling.
  - Guard GUI startup with `if __name__ == "__main__":` to prevent unintended launch on import.
  - API key handling: fallback to `OWM_API_KEY` environment variable if `API_key` module is missing.
- `src/schedule-service/weather_data.py`: Switch NOAA XML endpoint to HTTPS and add request timeout.

### Added
- `src/gui-weather/services/noaa.py` and `src/gui-weather/services/owm.py`: New service modules to encapsulate external API calls with HTTPS, headers, and timeouts.

### Changed
- `src/gui-weather/weather_app.py` now consumes service modules for data fetching (NOAA/NWS and OWM) instead of performing network and parsing logic directly.
- Unified NOAA retrieval via `get_noaa_current_obs()` which prefers NWS v3 JSON and falls back to legacy XML.
- Prevent Tkinter image garbage collection by retaining `PhotoImage` reference when loading OWM icons.
- Lint/format scope updated in `pyproject.toml` to exclude educational/legacy code under `src/tdd/` and `src/schedule-service/`.

### Website & Docs
- `index.html`: New GitHub Pages landing page with modern, responsive design; includes project descriptions, download links, and run instructions.
- `favicon.svg`: Added custom favicon.
- SEO/Share: Added canonical URL and Open Graph/Twitter meta tags.
- `README.md`: Revamped with modern overview, quickstart, project run instructions, tooling/quality, and links.
 - UI fixes: Prevent code block overflow within project cards; update footer to state MIT license.

### Tooling
- `pyproject.toml`: Migrated Ruff to `[tool.ruff.lint]` sections; enabled quotes rule (`Q`) aligned with Black; preserved excludes and line length.
- `.editorconfig`: Added for consistent editor settings (UTF‑8, LF, 4‑space indent, 100‑col wrap).

### Enhancements
- `services/noaa.py`: Improved NWS v3 mapping (wind, visibility, pressure conversions) and added `_urlopen_with_retry()` with exponential backoff; used for both NWS JSON and XML fallback.

### Notes
- NOAA legacy XML endpoints may be deprecated or unreliable. A future change will migrate to NWS v3 JSON or add robust error handling/retries.
