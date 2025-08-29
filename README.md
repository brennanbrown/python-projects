# Python Projects

A curated set of production-ready Python mini‑projects showcasing GUI development, API integrations, testing, and design principles. The codebase emphasizes reliability, maintainability, and modern tooling.

• Live Site: https://brennanbrown.github.io/python-projects  
• Repository: https://github.com/brennanbrown/python-projects  
• Resume (PDF): https://brennanbrown.ca/Resume.pdf

## Highlights

- **Modern tooling**: pytest, Black, Ruff, mypy, GitHub Actions CI
- **Security & robustness**: HTTPS, timeouts, custom User‑Agent, retry/backoff
- **Typed and modular**: service layers for external APIs, built‑in typing
- **Python targets**: 3.11/3.12/3.13

## Quickstart

```bash
git clone https://github.com/brennanbrown/python-projects.git
cd python-projects

python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

pytest -q  # verify everything is green
```

## Projects

### GUI Weather App (Tkinter)
- Path: `src/gui-weather/`
- Description: Cross‑platform Tkinter GUI fetching live weather from NOAA/NWS and OpenWeatherMap via a clean service layer. Uses HTTPS, timeouts, custom headers, and a unified NOAA fetcher (NWS v3 JSON with legacy XML fallback).
- Run:
  ```bash
  export OWM_API_KEY=<your_api_key>   # Windows: set OWM_API_KEY=<your_api_key>
  python src/gui-weather/weather_app.py
  ```

### Schedule Service
- Path: `src/schedule-service/`
- Description: Generates an HTML weather report; demonstrates basic scheduling and email sending.
- Run:
  ```bash
  python src/schedule-service/create_html.py
  # Optional demo
  python src/schedule-service/task_scheduler.py
  ```

### TDD Examples
- Path: `src/tdd/`
- Description: Focused exercises using pytest and unittest.mock (fixtures, monkeypatching, mocking).
- Run tests:
  ```bash
  pytest -q
  ```

### Design Patterns: Maze
- Path: `src/design-patterns/`
- Description: Demonstrates architecture/design principles through a maze implementation.
- Run (if a module entry point exists):
  ```bash
  python -m src.design-patterns.maze
  ```

### Breakpoints & OOP Examples
- Paths: `src/breakpoints/`, `src/example_oop.py`
- Description: Small scripts for debugging and OOP exploration.
- Run:
  ```bash
  python src/breakpoints/breakpoint_inheritance.py
  python src/breakpoints/breakpoint_two_classes.py
  python src/example_oop.py
  ```

## Tooling & Quality

- **Testing**: `pytest` with clean suites (currently 40 passing tests)
- **Formatting**: Black (100‑column line length) + `.editorconfig`
- **Linting**: Ruff (`E`, `F`, `I`, `UP`, `Q`) including import sorting and quote consistency
- **Typing**: mypy with practical defaults
- **CI**: GitHub Actions for linting and tests on modern Python versions

## Notable Design Choices

- `src/gui-weather/services/noaa.py`: `get_noaa_current_obs()` prefers NWS v3 JSON and falls back to legacy XML; includes conversions for wind, visibility, and pressure plus retry/backoff.
- `src/gui-weather/services/owm.py`: HTTPS with timeouts and headers; returns sunrise/sunset data.
- `src/gui-weather/weather_app.py`: GUI logic separated from API logic; fixes Tkinter image GC by retaining `PhotoImage` references.

## Links

- **GitHub Pages**: https://brennanbrown.github.io/python-projects  
- **Repository**: https://github.com/brennanbrown/python-projects  
- **Changelog**: [`CHANGELOG.md`](CHANGELOG.md)

## License

This repository is licensed under the terms of the MIT License. See [`LICENSE`](LICENSE).
