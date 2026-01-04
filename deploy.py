# main.py - The conductor for all your apps
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import your individual apps
from apps.app1.main import app as app1
from apps.app2.main import app as app2
# ... import all your apps

# Create the main application
main_app = FastAPI(title="My Apps Collection")

# Mount each app on its own path
main_app.mount("/app1", app1)
main_app.mount("/app2", app2)
# ... mount all apps

# Mount static files if needed
main_app.mount("/static", StaticFiles(directory="static"), name="static")

# Optional: Homepage
@main_app.get("/")
async def root():
    return {"message": "Welcome to my apps collection", "apps": ["/app1", "/app2"]}
