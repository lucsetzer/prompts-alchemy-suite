# main.py - FLEXIBLE orchestrator for mixed wizard styles
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

# Your exact wizard list
WIZARDS = [
    ("home-page", "/"),                    # One-pager at root
    ("prompt-wizard", "/prompt-wizard"),
    ("document-wizard", "/document-wizard"),
    ("hook-wizard", "/hook-wizard"),
    ("video-wizard", "/video-wizard"),
    ("thumbnail-wizard", "/thumbnail-wizard"),
]

print("=" * 60)
print("🚀 PROMPTS ALCHEMY SUITE - Loading Wizards")
print("=" * 60)

# Track what loads successfully
loaded_wizards = []

for folder_name, mount_path in WIZARDS:
    wizard_path = f"apps/{folder_name}/app.py"
    
    if not os.path.exists(wizard_path):
        print(f"⏸️  SKIPPED: {folder_name:20} | No app.py found")
        continue
    
    try:
        # Dynamically import the wizard
        spec = importlib.util.spec_from_file_location(folder_name, wizard_path)
        wizard_module = importlib.util.module_from_spec(spec)
        sys.modules[folder_name] = wizard_module
        spec.loader.exec_module(wizard_module)
        
        # STRATEGY 1: Check for FastAPI 'app' object (most common)
        if hasattr(wizard_module, 'app'):
            app.mount(mount_path, wizard_module.app)
            status = "✅ MOUNTED (FastAPI app)"
            
        # STRATEGY 2: Check for APIRouter 'router' object
        elif hasattr(wizard_module, 'router'):
            app.include_router(wizard_module.router, prefix=mount_path)
            status = "✅ ROUTER (APIRouter)"
            
        # STRATEGY 3: Check for function-based endpoints
        elif hasattr(wizard_module, 'home'):
            # Handle function-based wizards
            @app.get(mount_path + "/")
            async def wizard_home():
                return await wizard_module.home()
            status = "✅ FUNCTION (home endpoint)"
            
        # STRATEGY 4: Special handling for home-page
        elif folder_name == "home-page":
            # We'll handle home separately
            status = "🏠 HOME (handled separately)"
            
        else:
            status = "⚠️  UNKNOWN (no app/router found)"
        
        loaded_wizards.append((folder_name, mount_path, status))
        print(f"{status:25} | {folder_name:20} -> {mount_path}")
        
    except Exception as e:
        error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
        print(f"❌ FAILED:  {folder_name:20} | Error: {error_msg}")
        # print(traceback.format_exc())  # Uncomment for debugging

print("=" * 60)
print(f"📊 Summary: {len(loaded_wizards)}/{len(WIZARDS)} wizards loaded")
print("=" * 60)

# Special handling for home-page
def load_home_page():
    """Try to load the home page from various possible locations"""
    home_paths = [
        "apps/home-page/app.py",
        "apps/home-page/home.py", 
        "apps/home-page/main.py",
    ]
    
    for path in home_paths:
        if os.path.exists(path):
            try:
                spec = importlib.util.spec_from_file_location("home_page", path)
                home_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(home_module)
                
                # Check what the home module provides
                if hasattr(home_module, 'home_page'):
                    return home_module.home_page
                elif hasattr(home_module, 'home'):
                    return home_module.home
                elif hasattr(home_module, 'layout'):
                    # Create a simple home page using their layout
                    def simple_home():
                        from layout import layout
                        content = '''
                        <div style="text-align: center; padding: 4rem;">
                            <h1>Welcome to Prompts Alchemy</h1>
                            <p>Your AI Wizard Suite is running!</p>
                        </div>
                        '''
                        return HTMLResponse(layout("Home", content))
                    return simple_home
                    
            except Exception as e:
                continue
    
    # Fallback home page
    from layout import layout
    def fallback_home():
        content = '''
        <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
            <h1 style="color: var(--primary);">🎉 Prompts Alchemy Suite</h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin: 2rem 0;">
                Your AI wizard suite is successfully deployed!
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 3rem 0;">
        '''
        
        for wizard_name, wizard_path, _ in loaded_wizards:
            if wizard_name != "home-page":
                display_name = wizard_name.replace("-", " ").title()
                content += f'''
                <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3>{display_name}</h3>
                    <a href="{wizard_path}" style="color: var(--primary);">Open Wizard →</a>
                </div>
                '''
        
        content += '''
            </div>
        </div>
        '''
        return HTMLResponse(layout("Home", content))
    
    return fallback_home

