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

            from fastapi.middleware.trustedhost import TrustedHostMiddleware
            
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




loaded_wizards = []

for folder_name, mount_path in WIZARDS:
    wizard_path = f"apps/{folder_name}/app.py"
    
    print(f"\n{'='*50}")
    print(f"🚀 ATTEMPTING TO LOAD: {folder_name}")
    print(f"{'='*50}")
    print(f"1. Checking path: {wizard_path}")
    print(f"   Path exists: {os.path.exists(wizard_path)}")
    
    if not os.path.exists(wizard_path):
        print(f"⏸️  SKIPPED: {folder_name:20} | No app.py found")
        continue
    
    try:
        print(f"2. Creating import spec...")
        spec = importlib.util.spec_from_file_location(folder_name, wizard_path)
        print(f"   Spec created: {spec is not None}")
        
        wizard_module = importlib.util.module_from_spec(spec)
        sys.modules[folder_name] = wizard_module
        
        print(f"3. EXECUTING MODULE (this might fail)...")
        spec.loader.exec_module(wizard_module)  # <-- CRITICAL LINE
        print(f"   ✅ Module executed successfully!")
        
        print(f"4. Checking module attributes:")
        print(f"   • Has 'app'? {hasattr(wizard_module, 'app')}")
        print(f"   • Has 'layout' function? {hasattr(wizard_module, 'layout')}")
        print(f"   • Has 'home' function? {hasattr(wizard_module, 'home')}")
        print(f"   • All attributes: {[a for a in dir(wizard_module) if not a.startswith('_')][:10]}...")
        
        # STRATEGY 1: Check for FastAPI 'app' object (most common)
        if hasattr(wizard_module, 'app'):
            print(f"5. Mounting FastAPI app at '{mount_path}'...")
            app.mount(mount_path, wizard_module.app)
            status = "✅ MOUNTED (FastAPI app)"
            
        # STRATEGY 2: Check for APIRouter 'router' object
        elif hasattr(wizard_module, 'router'):
            app.include_router(wizard_module.router, prefix=mount_path)
            status = "✅ ROUTER (APIRouter)"
            
        # STRATEGY 3: Check for function-based endpoints
        elif hasattr(wizard_module, 'home'):
            print(f"5. Creating route for function at '{mount_path}'...")
            @app.get(mount_path + "/")
            async def wizard_home():
                return await wizard_module.home()
            status = "✅ FUNCTION (home endpoint)"
            
        # STRATEGY 4: Special handling for home-page
        elif folder_name == "home-page":
            status = "🏠 HOME (handled separately)"
            
        else:
            status = "⚠️  UNKNOWN (no app/router found)"
        
        loaded_wizards.append((folder_name, mount_path, status))
        print(f"6. RESULT: {status}")
        print(f"   Path: {folder_name:20} -> {mount_path}")
        
    except Exception as e:
        print(f"❌❌❌ LOAD FAILED!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        print(f"   Full traceback:")
        import traceback
        traceback.print_exc()
        
        error_msg = str(e)[:80] + "..." if len(str(e)) > 80 else str(e)
        print(f"❌ FAILED:  {folder_name:20} | Error: {error_msg}")

print("\n" + "=" * 60)
print(f"📊 FINAL SUMMARY: {len(loaded_wizards)}/{len(WIZARDS)} wizards loaded")
if loaded_wizards:
    print("Successfully loaded:")
    for name, path, status in loaded_wizards:
        print(f"  • {name:20} -> {path} ({status})")
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






# ============================================
# DEBUG ENDPOINTS
# ============================================

@app.get("/layout-check")
async def layout_check():
    """Check which wizards have duplicate layout functions"""
    import os
    
    results = {}
    wizards_to_check = [
        "prompt-wizard",
        "thumbnail-wizard", 
        "video-wizard",
        "hook-wizard",
        "document-wizard", 
        "home-page"
    ]
    
    for wizard in wizards_to_check:
        path = f"apps/{wizard}/app.py"
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                has_def_layout = 'def layout(' in content
                has_import_layout = 'from layout import layout' in content
                results[wizard] = {
                    "has_own_layout_function": has_def_layout,
                    "imports_root_layout": has_import_layout,
                    "status": "❌ HAS DUPLICATE LAYOUT" if has_def_layout else "✅ OK"
                }
        else:
            results[wizard] = {"error": "app.py not found"}
    
    return results

@app.get("/debug-loaded")
async def debug_loaded():
    """Show which wizards are actually loaded"""
    return {
        "loaded_wizards": loaded_wizards,
        "total": len(loaded_wizards)
    }




# TEST: Force create a simple route at root level
@app.get("/test-simple")
async def test_simple():
    return {"message": "FastAPI is working", "time": datetime.now().isoformat()}

# Also override the default 404
@app.exception_handler(404)
async def custom_404(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "message": "Route not found",
            "requested_path": request.url.path,
            "available_routes": [route.path for route in app.routes if hasattr(route, 'path')]
        }
    )




