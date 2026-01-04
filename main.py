# main.py - FOR ROOT-LEVEL WIZARDS
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import wizards directly from root
from prompt_wizard.app import app as prompt_app
from hook_wizard.app import app as hook_app
from document_wizard.app import app as document_app
from thumbnail_wizard.app import app as thumbnail_app
from video_wizard.app import app as video_app
from home_page.app import app as home_app

app = FastAPI(title="Prompts Alchemy Suite")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount all wizards
app.mount("/", home_app)  # Homepage at root
app.mount("/prompts", prompt_app)  # Your baby!
app.mount("/hooks", hook_app)
app.mount("/documents", document_app)
app.mount("/thumbnails", thumbnail_app)
app.mount("/videos", video_app)

# Health check
@app.get("/health")
async def health():
    return {"status": "alive", "wizards": 5, "flagship": "/prompts"}
