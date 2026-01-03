# layout.py - Thumbnail Wizard Layout
def layout(title: str, content: str) -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} | Thumbnail Wizard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    
    
        <!-- Navigation -->
    <nav class="suite-nav">
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <!-- Logo/Brand -->
                <div>
                    <a href="/" class="brand" style="text-decoration: none; font-size: 1.5rem;">
                        <i class="fas fa-flask"></i> Prompts Alchemy
                    </a>
                </div>
                
                <!-- Links - All 6 pages -->
                <div style="display: flex; gap: 1.5rem; align-items: center;">
                    <!-- Home -->
                    <a href="/" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-home"></i> Home
                    </a>
                    
                    <!-- Wizard 1: Prompt -->
                    <a href="/prompt-wizard" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-hat-wizard"></i> Prompt Wizard
                    </a>
                    
                    <!-- Wizard 2: Thumbnail -->
                    <a href="/thumbnail-wizard" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-image"></i> Thumbnail Wizard
                    </a>
                    
                    <!-- Wizard 3: Video -->
                    <a href="/video-wizard" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-video"></i> Video Wizard
                    </a>
                    
                    <!-- Wizard 4: Hook -->
                    <a href="/hook-wizard" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-fish"></i> Hook Wizard
                    </a>
                    
                    <!-- Wizard 5: Document -->
                    <a href="/document-wizard" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-file-contract"></i> Document Wizard
                    </a>
                    
                    <!-- Pricing -->
                    <a href="#pricing" style="color: #374151; text-decoration: none; font-weight: 500;">
                        <i class="fas fa-tag"></i> Pricing
                    </a>
                    
                    <!-- Get Started Button -->
                    <a href="#pricing" role="button" style="background: var(--primary); color: white; padding: 0.5rem 1.5rem;">
                        Get Started
                    </a>
                </div>
            </div>
        </div>
    </nav>
    
    
    <style>
        :root {{
            --primary: #8b5cf6;
            --primary-hover: #7c3aed;
            --secondary: #f59e0b;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --turquoise: #0d96c1;
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
        
        @media (min-width: 768px) {{
            .card-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        .step-card {{
            padding: 1.5rem;
            border: 2px solid #e5e7eb;
            border-radius: 0.75rem;
            text-align: center;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
            display: block;
            background: white;
        }}
        
        .step-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
        }}
        
        .step-card i {{
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }}
        
        /* Steps indicator */
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


        /* Better Navbar Styling */
.suite-nav {
    background: white;
    border-bottom: 2px solid #f3f4f6;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.suite-nav a {
    transition: all 0.2s ease;
    padding: 0.5rem 0;
    position: relative;
}

.suite-nav a:hover {
    color: var(--primary) !important;
}

/* Active page indicator */
.suite-nav a.active {
    color: var(--primary) !important;
    font-weight: 600;
}

.suite-nav a.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--primary);
    border-radius: 2px;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .suite-nav > .container > div {
        flex-direction: column;
        gap: 1rem;
    }
    
    .suite-nav .brand {
        font-size: 1.25rem;
    }
}


        
        
        /* Result boxes */
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
        
        .analysis-box {{
            background: #f0f9ff;
            border: 2px solid var(--turquoise);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .score-badge {{
            font-size: 3rem;
            font-weight: bold;
            color: var(--primary);
            text-align: center;
            margin: 1rem 0;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e5e7eb;
            border-radius: 5px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--primary);
            border-radius: 5px;
        }}
        
        /* Tab switching (simple no-JS version) */
        .tabs {{
            display: flex;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 2rem;
        }}
        
        .tab {{
            flex: 1;
            padding: 1rem;
            text-align: center;
            background: #f3f4f6;
            border: none;
            cursor: pointer;
            text-decoration: none;
            color: #6b7280;
        }}
        
        .tab.active {{
            background: var(--primary);
            color: white;
            font-weight: bold;
        }}
    </style>
</head>
<body style="background: white;"

<main class="container" style="padding: 2rem 0; min-height: 80vh;">
    {content}
</main>

<footer style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p>Thumbnail Wizard • No JavaScript • Pure Python & HTML</p>
</footer>
</body>
</html>'''
