# Football API Proxy

This repository contains a small FastAPI app that proxies parts of the API-Football (api-sports) API.

Docker
------
Build the image locally:

```powershell
docker build -t football_api:latest .
```

Run with Docker:

```powershell
docker run --rm -p 8000:8000 --env-file .env football_api:latest
```

Run with docker-compose:

```powershell
docker-compose up --build -d
```

Environment
-----------
Copy `.env.example` to `.env` and fill in your API key:

```
API_SPORTS_KEY=your_api_key_here
API_SPORTS_HOST=v3.football.api-sports.io
```

Notes
-----
- The app exposes endpoints under `/football` (for example `/football/countries/{name}/teams`).
- The container healthcheck pings `/`.
- If you are using the RapidAPI gateway rather than direct api-sports, you may need to change header names in `app/http_client.py` from `x-apisports-key`/`x-apisports-host` to `x-rapidapi-key`/`x-rapidapi-host`.

Troubleshooting
---------------
- If requests fail with 401/403, double-check your API key and header format.
- To see logs from the container:

```powershell
docker-compose logs -f
```

Security
--------
Don't commit your real `.env` file to version control. Use `.env.example` as a template.
