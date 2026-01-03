# simple_app.py - COMPLETE WITH ALL 6 STEPS AND LOADING
from fastapi import FastAPI, Query, Form
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import time

app = FastAPI()
DEEPSEEK_KEY = "sk-8dadf46bd95c47f88e8cb1fb4cd1f89e"

def layout(title: str, content: str) -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} | Prompts Alchemy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #8b5cf6;
            --primary-hover: #7c3aed;
        }}
        
        [role="button"], button, .btn-primary {{
            background: var(--primary);
            border-color: var(--primary);
        }}
        
        a {{ color: var(--primary); }}
        a:hover {{ color: var(--primary-hover); }}
        
        /* Cards */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .step-card {{
            padding: 1.5rem;
            border: 2px solid #e5e7eb;
            border-radius: 0.75rem;
            text-align: center;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
        }}
        
        .step-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .step-card i {{
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }}
        
        /* Loading bar */
        .loading-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            margin: 2rem 0;
            overflow: hidden;
        }}
        
        .loading-progress {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), #a78bfa);
            border-radius: 4px;
            animation: loading 2s infinite;
            width: 60%;
        }}
        
        @keyframes loading {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(350%); }}
        }}
        
        /* Step indicator */
        .steps {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 2rem 0;
        }}
        
        .step {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        .step.active {{
            background: var(--primary);
            color: white;
        }}

        
    :root {{
        --primary: #8b5cf6;
        --primary-hover: #7c3aed;
    }}
    
    /* ... existing CSS ... */
    
        /* RESULT BOX FIXES */
    .result-box {{
        background: #f8fafc !important;
        border: 2px solid #e5e7eb !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 0.5rem !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        white-space: pre-wrap !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        text-align: left !important;
        color: #1f2937 !important;
        overflow-x: auto;
    }}
    
    .result-box strong {{
        color: var(--primary);
        font-weight: bold;
    }}
    
    /* Make sure the enhanced prompt box has good contrast */
    .enhanced-prompt {{
        background: #f0f9ff;
        border: 2px solid var(--primary);
        border-radius: 0.75rem;
    }}

    /* SIMPLE ALIGNMENT FIX */
    .result-box, .result-box * {{
        text-align: left !important;
        text-align-last: left !important;
    }}

    /* Force left alignment in all containers */
    main .container .result-box {{
        text-align: left !important;
    }}
</style>
</head>
<body style="background: white;">
<nav style="padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
    <div class="container">
        <a href="/" style="text-decoration: none; font-size: 1.25rem; font-weight: bold; color: var(--primary);">
            <i class="fas fa-flask"></i> Prompts Alchemy
        </a>
        <span style="float: right;">
            <a href="/" style="margin-right: 1rem;">Home</a>
            <a href="/wizard">Prompt Wizard</a>
        </span>
    </div>
</nav>

<main class="container" style="padding: 2rem 0; min-height: 80vh;">
    {content}
</main>

<footer style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p>Prompt Wizard • No JavaScript • Pure Python & HTML</p>
</footer>
</body>
</html>'''



# Add this debug endpoint to see the full layout
@app.get("/debug-layout")
async def debug_layout():
    # Show what layout() produces with minimal content
    test_content = "<h1>Test</h1>"
    full_html = layout("Test", test_content)
    
    # Return first 2000 chars to see navbar
    return HTMLResponse(f"<pre>{full_html[:2000]}</pre>")



# ========== DASHBOARD ==========
@app.get("/")
async def home():
    content = '''
    <div style="text-align: center; padding: 4rem 0;">
        <h1 style="color: var(--primary);">
            <i class="fas fa-flask"></i><br>
            Prompts Alchemy
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            AI tools for content creators. Start with Prompt Wizard.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="/wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-hat-wizard"></i> Start Prompt Wizard
            </a>
        </div>
        
        <div class="card-grid">
            <div class="step-card">
                <i class="fas fa-hat-wizard"></i>
                <h3>Prompt Wizard</h3>
                <p>Create perfect AI prompts</p>
                <span style="background: var(--primary); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.9rem;">Ready</span>
            </div>
            
            <div class="step-card" style="opacity: 0.7;">
                <i class="fas fa-fish"></i>
                <h3>Hook Wizard</h3>
                <p>Generate viral hooks</p>
                <span style="background: #6b7280; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.9rem;">Soon</span>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Home", content))

# ========== STEP 1: GOAL ==========
@app.get("/wizard")
async def step1():
    content = '''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step active">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 1: Choose Your Goal</h1>
        <p style="text-align: center; color: #6b7280;">
            What do you want the AI to help you with?
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step2?goal=explain" class="step-card">
                <i class="fas fa-comment-alt"></i>
                <h3>Explain</h3>
                <p>Break down complex topics</p>
            </a>
            
            <a href="/wizard/step2?goal=create" class="step-card">
                <i class="fas fa-lightbulb"></i>
                <h3>Create</h3>
                <p>Generate new content</p>
            </a>
            
            <a href="/wizard/step2?goal=analyze" class="step-card">
                <i class="fas fa-chart-bar"></i>
                <h3>Analyze</h3>
                <p>Review data or text</p>
            </a>
            
            <a href="/wizard/step2?goal=solve" class="step-card">
                <i class="fas fa-puzzle-piece"></i>
                <h3>Solve</h3>
                <p>Find solutions to problems</p>
            </a>
            
            <a href="/wizard/step2?goal=brainstorm" class="step-card">
                <i class="fas fa-brain"></i>
                <h3>Brainstorm</h3>
                <p>Generate ideas</p>
            </a>
            
            <a href="/wizard/step2?goal=edit" class="step-card">
                <i class="fas fa-edit"></i>
                <h3>Edit/Improve</h3>
                <p>Refine existing content</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" role="button" class="secondary">Cancel</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 1: Goal", content))

# ========== STEP 2: AUDIENCE ==========
@app.get("/wizard/step2")
async def step2(goal: str = Query("explain")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step active">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 2: Choose Your Audience</h1>
        <p style="text-align: center; color: #6b7280;">
            Who will read or use this?
        </p>
        
        <p style="text-align: center;"><strong>Goal:</strong> {goal.title()}</p>
        
        <div class="card-grid">
            <a href="/wizard/step3?goal={goal}&audience=general" class="step-card">
                <i class="fas fa-users"></i>
                <h3>General Public</h3>
                <p>Anyone can understand</p>
            </a>
            
            <a href="/wizard/step3?goal={goal}&audience=experts" class="step-card">
                <i class="fas fa-user-tie"></i>
                <h3>Experts</h3>
                <p>Deep knowledge assumed</p>
            </a>
            
            <a href="/wizard/step3?goal={goal}&audience=students" class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Students</h3>
                <p>Learning-focused</p>
            </a>
            
            <a href="/wizard/step3?goal={goal}&audience=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Professional audience</p>
            </a>
            
            <a href="/wizard/step3?goal={goal}&audience=technical" class="step-card">
                <i class="fas fa-cogs"></i>
                <h3>Technical</h3>
                <p>Developers, engineers</p>
            </a>
            
            <a href="/wizard/step3?goal={goal}&audience=myself" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Just Me</h3>
                <p>Personal use only</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 2: Audience", content))

# ========== STEP 3: PLATFORM ==========
@app.get("/wizard/step3")
async def step3(goal: str = Query("explain"), audience: str = Query("general")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step active">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 3: Choose Platform</h1>
        <p style="text-align: center; color: #6b7280;">
            Which AI will you use this prompt with?
        </p>
        
        <p style="text-align: center;">
            <strong>Goal:</strong> {goal.title()} • 
            <strong>Audience:</strong> {audience.title()}
        </p>
        
       # In the STEP 3: PLATFORM section, update the card_grid:

<div class="card-grid">
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=chatgpt" class="step-card">
        <i class="fas fa-comment"></i>
        <h3>ChatGPT</h3>
        <p>OpenAI's text AI</p>
    </a>
    
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=claude" class="step-card">
        <i class="fas fa-robot"></i>
        <h3>Claude</h3>
        <p>Anthropic's thoughtful AI</p>
    </a>
    
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=gemini" class="step-card">
        <i class="fas fa-search"></i>
        <h3>Gemini</h3>
        <p>Google's multimodal AI</p>
    </a>
    
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=deepseek" class="step-card">
        <i class="fas fa-bolt"></i>
        <h3>DeepSeek</h3>
        <p>Fast and capable</p>
    </a>
    
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=dalle" class="step-card">
        <i class="fas fa-palette"></i>
        <h3>DALL-E</h3>
        <p>OpenAI's image generator</p>
    </a>
    
    <a href="/wizard/step4?goal={goal}&audience={audience}&platform=midjourney" class="step-card">
        <i class="fas fa-paint-brush"></i>
        <h3>Midjourney</h3>
        <p>Discord image generator</p>
    </a>
</div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step2?goal={goal}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 3: Platform", content))

# ========== STEP 4: STYLE ==========
@app.get("/wizard/step4")
async def step4(goal: str = Query("explain"), audience: str = Query("general"), platform: str = Query("chatgpt")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step active">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 4: Choose Style</h1>
        <p style="text-align: center; color: #6b7280;">
            How should the AI structure its response?
        </p>
        
        <p style="text-align: center;">
            <strong>Goal:</strong> {goal.title()} • 
            <strong>Audience:</strong> {audience.title()} • 
            <strong>Platform:</strong> {platform.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=direct" class="step-card">
                <i class="fas fa-bullseye"></i>
                <h3>Direct</h3>
                <p>Straight to the point</p>
            </a>
            
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=structured" class="step-card">
                <i class="fas fa-list"></i>
                <h3>Structured</h3>
                <p>Organized with headings</p>
            </a>
            
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=creative" class="step-card">
                <i class="fas fa-paint-brush"></i>
                <h3>Creative</h3>
                <p>Imaginative and free</p>
            </a>
            
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=technical" class="step-card">
                <i class="fas fa-cogs"></i>
                <h3>Technical</h3>
                <p>Detailed and precise</p>
            </a>
            
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=conversational" class="step-card">
                <i class="fas fa-comments"></i>
                <h3>Conversational</h3>
                <p>Natural dialogue</p>
            </a>
            
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style=stepbystep" class="step-card">
                <i class="fas fa-footsteps"></i>
                <h3>Step-by-Step</h3>
                <p>Guided instructions</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step3?goal={goal}&audience={audience}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 4: Style", content))

# ========== STEP 5: TONE ==========
@app.get("/wizard/step5")
async def step5(goal: str = Query("explain"), audience: str = Query("general"), platform: str = Query("chatgpt"), style: str = Query("direct")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step active">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 5: Choose Tone</h1>
        <p style="text-align: center; color: #6b7280;">
            What mood or attitude should it use?
        </p>
        
        <p style="text-align: center;">
            <strong>Goal:</strong> {goal.title()} • 
            <strong>Audience:</strong> {audience.title()} • 
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Style:</strong> {style.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=professional" class="step-card">
                <i class="fas fa-suitcase"></i>
                <h3>Professional</h3>
                <p>Formal, business-like</p>
            </a>
            
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=friendly" class="step-card">
                <i class="fas fa-smile"></i>
                <h3>Friendly</h3>
                <p>Warm, approachable</p>
            </a>
            
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=authoritative" class="step-card">
                <i class="fas fa-crown"></i>
                <h3>Authoritative</h3>
                <p>Confident, expert-like</p>
            </a>
            
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=educational" class="step-card">
                <i class="fas fa-book"></i>
                <h3>Educational</h3>
                <p>Teaching, explanatory</p>
            </a>
            
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=enthusiastic" class="step-card">
                <i class="fas fa-fire"></i>
                <h3>Enthusiastic</h3>
                <p>Energetic, passionate</p>
            </a>
            
            <a href="/wizard/step6?goal={goal}&audience={audience}&platform={platform}&style={style}&tone=neutral" class="step-card">
                <i class="fas fa-balance-scale"></i>
                <h3>Neutral</h3>
                <p>Objective, unbiased</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step4?goal={goal}&audience={audience}&platform={platform}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 5: Tone", content))

# ========== STEP 6: ENTER PROMPT ==========
@app.get("/wizard/step6")
async def step6(
    goal: str = Query("explain"),
    audience: str = Query("general"),
    platform: str = Query("chatgpt"),
    style: str = Query("direct"),
    tone: str = Query("professional")
):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step active">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 6: Enter Your Prompt</h1>
        <p style="text-align: center; color: #6b7280;">
            Type your initial prompt below
        </p>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Selections:</h3>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 1rem 0;">
                <div><strong>Goal:</strong><br>{goal.title()}</div>
                <div><strong>Audience:</strong><br>{audience.title()}</div>
                <div><strong>Platform:</strong><br>{platform.title()}</div>
                <div><strong>Style:</strong><br>{style.title().replace("Stepbystep", "Step-by-Step")}</div>
                <div><strong>Tone:</strong><br>{tone.title()}</div>
            </div>
        </div>
        
        <form action="/process" method="POST">
            <input type="hidden" name="goal" value="{goal}">
            <input type="hidden" name="audience" value="{audience}">
            <input type="hidden" name="platform" value="{platform}">
            <input type="hidden" name="style" value="{style}">
            <input type="hidden" name="tone" value="{tone}">
            
            <label for="prompt">
                <strong>Your Prompt:</strong>
                <p style="color: #6b7280; margin: 0.5rem 0;">What do you want to ask the AI?</p>
            </label>
            <textarea id="prompt" name="prompt" rows="8" placeholder="Type your prompt here..." required style="width: 100%; padding: 1rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-family: monospace;"></textarea>
            
            <div style="text-align: center; margin: 2rem 0;">
                <button type="submit" style="padding: 1rem 3rem; font-size: 1.2rem;">
                    <i class="fas fa-magic"></i> Generate Enhanced Prompt
                </button>
                <p style="margin-top: 1rem; color: #6b7280;">
                    <i class="fas fa-clock"></i> This will take 10-30 seconds
                </p>
            </div>
        </form>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step5?goal={goal}&audience={audience}&platform={platform}&style={style}" 
               role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 6: Enter Prompt", content))

# ========== PROCESS WITH LOADING BAR ==========
@app.post("/process")
async def process_prompt(
    goal: str = Form(...),
    audience: str = Form(...),
    platform: str = Form(...),
    style: str = Form(...),
    tone: str = Form(...),
    prompt: str = Form(...)
):
    # Show loading page immediately
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-hat-wizard"></i>
        </div>
        
        <h1 style="color: var(--primary);">Working AI Magic...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Enhancing your prompt for {platform.title()} with {tone} tone...
        </p>
        
        <!-- ANIMATED LOADING BAR -->
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            Free AI can be slow. Please wait 15-30 seconds...
        </p>
        
        <!-- Auto-refresh to result after 2 seconds -->
        <meta http-equiv="refresh" content="2;url=/result?goal={goal}&audience={audience}&platform={platform}&style={style}&tone={tone}&prompt={prompt}">
    </div>
    '''
    
    return HTMLResponse(layout("Processing...", loading_content))

# ========== RESULT ==========
# ========== RESULT ==========
@app.get("/result")
async def show_result(
    goal: str = Query(...),
    audience: str = Query(...),
    platform: str = Query(...),
    style: str = Query(...),
    tone: str = Query(...),
    prompt: str = Query(...)
):
    # TEST MODE - Set to False for real API
    TEST_MODE = False
    TURQUOISE = "#0d96c1"
    TURQUOISE_LIGHT = "#ecfeff"
    TURQUOISE_DARK = "#0c4a6e"
    
    try:
        if TEST_MODE:
            # Mock enhanced prompt
            ai_text = f'''As a prompt engineering expert specializing in {platform}, craft a detailed prompt that achieves the goal of "{goal}" for an audience of "{audience}". 

Use a {tone} tone and {style} style. Structure the prompt to include:
1. Clear context about the desired outcome
2. Specific instructions tailored to {platform}'s capabilities
3. Guidance on format, length, and key elements to include
4. Considerations for engaging the target audience effectively

Ensure the enhanced prompt is actionable, well-structured, and optimized for the best possible results from {platform}.'''
        else:
                        # Real API call with BETTER prompt
            system_prompt = f"""You are an elite prompt engineer. Transform this basic prompt into a highly effective, specific prompt for {platform}.

USER'S CONTEXT:
- Goal: {goal}
- Target audience: {audience}
- Desired style: {style}
- Desired tone: {tone}
- Original prompt: "{prompt}"

YOUR TASK: Create a SINGLE, IMPROVED prompt that:
1. Is optimized specifically for {platform}
2. Will resonate with {audience}
3. Achieves the "{goal}" goal effectively
4. Uses {tone} tone throughout
5. Is structured in a {style} way
6. Includes specific, actionable instructions
7. Sets clear expectations for output format

DO NOT include explanations, notes, or markdown. Output ONLY the enhanced prompt text."""
            
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=45
            )
            
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}")
            
            ai_text = response.json()["choices"][0]["message"]["content"]
        
        # Build beautiful result page
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; color: {TURQUOISE};">
            <i class="fas fa-check-circle"></i>
        </div>
        <h1 style="color: {TURQUOISE};">Prompt Enhanced!</h1>
        <p style="color: #64748b;">For <strong>{platform.title()}</strong> • <strong>{audience.title()}</strong> • <strong>{tone.title()}</strong> tone</p>
    </div>
    
    <!-- Original Prompt Card -->
    <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; border: 2px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <div style="background: #94a3b8; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                <i class="fas fa-pencil-alt"></i>
            </div>
            <h3 style="margin: 0; color: #64748b;">Original Prompt</h3>
        </div>
        
        <div style="font-size: 1rem; line-height: 1.5; padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 4px solid #94a3b8; color: #475569;">
            {prompt}
        </div>
    </div>
    
    <!-- Enhanced Prompt Card -->
    <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; border: 2px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <div style="background: {TURQUOISE}; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                <i class="fas fa-star"></i>
            </div>
            <h3 style="margin: 0; color: {TURQUOISE};">Enhanced Prompt</h3>
            <span style="font-size: 0.8rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 4px; margin-left: auto;">
                <i class="fas fa-mouse-pointer"></i> Click to select
            </span>
        </div>
        
        <div style="user-select: all; -webkit-user-select: all; -moz-user-select: all;
                    font-size: 1.1rem; line-height: 1.5; padding: 1.5rem; background: {TURQUOISE_LIGHT}; 
                    border-radius: 8px; border-left: 4px solid {TURQUOISE}; color: {TURQUOISE_DARK}; 
                    font-family: 'Georgia', serif; white-space: pre-wrap; cursor: text;">
            {ai_text}
        </div>
        
        <div style="font-size: 0.8rem; color: #6b7280; margin-top: 1rem; text-align: center; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
            <i class="fas fa-clipboard"></i> Select text above, then Ctrl+C / Cmd+C to copy
        </div>
    </div>
    
    <!-- Context Info -->
    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin: 2rem 0; border: 2px dashed {TURQUOISE};">
        <h3 style="color: {TURQUOISE}; margin-bottom: 1rem; text-align: center;">
            <i class="fas fa-cog"></i> Prompt Context
        </h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.25rem; font-weight: 600;">
                    <i class="fas fa-bullseye"></i> Goal
                </div>
                <div style="font-size: 0.9rem; color: #475569;">{goal.title()}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.25rem; font-weight: 600;">
                    <i class="fas fa-users"></i> Audience
                </div>
                <div style="font-size: 0.9rem; color: #475569;">{audience.title()}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.25rem; font-weight: 600;">
                    <i class="fas fa-robot"></i> Platform
                </div>
                <div style="font-size: 0.9rem; color: #475569;">{platform.title()}</div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 3rem;">
        <a href="/wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-hat-wizard"></i> Create Another Prompt
        </a>
        <a href="/" role="button" style="background: #64748b; border-color: #64748b;">
            <i class="fas fa-home"></i> Dashboard
        </a>
    </div>
</div>
'''
        
    except Exception as e:
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> Error</h1>
    <p>{str(e)}</p>
    <a href="/" role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Start Over</a>
</div>
'''
    
    return HTMLResponse(layout("Result", result_content))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
