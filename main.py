from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from layout import layout
import importlib.util
import sys
import os
import traceback

app = FastAPI(title="Prompts Alchemy Suite", version="1.0")

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates if needed
os.makedirs("templates", exist_ok=True)
templates = Jinja2Templates(directory="templates")