# MANUAL MOUNT TEST (temporary)
print("\n=== MANUAL MOUNT TEST ===")

# Test prompt-wizard
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "manual_prompt", 
        "apps/prompt-wizard/app.py"
    )
    manual_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manual_module)
    
    if hasattr(manual_module, 'app'):
        app.mount("/manual-test", manual_module.app)
        print("✅ Manually mounted at /manual-test")
        print(f"  Routes in manual app: {[r.path for r in manual_module.app.routes]}")
    else:
        print("❌ No 'app' in manual module")
except Exception as e:
    print(f"❌ Manual mount failed: {e}")




@app.get("/test-wizard-content/{wizard_name}")
async def test_wizard_content(wizard_name: str):
    """Test what a wizard actually returns"""
    import importlib.util
    import requests
    
    wizard_path = f"apps/{wizard_name}/app.py"
    
    if not os.path.exists(wizard_path):
        return {"error": f"Wizard not found: {wizard_path}"}
    
    try:
        # Load the wizard module
        spec = importlib.util.spec_from_file_location("test_wizard", wizard_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check what the home route returns
        if hasattr(module, 'app'):
            # Get the first route (usually home)
            routes = module.app.routes
            first_route = None
            for route in routes:
                if hasattr(route, 'path') and route.path == "/":
                    first_route = route
                    break
            
            return {
                "wizard": wizard_name,
                "has_app": True,
                "routes_count": len(routes),
                "routes": [{"path": r.path, "methods": getattr(r, 'methods', [])} 
                          for r in routes if hasattr(r, 'path')],
                "first_route": first_route.path if first_route else None,
                "module_attributes": [a for a in dir(module) if not a.startswith('_')]
            }
        else:
            return {"error": "No app found in module"}
            
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}





@app.get("/debug-access/{wizard_name}")
async def debug_access(wizard_name: str):
    """Try to access a wizard directly through the mount"""
    import http.client
    import json
    
    # This simulates what a browser would see
    test_path = f"/{wizard_name}" if wizard_name != "home-page" else "/"
    
    return {
        "wizard": wizard_name,
        "test_path": test_path,
        "mount_point": f"https://your-site.up.railway.app{test_path}",
        "note": "Visit the above URL to test"
    }




# ============================================
# EMERGENCY DEBUG - ALWAYS WORKS
# ============================================

@app.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": datetime.now().isoformat()}

@app.get("/debug-app")
async def debug_app():
    """Debug the actual app object"""
    import inspect
    return {
        "app_id": id(app),
        "app_type": type(app).__name__,
        "app_title": getattr(app, 'title', 'No title'),
        "app_routes_count": len(app.routes),
        "all_routes": [
            {
                "path": route.path,
                "name": getattr(route, 'name', 'No name'),
                "methods": getattr(route, 'methods', []),
                "is_mount": hasattr(route, 'app')
            }
            for route in app.routes if hasattr(route, 'path')
        ],
        "loaded_wizards_count": len(loaded_wizards) if 'loaded_wizards' in locals() else "Not found",
        "current_file": __file__,
        "main_module": __name__
    }

# Force register a simple route that MUST work
@app.get("/")
async def force_root():
    return {"message": "FORCED ROOT ROUTE", "app": "main.py"}

# Also mount a simple test app
from fastapi import FastAPI as FastAPI2
from fastapi.responses import HTMLResponse

test_app = FastAPI2()

@test_app.get("/")
async def test_app_home():
    return HTMLResponse("<h1>Test App Works</h1>")

app.mount("/test-app", test_app)




@app.get("/debug-current/{wizard_name}")
async def debug_current(wizard_name: str):
    """Debug what's actually accessible right now"""
    return {
        "test_urls": [
            f"https://your-site.up.railway.app/{wizard_name}/",
            f"https://your-site.up.railway.app/{wizard_name}/wizard",
            f"https://your-site.up.railway.app/{wizard_name}/wizard/step2?goal=explain"
        ],
        "note": "Try these exact URLs with trailing slashes where shown"
    }








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
