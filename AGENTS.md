# AGENTS.md

## Run Dashboard
```bash
py ./app.py
```
Set `DEV_MODE=1` or `DEV_MODE=True` in `.env` for hot-reload.

## Download Data
```bash
python src/data_processing/get_data.py
```
Downloads from Google Drive (ID in `src/config.py`).

## Dependencies
```bash
pip install -r requirements.txt
```

## Tech Stack
- Dash + dash-mantine-components (UI)
- SQLite (`Data/db.sqlite3`) + DuckDB (`Data/db.duckdb`)
- gdown (Google Drive downloads)

## Data Flow
- Raw CSV → `Data/Raw/`
- Processed CSV → `Data/Processed/`
- DuckDB loads from Processed CSVs via `read_csv_auto()`

## Key Files
- `app.py` - Main Dash entry
- `src/config.py` - Paths, data URL, DB locations
- `src/dashboard/pages/` - Dash pages (home.py, objectives.py, analisis.py)
- `Data/Processed/schemas.sql` - Original table schemas (may differ from current CSVs)

## Common Issues
- **CSV type mismatches**: DuckDB's `read_csv_auto` infers types from data. Some CSVs have strings ("True") in INTEGER columns (e.g., `is_starter` in player_games, `team_1`/`team_2` in features). When recreating DuckDB, use `read_csv_auto` without type hints, or fix CSV data first.
- **DuckDB creation**: Use `CREATE TABLE x AS SELECT * FROM read_csv_auto('path')` - don't specify column types manually unless CSV data is clean.