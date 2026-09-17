# FastAPI entry point.
#
# Build the app, include every router under /api, and serve the built React app
# (frontend/dist) as static files so the whole thing runs on one HTTPS origin --
# no CORS needed for real phone/laptop usage. Enable CORS only when running the
# Vite dev server separately (ENV=development). Start/stop the APScheduler job
# (periodic Plaid re-sync) on app startup/shutdown.
#
# Run with: uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-certfile <path> --ssl-keyfile <path>