# Load and attach the home page
home_handler = load_home_page()
app.get("/")(home_handler)

# Also provide a direct /home endpoint
app.get("/home")(home_handler)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "wizards_loaded": len(loaded_wizards),
        "wizards": [w[0] for w in loaded_wizards]
    }

# Debug endpoint to see structure
@app.get("/debug/structure")
async def debug_structure():
    import json
    structure = {}
    for wizard in WIZARDS:
        folder_name, path = wizard
        wizard_dir = f"apps/{folder_name}"
        if os.path.exists(wizard_dir):
            files = os.listdir(wizard_dir)
            structure[folder_name] = {
                "path": path,
                "files": files,
                "has_app_py": "app.py" in files
            }
    return structure


@app.get("/debug/wizard-internals")
async def debug_wizard_internals():
    """Test the wizard's app.py directly"""
    import importlib.util
    import sys
    
    wizard_path = "apps/prompt-wizard/app.py"
    
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location("test_wizard", wizard_path)
        module = importlib.util.module_from_spec(spec)
        
        # Execute it
        spec.loader.exec_module(module)
        
        # Check what we got
        result = {
            "file_exists": True,
            "module_loaded": True,
            "has_app": hasattr(module, 'app'),
            "has_home": hasattr(module, 'home'),
            "all_attrs": [a for a in dir(module) if not a.startswith('_')],
        }
        
        # Try to create a minimal app if missing
        if not hasattr(module, 'app'):
            from fastapi import FastAPI
            temp_app = FastAPI()
            
            # If home function exists, add it
            if hasattr(module, 'home'):
                @temp_app.get("/")
                async def temp_home():
                    return await module.home()
            
            result["created_temp_app"] = True
            result["temp_app_routes"] = [r.path for r in temp_app.routes]
            
        return result
        
    except Exception as e:
        return {
            "file_exists": os.path.exists(wizard_path),
            "error": str(e),
            "traceback": traceback.format_exc()
        }




# ============================================
# DIRECT MOUNT TEST (FIXED VERSION)
# ============================================
print("\n" + "=" * 60)
print("🧪 DIRECT MOUNT TEST")
print("=" * 60)

try:
    # Use importlib to handle hyphen in folder name
    import importlib.util
    import sys
    
    wizard_path = "apps/prompt-wizard/app.py"
    
    # Load the module
    spec = importlib.util.spec_from_file_location("prompt_wizard_test", wizard_path)
    wizard_module = importlib.util.module_from_spec(spec)
    sys.modules["prompt_wizard_test"] = wizard_module
    spec.loader.exec_module(wizard_module)
    
    print(f"✅ Prompt wizard module loaded")
    print(f"   Has 'app' attribute? {hasattr(wizard_module, 'app')}")
    
    if hasattr(wizard_module, 'app'):
        # Mount it at a test path
        app.mount("/test-prompt", wizard_module.app)
        print(f"   ✅ Mounted at /test-prompt")
        
        # Check for duplicate layout function
        if hasattr(wizard_module, 'layout'):
            print(f"   ⚠️  WARNING: Wizard has its own layout() function!")
            print(f"   This will override the root layout. Delete it!")
        else:
            print(f"   ✅ Using root layout (good)")
            
    else:
        print(f"   ❌ No 'app' found in module")
        print(f"   Available attributes: {[a for a in dir(wizard_module) if not a.startswith('_')]}")
        
except Exception as e:
    print(f"❌ Direct mount test FAILED: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)




@app.get("/debug/wizard-check")
async def debug_wizard_check():
    """Check the prompt wizard's status"""
    import importlib.util
    import os
    
    wizard_path = "apps/prompt-wizard/app.py"
    
    if not os.path.exists(wizard_path):
        return {"error": f"File not found: {wizard_path}"}
    
    try:
        spec = importlib.util.spec_from_file_location("debug_check", wizard_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return {
            "wizard_exists": True,
            "has_app": hasattr(module, 'app'),
            "has_layout_function": hasattr(module, 'layout'),
            "app_type": type(module.app).__name__ if hasattr(module, 'app') else None,
            "all_attrs": [a for a in dir(module) if not a.startswith('_')]
        }
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}






if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("🌐 Server starting: http://localhost:8000")
    print("📚 API Docs:        http://localhost:8000/docs")
    print("🏠 Home Page:       http://localhost:8000/")
    print("🩺 Health Check:    http://localhost:8000/health")
    print("🐛 Debug Info:      http://localhost:8000/debug/structure")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
