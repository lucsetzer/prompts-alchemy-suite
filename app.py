# app.py - SINGLE APP FOR EVERYTHING
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sys
import uvicorn
import requests
import re
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
import time
import uuid
import base64
from PIL import Image
import io
import json

# API Keys from environment
API_KEYS = {
    "prompt": os.getenv("PROMPT_WIZARD_API_KEY"),
    "thumbnail": os.getenv("THUMBNAIL_WIZARD_API_KEY"),
    "video": os.getenv("VIDEO_WIZARD_API_KEY"),
    "hook": os.getenv("HOOK_WIZARD_API_KEY"),
    "document": os.getenv("DOCUMENT_WIZARD_API_KEY"),
}



app = FastAPI(title="Prompts Alchemy Suite")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Import layout
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import layout

# ---------- HOME PAGE -----------
app = FastAPI()



# Add this debug endpoint to see the full layout
@app.get("/debug-layout")
async def debug_layout():
    # Show what layout() produces with minimal content
    test_content = "<h1>Test</h1>"
    full_html = layout("Test", test_content)
    
    # Return first 2000 chars to see navbar
    return HTMLResponse(f"<pre>{full_html[:2000]}</pre>")



@app.get("/home")
async def home_page():
    content = '''
    <div style="max-width: 1200px; margin: 0 auto;">
        <!-- HERO SECTION -->
        <section style="text-align: center; padding: 4rem 0;">
            <div style="font-size: 5rem; color: var(--primary); margin-bottom: 1rem;">
                <i class="fas fa-flask"></i>
            </div>
            <h1 style="font-size: 3.5rem; color: var(--primary); margin-bottom: 1rem;">
                Prompts Alchemy
            </h1>
            <p style="font-size: 1.5rem; color: #374151; max-width: 800px; margin: 0 auto 2rem; font-weight: 500;">
                Transform your content creation with 5 specialized AI wizards
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
                <a href="#wizards" role="button" style="padding: 1rem 2.5rem; font-size: 1.2rem;">
                    <i class="fas fa-eye"></i> Explore Wizards
                </a>
                <a href="#pricing" role="button" class="secondary" style="padding: 1rem 2.5rem; font-size: 1.2rem;">
                    <i class="fas fa-crown"></i> View Pricing
                </a>
            </div>
        </section>

        <!-- PROBLEM SECTION -->
        <section style="background: #f9fafb; border-radius: 1rem; padding: 3rem; margin: 3rem 0;">
            <h2 style="text-align: center; color: var(--primary); margin-bottom: 2rem;">
                The Content Creation Struggle is Real
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: #ef4444; margin-bottom: 1rem;">
                        <i class="fas fa-clock"></i>
                    </div>
                    <h3 style="color: #374151;">Time-Consuming</h3>
                    <p style="color: #4b5563;">Hours spent on thumbnails, scripts, and prompts that don't convert</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: #ef4444; margin-bottom: 1rem;">
                        <i class="fas fa-question-circle"></i>
                    </div>
                    <h3 style="color: #374151;">Uncertain Results</h3>
                    <p style="color: #4b5563;">Not knowing if your content will perform until it's too late</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: #ef4444; margin-bottom: 1rem;">
                        <i class="fas fa-tools"></i>
                    </div>
                    <h3 style="color: #374151;">Tool Overload</h3>
                    <p style="color: #4b5563;">Jumping between 10+ different apps for each content type</p>
                </div>
            </div>
        </section>

        <!-- SOLUTION: 5 WIZARDS + MARKETPLACE -->
        <section id="wizards" style="padding: 3rem 0;">
            <h2 style="text-align: center; color: var(--primary); margin-bottom: 3rem;">
                One Suite, Five Specialized Wizards
            </h2>
            
            <!-- Creator Wizards -->
            <div style="margin-bottom: 4rem;">
                <h3 style="text-align: center; color: var(--primary); margin-bottom: 2rem;">
                    <i class="fas fa-magic"></i> Creator Wizards
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <!-- Prompt Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-hat-wizard"></i>
                        </div>
                        <h4 style="color: #374151;">Prompt Wizard</h4>
                        <p style="color: #4b5563;">Create perfect AI prompts tailored to any platform</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Available Now
                        </div>
                    </div>
                    
                    <!-- Hook Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-fish"></i>
                        </div>
                        <h4 style="color: #374151;">Hook Wizard</h4>
                        <p style="color: #4b5563;">Generate viral hooks that stop scrollers in their tracks</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Available Now
                        </div>
                    </div>
                    
                    <!-- Script Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-cube"></i>
                        </div>
                        <h4 style="color: #374151;">Marketplace</h4>
                        <p style="color: #4b5563;">Buy & sell AI templates, prompts, and workflows</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #f59e0b; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Coming Soon
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Analyzer Wizards -->
            <div>
                <h3 style="text-align: center; color: var(--primary); margin-bottom: 2rem;">
                    <i class="fas fa-search"></i> Analyzer Wizards
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <!-- Thumbnail Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-image"></i>
                        </div>
                        <h4 style="color: #374151;">Thumbnail Wizard</h4>
                        <p style="color: #4b5563;">AI analysis of thumbnails with actionable improvement tips</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Available Now
                        </div>
                    </div>
                    
                    <!-- Document Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-file-contract"></i>
                        </div>
                        <h4 style="color: #374151;">Document Wizard</h4>
                        <p style="color: #4b5563;">Decode legal/medical jargon into plain English</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Available Now
                        </div>
                    </div>
                    
                    <!-- Video Wizard -->
                    <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;">
                            <i class="fas fa-video"></i>
                        </div>
                        <h4 style="color: #374151;">Video Wizard</h4>
                        <p style="color: #4b5563;">Analyze video content for engagement optimization</p>
                        <div style="margin-top: 1rem; padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 2rem; display: inline-block; font-weight: bold;">
                            Available Now
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- HOW IT WORKS -->
        <section style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 1rem; padding: 3rem; margin: 3rem 0;">
            <h2 style="text-align: center; color: var(--primary); margin-bottom: 3rem;">
                How It Works: AI Magic in 3 Steps
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;">
                        <div style="background: var(--primary); color: white; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold;">
                            1
                        </div>
                    </div>
                    <h3 style="color: #374151;">Choose Your Wizard</h3>
                    <p style="color: #4b5563;">Select from 5 specialized tools for your content type</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;">
                        <div style="background: var(--primary); color: white; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold;">
                            2
                        </div>
                    </div>
                    <h3 style="color: #374151;">Input Your Content</h3>
                    <p style="color: #4b5563;">Upload, paste, or describe what you're working on</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;">
                        <div style="background: var(--primary); color: white; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold;">
                            3
                        </div>
                    </div>
                    <h3 style="color: #374151;">Get AI Magic</h3>
                    <p style="color: #4b5563;">Receive optimized content or detailed analysis</p>
                </div>
            </div>
        </section>

        <!-- SIMPLIFIED PRICING -->
        <section id="pricing" style="padding: 3rem 0;">
            <h2 style="text-align: center; color: var(--primary); margin-bottom: 2rem;">
                Simple, Transparent Pricing
            </h2>
            <p style="text-align: center; color: #4b5563; max-width: 800px; margin: 0 auto 3rem; font-size: 1.1rem;">
                One credit system for all 5 wizards. Use credits on any tool, anytime.
            </p>
            
            <!-- Credit Cost Table -->
            <div style="background: #f9fafb; border-radius: 1rem; padding: 2rem; margin-bottom: 3rem;">
                <h3 style="text-align: center; color: var(--primary); margin-bottom: 1.5rem;">
                    <i class="fas fa-coins"></i> Credit Costs
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; max-width: 800px; margin: 0 auto;">
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
                        <div style="font-weight: bold; color: var(--primary);">Thumbnail Wizard</div>
                        <div style="color: #374151; font-size: 1.1rem; margin: 0.5rem 0;">3 credits</div>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
                        <div style="font-weight: bold; color: var(--primary);">Document Wizard</div>
                        <div style="color: #374151; font-size: 1.1rem; margin: 0.5rem 0;">2 credits</div>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
                        <div style="font-weight: bold; color: var(--primary);">Video Wizard</div>
                        <div style="color: #374151; font-size: 1.1rem; margin: 0.5rem 0;">1 credit</div>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
                        <div style="font-weight: bold; color: var(--primary);">Hook Wizard</div>
                        <div style="color: #374151; font-size: 1.1rem; margin: 0.5rem 0;">1 credit</div>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #e5e7eb;">
                        <div style="font-weight: bold; color: var(--primary);">Prompt Wizard</div>
                        <div style="color: #374151; font-size: 1.1rem; margin: 0.5rem 0;">2 credits</div>
                    </div>
                </div>
            </div>
            
            <!-- Three Simple Plans -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <!-- Student Plan -->
                <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; border: 2px solid #e5e7eb;">
                    <h3 style="color: #374151; margin-bottom: 1rem;">Student</h3>
                    <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 0.5rem;">
                        $9.99<span style="font-size: 1rem; color: #6b7280;">/month</span>
                    </div>
                    <div style="color: #374151; margin-bottom: 1.5rem; font-weight: bold; font-size: 1.1rem;">
                        50 credits/month
                    </div>
                    <ul style="list-style: none; padding: 0; margin: 0 0 2rem 0; text-align: left;">
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            All 5 wizards
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Verified students only
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-times" style="color: #ef4444; position: absolute; left: 0;"></i>
                            Watermarked outputs
                        </li>
                    </ul>
                    <a href="#pricing" role="button" style="width: 100%;">Start as Student</a>
                </div>
                
                <!-- Creator Plan (Most Popular) -->
                <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 8px 16px rgba(139, 92, 246, 0.15); text-align: center; border: 2px solid var(--primary); position: relative;">
                    <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--primary); color: white; padding: 0.25rem 1rem; border-radius: 1rem; font-size: 0.9rem;">
                        Most Popular
                    </div>
                    <h3 style="color: var(--primary); margin-bottom: 1rem;">Creator</h3>
                    <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 0.5rem;">
                        $19<span style="font-size: 1rem; color: #6b7280;">/month</span>
                    </div>
                    <div style="color: #374151; margin-bottom: 1.5rem; font-weight: bold; font-size: 1.1rem;">
                        100 credits/month
                    </div>
                    <ul style="list-style: none; padding: 0; margin: 0 0 2rem 0; text-align: left;">
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Clean, watermark-free outputs
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Save & organize projects
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Priority processing
                        </li>
                    </ul>
                    <a href="#pricing" role="button" style="width: 100%; background: var(--primary);">Choose Creator Plan</a>
                </div>
                
                <!-- Power User Plan -->
                <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; border: 2px solid #e5e7eb;">
                    <h3 style="color: #374151; margin-bottom: 1rem;">Power User</h3>
                    <div style="font-size: 2.5rem; color: var(--primary); margin-bottom: 0.5rem;">
                        $49<span style="font-size: 1rem; color: #6b7280;">/month</span>
                    </div>
                    <div style="color: #374151; margin-bottom: 1.5rem; font-weight: bold; font-size: 1.1rem;">
                        300 credits/month
                    </div>
                    <ul style="list-style: none; padding: 0; margin: 0 0 2rem 0; text-align: left;">
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Everything in Creator
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Bulk processing
                        </li>
                        <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                            <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i>
                            Custom workflows
                        </li>
                    </ul>
                    <a href="#pricing" role="button" class="secondary" style="width: 100%;">Choose Power User</a>
                </div>
            </div>
            
            <!-- Free Plan -->
            <div style="background: #f0f9ff; border-radius: 1rem; padding: 2rem; margin-top: 2rem; text-align: center;">
                <h3 style="color: var(--primary); margin-bottom: 1rem;">
                    <i class="fas fa-gift"></i> Free Trial
                </h3>
                <div style="font-size: 2rem; color: var(--primary); margin-bottom: 1rem;">
                    10 credits free
                </div>
                <p style="color: #374151; margin-bottom: 1.5rem;">Try all 5 wizards with no credit card required</p>
                <a href="#pricing" role="button" style="background: var(--primary); color: white; border: none; padding: 0.75rem 1.5rem;">
                    Start Free Trial
                </a>
            </div>
            
            <!-- Business Contact CTA -->
            <div style="background: linear-gradient(135deg, #1f2937, #374151); color: white; border-radius: 1rem; padding: 2rem; margin-top: 2rem; text-align: center;">
                <h3 style="margin-bottom: 1rem;">
                    <i class="fas fa-building"></i> Business & Team Plans
                </h3>
                <p style="margin-bottom: 1.5rem; opacity: 0.9;">
                    Need custom plans for your team? Contact us for volume discounts, white-label solutions, and enterprise features.
                </p>
                <a href="mailto:business@prompts-alchemy.com" role="button" style="background: white; color: #1f2937; border: none; padding: 1rem 2rem; font-weight: bold;">
                    <i class="fas fa-envelope"></i> Contact for Business Plans
                </a>
            </div>
        </section>

        <!-- FAQ -->
        <section style="padding: 3rem 0;">
            <h2 style="text-align: center; color: var(--primary); margin-bottom: 3rem;">
                Frequently Asked Questions
            </h2>
            <div style="max-width: 800px; margin: 0 auto;">
                <details style="background: white; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #e5e7eb;">
                    <summary style="font-weight: bold; color: var(--primary); cursor: pointer; color: #374151;">
                        What counts as an AI credit?
                    </summary>
                    <p style="margin-top: 1rem; color: #4b5563;">
                        One AI credit = one use of any wizard. Whether you're analyzing a thumbnail, generating a prompt, or reviewing a document, each complete operation uses one credit. Credits reset monthly.
                    </p>
                </details>
                
                <details style="background: white; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #e5e7eb;">
                    <summary style="font-weight: bold; color: var(--primary); cursor: pointer; color: #374151;">
                        Can I switch between plans?
                    </summary>
                    <p style="margin-top: 1rem; color: #4b5563;">
                        Yes! You can upgrade, downgrade, or cancel anytime. Unused credits roll over for 30 days. We prorate changes.
                    </p>
                </details>
                
                <details style="background: white; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #e5e7eb;">
                    <summary style="font-weight: bold; color: var(--primary); cursor: pointer; color: #374151;">
                        Do you offer refunds?
                    </summary>
                    <p style="margin-top: 1rem; color: #4b5563;">
                        We offer a 7-day money-back guarantee for all paid plans. If you're not satisfied, we'll refund your payment, no questions asked.
                    </p>
                </details>
            </div>
        </section>

        <!-- FINAL CTA -->
        <section style="background: linear-gradient(135deg, var(--primary), #7c3aed); color: white; border-radius: 1rem; padding: 4rem 2rem; text-align: center; margin: 3rem 0;">
            <h2 style="margin-bottom: 1rem;">Start Creating Better Content Today</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
                Join creators who are saving hours every week with AI-powered tools
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="#pricing" role="button" style="background: white; color: var(--primary); border: none; padding: 1rem 2.5rem;">
                    <i class="fas fa-gift"></i> Start Free Trial
                </a>
                <a href="#wizards" role="button" style="background: transparent; border: 2px solid white; color: white; padding: 1rem 2.5rem;">
                    <i class="fas fa-eye"></i> Explore Wizards
                </a>
            </div>
        </section>
    </div>
    '''
    return HTMLResponse(layout("Prompts Alchemy - AI Wizard Suite", content))

@app.get("/")
async def root():
    return await home_page()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ---------- DOCUMENT WIZARD -----------

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
            <i class="fas fa-file-contract"></i><br>
            Document Decoder
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 600px; margin: 1rem auto;">
            AI-powered translation of complex documents. Understand legal, medical, and technical language in plain English.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-magic"></i> Decode a Document
            </a>
        </div>
        
        <div class="card-grid">
            <div class="step-card">
                <i class="fas fa-gavel"></i>
                <h3>Legal Documents</h3>
                <p>Contracts, leases, terms of service</p>
            </div>
            
            <div class="step-card">
                <i class="fas fa-heart-pulse"></i>
                <h3>Medical Papers</h3>
                <p>Reports, prescriptions, instructions</p>
            </div>
            
            <div class="step-card">
                <i class="fas fa-file-signature"></i>
                <h3>Contracts</h3>
                <p>Employment, service, rental agreements</p>
            </div>
            
            <div class="step-card">
                <i class="fas fa-warning"></i>
                <h3>Warning Labels</h3>
                <p>Safety instructions, disclaimers</p>
            </div>
            
            <div class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Academic Papers</h3>
                <p>Research, studies, technical docs</p>
            </div>
            
            <div class="step-card">
                <i class="fas fa-building"></i>
                <h3>Government Forms</h3>
                <p>Applications, permits, official docs</p>
            </div>
        </div>
        
        <div class="warning-box" style="max-width: 600px; margin: 3rem auto;">
            <h3 style="color: #d97706; margin-top: 0;">
                <i class="fas fa-exclamation-triangle"></i> Important Notice
            </h3>
            <p style="margin-bottom: 0;">
                This tool provides AI-assisted interpretation for educational purposes only. 
                For legal, medical, or financial decisions, always consult a qualified professional.
            </p>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Home", content))

# ========== STEP 1: DOCUMENT TYPE ==========
@app.get("/wizard")
async def step1():
    content = '''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step active">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 1: Document Type</h1>
        <p style="text-align: center; color: #6b7280;">
            What type of document are you trying to understand?
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step2?doc_type=legal" class="step-card">
                <i class="fas fa-gavel"></i>
                <h3>Legal Document</h3>
                <p>Contract, lease, terms of service, agreement</p>
            </a>
            
            <a href="/wizard/step2?doc_type=medical" class="step-card">
                <i class="fas fa-heart-pulse"></i>
                <h3>Medical Document</h3>
                <p>Report, prescription, diagnosis, instructions</p>
            </a>
            
            <a href="/wizard/step2?doc_type=contract" class="step-card">
                <i class="fas fa-file-signature"></i>
                <h3>Contract/Agreement</h3>
                <p>Employment, service, rental, purchase agreement</p>
            </a>
            
            <a href="/wizard/step2?doc_type=financial" class="step-card">
                <i class="fas fa-money-bill-wave"></i>
                <h3>Financial Document</h3>
                <p>Loan terms, investment, insurance, tax forms</p>
            </a>
            
            <a href="/wizard/step2?doc_type=technical" class="step-card">
                <i class="fas fa-cogs"></i>
                <h3>Technical Manual</h3>
                <p>Instructions, specifications, warranty</p>
            </a>
            
            <a href="/wizard/step2?doc_type=government" class="step-card">
                <i class="fas fa-landmark"></i>
                <h3>Government Form</h3>
                <p>Application, permit, official document</p>
            </a>
            
            <a href="/wizard/step2?doc_type=academic" class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Academic Paper</h3>
                <p>Research, study, scientific paper</p>
            </a>
            
            <a href="/wizard/step2?doc_type=other" class="step-card">
                <i class="fas fa-file-alt"></i>
                <h3>Other Complex Document</h3>
                <p>Any difficult-to-understand text</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" role="button" class="secondary">Cancel</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 1: Document Type", content))

# ========== STEP 2: AUDIENCE LEVEL ==========
@app.get("/wizard/step2")
async def step2(doc_type: str = Query("legal")):
    doc_type_names = {
        "legal": "Legal Document",
        "medical": "Medical Document", 
        "contract": "Contract/Agreement",
        "financial": "Financial Document",
        "technical": "Technical Manual",
        "government": "Government Form",
        "academic": "Academic Paper",
        "other": "Complex Document"
    }
    
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step active">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 2: Your Knowledge Level</h1>
        <p style="text-align: center; color: #6b7280;">
            How familiar are you with {doc_type_names[doc_type].lower()}s?
        </p>
        
        <p style="text-align: center;"><strong>Document Type:</strong> {doc_type_names[doc_type]}</p>
        
        <div class="card-grid">
            <a href="/wizard/step3?doc_type={doc_type}&level=novice" class="step-card">
                <i class="fas fa-seedling"></i>
                <h3>Novice</h3>
                <p>Little to no experience. Explain like I'm new.</p>
            </a>
            
            <a href="/wizard/step3?doc_type={doc_type}&level=general" class="step-card">
                <i class="fas fa-user"></i>
                <h3>General Public</h3>
                <p>Basic understanding. Use everyday language.</p>
            </a>
            
            <a href="/wizard/step3?doc_type={doc_type}&level=educated" class="step-card">
                <i class="fas fa-user-graduate"></i>
                <h3>Educated Layperson</h3>
                <p>Some background. Can handle some terminology.</p>
            </a>
            
            <a href="/wizard/step3?doc_type={doc_type}&level=professional" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Related Professional</h3>
                <p>Work in related field. Want deeper analysis.</p>
            </a>
        </div>
        
        <div class="info-box">
            <p style="margin: 0;">
                <strong>Tip:</strong> Choose "Novice" for maximum plain English translation. 
                The AI will avoid all jargon and use simple analogies.
            </p>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="wizard" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 2: Knowledge Level", content))

# ========== STEP 3: DOCUMENT INPUT ==========
@app.get("/wizard/step3")
async def step3(
    doc_type: str = Query("legal"),
    level: str = Query("novice")
):
    doc_type_names = {
        "legal": "Legal Document",
        "medical": "Medical Document",
        "contract": "Contract/Agreement", 
        "financial": "Financial Document",
        "technical": "Technical Manual",
        "government": "Government Form",
        "academic": "Academic Paper",
        "other": "Complex Document"
    }
    
    level_names = {
        "novice": "Novice",
        "general": "General Public", 
        "educated": "Educated Layperson",
        "professional": "Related Professional"
    }
    
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step active">3</div>
            <div class="step">4</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 3: Paste Your Document</h1>
        <p style="text-align: center; color: #6b7280;">
            Copy and paste the text you want to understand
        </p>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Selections:</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1rem 0;">
                <div><strong>Document Type:</strong><br>{doc_type_names[doc_type]}</div>
                <div><strong>Your Level:</strong><br>{level_names[level]}</div>
            </div>
        </div>
        
        <div class="warning-box">
            <h4 style="color: #d97706; margin-top: 0;">
                <i class="fas fa-shield-alt"></i> Privacy & Security
            </h4>
            <p style="margin-bottom: 0;">
                • Your document is processed securely via API<br>
                • No data is stored permanently<br>
                • Remove sensitive personal information before pasting<br>
                • For highly confidential documents, use generic examples
            </p>
        </div>
        
        <form action="/process" method="POST">
            <input type="hidden" name="doc_type" value="{doc_type}">
            <input type="hidden" name="level" value="{level}">
            
            <div style="margin: 2rem 0;">
                <label for="document_text">
                    <strong>Document Text:</strong>
                    <p style="color: #6b7280; margin: 0.5rem 0;">
                        Paste the full document or the specific section you want decoded.
                    </p>
                </label>
                <textarea id="document_text" name="document_text" rows="12" 
                          placeholder="Paste your legal clause, medical report, contract section, or any complex text here..."
                          class="doc-input"></textarea>
            </div>
            
            <div style="margin: 2rem 0;">
                <label for="specific_questions">
                    <strong>Specific Questions (Optional):</strong>
                    <p style="color: #6b7280; margin: 0.5rem 0;">
                        What specifically do you want to understand about this document?
                    </p>
                </label>
                <textarea id="specific_questions" name="specific_questions" rows="4" 
                          placeholder="Example questions: 
• What are the hidden risks in this clause?
• What does this medical term mean for my treatment?
• What am I really agreeing to here?
• What are my rights vs. responsibilities?"
                          style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem;"></textarea>
            </div>
            
            <div style="text-align: center; margin: 2rem 0;">
                <button type="submit" style="padding: 1rem 3rem; font-size: 1.2rem;">
                    <i class="fas fa-search"></i> Decode This Document
                </button>
                <p style="margin-top: 1rem; color: #6b7280;">
                    <i class="fas fa-clock"></i> AI analysis takes 15-30 seconds
                </p>
            </div>
        </form>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step2?doc_type={doc_type}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 3: Document Input", content))

# ========== PROCESS ==========
@app.post("/process")
async def process_document(
    doc_type: str = Form(...),
    level: str = Form(...),
    document_text: str = Form(...),
    specific_questions: str = Form("")
):
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-search"></i>
        </div>
        
        <h1 style="color: var(--primary);">Decoding Your Document...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Analyzing {doc_type.replace("_", " ").title()} text for a {level} understanding...
        </p>
        
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            <i class="fas fa-lightbulb"></i> Looking for tricky language, hidden meanings, and plain English translations...
        </p>
        
        <meta http-equiv="refresh" content="3;url=/result?doc_type={doc_type}&level={level}&document_text={document_text}&specific_questions={specific_questions}">
    </div>
    '''
    
    return HTMLResponse(layout("Decoding...", loading_content))

# ========== RESULT ==========
@app.get("/result")
async def show_result(
    doc_type: str = Query(...),
    level: str = Query(...),
    document_text: str = Query(...),
    specific_questions: str = Query("")
):
    # YOUR TURQUOISE COLOR
    TURQUOISE = "#0d96c1"
    TURQUOISE_LIGHT = "#ecfeff"
    TURQUOISE_DARK = "#0c4a6e"
    
    # CHECK DOCUMENT SIZE FIRST
    word_count = len(document_text.split())
    
    if word_count > 2000:
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #d97706;"><i class="fas fa-exclamation-triangle"></i> Document Too Large</h1>
    <div style="background: #fef3c7; border: 2px solid #f59e0b; border-radius: 0.5rem; padding: 1.5rem; margin: 1rem 0;">
        <p><strong>{word_count} words detected (limit: 2,000 words)</strong></p>
        <p>For best results:</p>
        <ol style="text-align: left; max-width: 500px; margin: 1rem auto;">
            <li><strong>Extract the most important section</strong> (1-2 paragraphs)</li>
            <li>Focus on the <strong>specific clause</strong> you don't understand</li>
            <li>Copy just the <strong>key paragraphs</strong></li>
        </ol>
    </div>
    <div style="margin: 2rem 0;">
        <a href="/wizard/step3?doc_type={doc_type}&level={level}" 
           role="button" style="background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-edit"></i> Try Again with Smaller Section
        </a>
    </div>
</div>
'''
        return HTMLResponse(layout("Document Too Large", result_content))
    
    # TEST MODE
    TEST_MODE = False
    
    try:
        if TEST_MODE:
            ai_text = '''OVERALL COMPLEXITY SCORE: 8/10 - This legal clause uses dense legal terminology but follows standard contract structure

PLAIN ENGLISH TRANSLATION:
This section says: "If someone sues the other party for any reason, the first party will pay for all legal costs and damages." 
• You're agreeing to cover ALL legal expenses if the other party gets sued
• This applies even if the lawsuit isn't really their fault
• There's no limit to how much you might have to pay

TRICKY LANGUAGE ALERT:
• "Indemnifies and holds harmless": Means you'll pay ALL legal costs for the other party | This is very broad protection for them | Example: If they get sued for $1M, you pay it
• "Any and all claims, demands, damages": Means EVERY possible type of legal complaint | Very broad language that covers things you can't predict | Example: Future lawsuits you can't imagine today
• "Causes of action or suits at law or in equity": Means ANY type of lawsuit in ANY court system | Covers more than just normal lawsuits | Example: Arbitration, mediation, court cases

RED FLAGS TO WATCH FOR:
• Unlimited liability: You could owe millions with no cap | Very risky for individuals/small businesses | Ask for: A dollar limit or "to the extent permitted by law"
• One-sided protection: Only protects the other party, not you | Creates unequal relationship | Ask for: Mutual indemnification (both sides protect each other)
• Broad language: "Any and all" means literally everything | Could cover lawsuits unrelated to your actual work | Ask for: Specific list of what's covered

STANDARD/BOILERPLATE SECTIONS:
• Legal jurisdiction: Which state's laws apply | Most contracts have this | No need to worry unless it's an unusual state
• Notice provisions: How to send official letters | Standard administrative detail | Just note the addresses/email
• Severability: If one part is illegal, rest stays valid | Standard protection for both sides | Nothing to negotiate

YOUR RIGHTS (What you can do):
• Right to receive notice: They must notify you before suing | How to exercise: Make sure your contact info is correct
• Right to defend: You can choose the lawyers (usually) | How to exercise: Ask for "right to select counsel" in clause

YOUR RESPONSIBILITIES (What you must do):
• Pay all legal costs: You cover everything if they get sued | Consequences if not done: They can sue you for reimbursement
• Cooperate with defense: You must help with the legal case | Consequences if not done: Could lose insurance coverage

NEXT STEPS & QUESTIONS TO ASK:
1. Question to ask a lawyer: "Is there a way to cap my liability at a specific dollar amount or my insurance limits?"
2. Action to take: Ask for "mutual indemnification" - both sides protect each other equally
3. What to research: Your insurance policy - does it cover "contractual liability"?

BOTTOM LINE SUMMARY:
This is a very one-sided liability clause that could leave you responsible for unlimited legal costs if the other party gets sued for any reason. For a novice, this is risky without a liability cap. Ask for either a dollar limit or make it mutual so both sides have the same protection.'''
        else:
            ai_text = "Real API mode - set TEST_MODE = False"
        
        # Parse sections
        sections = {}
        current_section = None
        current_content = []
        
        for line in ai_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.endswith(':'):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.rstrip(':')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Build cards - SIMPLE VERSION THAT WON'T BREAK
        analysis_html = ""
        
        section_config = [
            ("PLAIN ENGLISH TRANSLATION", "fa-language", "The document in simple terms"),
            ("TRICKY LANGUAGE ALERT", "fa-exclamation-triangle", "Watch out for these terms"),
            ("RED FLAGS TO WATCH FOR", "fa-flag", "Potential concerns to address"),
            ("STANDARD/BOILERPLATE SECTIONS", "fa-check-circle", "Normal sections, nothing to worry"),
            ("YOUR RIGHTS", "fa-shield-alt", "What you're entitled to"),
            ("YOUR RESPONSIBILITIES", "fa-tasks", "What you need to do"),
            ("NEXT STEPS & QUESTIONS TO ASK", "fa-question-circle", "Actionable advice"),
            ("BOTTOM LINE SUMMARY", "fa-bullseye", "The most important takeaway")
        ]
        
        for section_title, icon, description in section_config:
            if section_title in sections:
                content = sections[section_title]
                
                analysis_html += f'''
<div style="background: white; border: 2px solid {TURQUOISE}; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; display: block;">
    <h3 style="color: {TURQUOISE}; margin-top: 0; border-bottom: 2px solid {TURQUOISE_LIGHT}; padding-bottom: 0.5rem;">
        <i class="fas {icon}" style="margin-right: 0.5rem;"></i>{section_title}
    </h3>
    <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 1rem;">
        <i class="fas fa-info-circle"></i> {description}
    </p>
    <div style="background: {TURQUOISE_LIGHT}; padding: 1rem; border-radius: 8px; border-left: 4px solid {TURQUOISE}; color: {TURQUOISE_DARK}; line-height: 1.6;">
        {content.replace(chr(10), '<br>').replace('•', '•')}
    </div>
</div>
'''
        
        # Score card
        if "OVERALL COMPLEXITY SCORE" in ai_text:
            score = "5"
            try:
                import re
                score_match = re.search(r'(\d+(?:\.\d+)?)/10', ai_text)
                if score_match:
                    score = score_match.group(1)
            except:
                pass
            
            try:
                score_num = float(score)
                if score_num >= 8:
                    score_color = "#dc2626"
                    score_icon = "fa-brain"
                    score_text = "Very Complex"
                elif score_num >= 6:
                    score_color = "#d97706"
                    score_icon = "fa-exclamation-triangle"
                    score_text = "Complex"
                elif score_num >= 4:
                    score_color = TURQUOISE
                    score_icon = "fa-balance-scale"
                    score_text = "Moderate"
                else:
                    score_color = "#059669"
                    score_icon = "fa-check-circle"
                    score_text = "Fairly Simple"
            except:
                score_color = TURQUOISE
                score_icon = "fa-file-alt"
                score_text = "Document Analysis"
            
            score_html = f'''
<div style="background: white; border: 3px solid {score_color}; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; text-align: center; display: block;">
    <div style="font-size: 0.9rem; color: {score_color}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
        <i class="fas {score_icon}"></i> Document Complexity Score
    </div>
    <div style="font-size: 4rem; font-weight: bold; color: {score_color}; margin: 0.5rem 0; line-height: 1;">
        {score}<span style="font-size: 2rem; opacity: 0.7;">/10</span>
    </div>
    <div style="font-size: 1.1rem; color: #374151; margin-top: 0.5rem;">
        {score_text} • {doc_type.replace("_", " ").title()} • {level.replace("_", " ").title()} Level
    </div>
</div>
'''
            analysis_html = score_html + analysis_html
        
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; color: {TURQUOISE};">
            <i class="fas fa-file-contract"></i>
        </div>
        <h1 style="color: {TURQUOISE};">Document Decoded!</h1>
        <p style="color: #64748b;">Translated for <strong>{level.replace("_", " ").title()}</strong> understanding</p>
    </div>
    
    <div style="background: #fef3c7; border: 2px solid #f59e0b; border-radius: 0.5rem; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: #d97706; margin-top: 0;">
            <i class="fas fa-gavel"></i> Legal Disclaimer
        </h4>
        <p style="margin-bottom: 0;">
            This AI analysis is for educational purposes only. It helps you understand documents better, 
            but is NOT legal, medical, or financial advice. For important decisions, consult a qualified professional.
        </p>
    </div>
    
    {analysis_html}
    
    <div style="text-align: center; margin-top: 3rem;">
        <a href="wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-file-contract"></i> Decode Another Document
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
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> Analysis Error</h1>
    <p>{str(e)}</p>
    <a href="/wizard/step3?doc_type={doc_type}&level={level}" 
       role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Try Again</a>
</div>
'''
    
    return HTMLResponse(layout("Document Analysis Results", result_content))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
  

# ---------- HOOK WIZARD -----------

# This tells Python to look in root folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now this imports from ROOT layout.py
from layout import layout

app = FastAPI()
DEEPSEEK_KEY = os.getenv("HOOK_WIZARD_API_KEY")
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
            <i class="fas fa-fish-hook"></i><br>
            Hook Alchemy
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            AI-powered hook generator. Stop viewers from scrolling in 3 seconds.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-magic"></i> Start Hook Wizard
            </a>
        </div>
        
        <div class="card-grid">
            <div class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok Hooks</h3>
                <p>Stop the scroll in 1 second</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube Hooks</h3>
                <p>Beat the 30-second skip</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram Hooks</h3>
                <p>Grab attention on Reels</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn Hooks</h3>
                <p>Professional engagement</p>
            </div>
        </div>
        
        <div class="hook-example" style="max-width: 600px; margin: 3rem auto;">
            <h3>Example Hook Generated:</h3>
            <p>"What if I told you your first 3 seconds determine 80% of your video's success? Here's why..."</p>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Home", content))

# ========== STEP 1: PLATFORM ==========
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 1: Choose Platform</h1>
        <p style="text-align: center; color: #6b7280;">
            Where will your content be seen?
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step2?platform=tiktok" class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok</h3>
                <p>Fast, bold, under 3 seconds</p>
            </a>
            
            <a href="/wizard/step2?platform=youtube" class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube</h3>
                <p>5-15 second hooks</p>
            </a>
            
            <a href="/wizard/step2?platform=instagram" class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram</h3>
                <p>Reels & Stories</p>
            </a>
            
            <a href="/wizard/step2?platform=linkedin" class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn</h3>
                <p>Professional, value-first</p>
            </a>
            
            <a href="/wizard/step2?platform=twitter" class="step-card">
                <i class="fab fa-twitter"></i>
                <h3>Twitter/X</h3>
                <p>Thread starters</p>
            </a>
            
            <a href="/wizard/step2?platform=facebook" class="step-card">
                <i class="fab fa-facebook"></i>
                <h3>Facebook</h3>
                <p>Groups & viral posts</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" role="button" class="secondary">Cancel</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 1: Platform", content))

# ========== STEP 2: HOOK TYPE ==========
@app.get("/wizard/step2")
async def step2(platform: str = Query("tiktok")):
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 2: Hook Type</h1>
        <p style="text-align: center; color: #6b7280;">
            What style of hook works best?
        </p>
        
        <p style="text-align: center;"><strong>Platform:</strong> {platform.title()}</p>
        
        <div class="card-grid">
            <a href="/wizard/step3?platform={platform}&type=question" class="step-card">
                <i class="fas fa-question-circle"></i>
                <h3>Question</h3>
                <p>Makes viewer think immediately</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=shocking" class="step-card">
                <i class="fas fa-bolt"></i>
                <h3>Shocking Stat</h3>
                <p>Surprising fact or number</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=story" class="step-card">
                <i class="fas fa-book"></i>
                <h3>Story</h3>
                <p>Personal anecdote or case study</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=controversy" class="step-card">
                <i class="fas fa-fire"></i>
                <h3>Controversy</h3>
                <p>Take a bold stance</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=howto" class="step-card">
                <i class="fas fa-wrench"></i>
                <h3>"How to"</h3>
                <p>Immediate value promise</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=fear" class="step-card">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Fear/Opportunity</h3>
                <p>What they're missing/avoiding</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="wizard" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 2: Hook Type", content))

# ========== STEP 3: CONTENT TYPE ==========
@app.get("/wizard/step3")
async def step3(platform: str = Query("tiktok"), type: str = Query("question")):
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 3: Content Type</h1>
        <p style="text-align: center; color: #6b7280;">
            What kind of content follows the hook?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Hook Type:</strong> {type.replace("_", " ").title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step4?platform={platform}&type={type}&content=educational" class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Educational</h3>
                <p>Teach, explain, inform</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&content=entertainment" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Entertainment</h3>
                <p>Funny, engaging, fun</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&content=inspirational" class="step-card">
                <i class="fas fa-heart"></i>
                <h3>Inspirational</h3>
                <p>Motivate, uplift, inspire</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&content=review" class="step-card">
                <i class="fas fa-star"></i>
                <h3>Review</h3>
                <p>Product/service analysis</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&content=vlog" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Vlog/Personal</h3>
                <p>Day-in-life, personal stories</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&content=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Marketing, tips, industry</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step2?platform={platform}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 3: Content Type", content))

# ========== STEP 4: AUDIENCE ==========
@app.get("/wizard/step4")
async def step4(platform: str = Query("tiktok"), type: str = Query("question"), content: str = Query("educational")):
    content_html = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step active">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 4: Target Audience</h1>
        <p style="text-align: center; color: #6b7280;">
            Who are you trying to reach?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Hook:</strong> {type.replace("_", " ").title()} • 
            <strong>Content:</strong> {content.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=genz" class="step-card">
                <i class="fas fa-mobile-alt"></i>
                <h3>Gen Z</h3>
                <p>18-24, digital natives</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=millennials" class="step-card">
                <i class="fas fa-home"></i>
                <h3>Millennials</h3>
                <p>25-40, career-focused</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=professionals" class="step-card">
                <i class="fas fa-suitcase"></i>
                <h3>Professionals</h3>
                <p>Business, B2B, career</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=creators" class="step-card">
                <i class="fas fa-paint-brush"></i>
                <h3>Creators</h3>
                <p>Content creators, artists</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=parents" class="step-card">
                <i class="fas fa-baby"></i>
                <h3>Parents</h3>
                <p>Family, parenting, home</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience=general" class="step-card">
                <i class="fas fa-users"></i>
                <h3>General</h3>
                <p>Broad appeal</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step3?platform={platform}&type={type}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 4: Audience", content_html))

# ========== STEP 5: TONE ==========
@app.get("/wizard/step5")
async def step5(platform: str = Query("tiktok"), type: str = Query("question"), content: str = Query("educational"), audience: str = Query("genz")):
    content_html = f'''
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
            What's the voice/personality?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Hook:</strong> {type.replace("_", " ").title()} • 
            <strong>Content:</strong> {content.title()} • 
            <strong>Audience:</strong> {audience.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=urgent" class="step-card">
                <i class="fas fa-clock"></i>
                <h3>Urgent</h3>
                <p>Time-sensitive, must-watch</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=funny" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Funny</h3>
                <p>Humor, wit, entertainment</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=serious" class="step-card">
                <i class="fas fa-balance-scale"></i>
                <h3>Serious</h3>
                <p>Professional, authoritative</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=curious" class="step-card">
                <i class="fas fa-search"></i>
                <h3>Curious</h3>
                <p>Questioning, exploratory</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=excited" class="step-card">
                <i class="fas fa-star"></i>
                <h3>Excited</h3>
                <p>Energetic, enthusiastic</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&content={content}&audience={audience}&tone=relatable" class="step-card">
                <i class="fas fa-handshake"></i>
                <h3>Relatable</h3>
                <p>"I've been there too"</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step4?platform={platform}&type={type}&content={content}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 5: Tone", content_html))

# ========== STEP 6: TOPIC INPUT ==========
@app.get("/wizard/step6")
async def step6(
    platform: str = Query("tiktok"),
    type: str = Query("question"),
    content: str = Query("educational"),
    audience: str = Query("genz"),
    tone: str = Query("urgent")
):
    content_html = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step active">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 6: Enter Your Topic</h1>
        <p style="text-align: center; color: #6b7280;">
            What's your content about?
        </p>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Selections:</h3>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 1rem 0;">
                <div><strong>Platform:</strong><br>{platform.title()}</div>
                <div><strong>Hook Type:</strong><br>{type.replace("_", " ").title()}</div>
                <div><strong>Content:</strong><br>{content.title()}</div>
                <div><strong>Audience:</strong><br>{audience.title()}</div>
                <div><strong>Tone:</strong><br>{tone.title()}</div>
            </div>
        </div>
        
        <div style="background: #eff6ff; border: 2px solid var(--primary); border-radius: 0.75rem; padding: 1rem; margin: 1rem 0;">
            <p style="margin: 0; color: #1e40af; display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-lightbulb" style="color: var(--primary);"></i>
                <strong>Pro Tip:</strong> Be specific! "How to lose weight" vs "3 science-backed habits for sustainable weight loss"
            </p>
        </div>
        
        <form action="/process" method="POST">
            <input type="hidden" name="platform" value="{platform}">
            <input type="hidden" name="type" value="{type}">
            <input type="hidden" name="content" value="{content}">
            <input type="hidden" name="audience" value="{audience}">
            <input type="hidden" name="tone" value="{tone}">
            
            <div style="margin: 2rem 0;">
                <label for="topic">
                    <strong>Your Topic/Subject:</strong>
                    <p style="color: #6b7280; margin: 0.5rem 0;">What is your video/post/content about?</p>
                </label>
                <textarea id="topic" name="topic" rows="4" 
                          placeholder="Example: 'Sustainable weight loss without dieting' or 'Review of the new iPhone camera features' or 'Day in the life of a remote software developer'"
                          style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem;" required></textarea>
            </div>
            
            <div style="text-align: center; margin: 2rem 0;">
                <button type="submit" style="padding: 1rem 3rem; font-size: 1.2rem;">
                    <i class="fas fa-magic"></i> Generate Viral Hooks
                </button>
                <p style="margin-top: 1rem; color: #6b7280;">
                    <i class="fas fa-clock"></i> Creating 3 hook options for you...
                </p>
            </div>
        </form>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step5?platform={platform}&type={type}&content={content}&audience={audience}" 
               role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 6: Enter Topic", content_html))

# ========== PROCESS ==========
@app.post("/document-wizard/process")
async def process_hook(
    platform: str = Form(...),
    type: str = Form(...),
    content: str = Form(...),
    audience: str = Form(...),
    tone: str = Form(...),
    topic: str = Form(...)
):
    DEEPSEEK_KEY = os.getenv("DOCUMENT_WIZARD_API_KEY")
    
    # Show loading page
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-fish-hook"></i>
        </div>
        
        <h1 style="color: var(--primary);">Crafting Your Hooks...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Creating {type} hooks for {platform} targeting {audience}...
        </p>
        
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            Generating 3 viral hook options...
        </p>
        
        <!-- Auto-refresh to result after 3 seconds -->
        <meta http-equiv="refresh" content="3;url=/result?platform={platform}&type={type}&content={content}&audience={audience}&tone={tone}&topic={topic}">
    </div>
    '''
    
    return HTMLResponse(layout("Creating Hooks...", loading_content))

def parse_hooks_from_response(ai_response: str) -> list:
    """Parse AI response into structured hook data"""
    hooks = []
    
    # Clean the response
    ai_response = ai_response.strip()
    
    # Split by hook sections (looks for "### **Hook Option X**" or similar)
    import re
    
    # Try multiple patterns
    patterns = [
        r'### \*\*Hook Option \d+\*\*',  # ### **Hook Option 1**
        r'\d+\.\s*\*\*Hook Text\*\*',    # 1. **Hook Text**
        r'Hook Option \d+:',             # Hook Option 1:
    ]
    
    for pattern in patterns:
        sections = re.split(pattern, ai_response, flags=re.IGNORECASE)
        if len(sections) > 1:  # Found matches
            # Skip first part (might be intro text)
            for section in sections[1:4]:  # Take first 3 hooks
                hook = parse_single_hook(section)
                if hook:
                    hooks.append(hook)
            break
    
    # If still no hooks, try a simpler approach
    if not hooks:
        hooks = parse_fallback_hooks(ai_response)
    
    return hooks

def parse_single_hook(section: str) -> dict:
    """Parse a single hook section"""
    import re
    hook = {}
    
    # Clean up the section
    section = section.strip()
    
    # Extract hook text - more specific pattern
    # Look for "Hook Text:" followed by content (might be on next line)
    text_patterns = [
        r'\*\*Hook Text\*\*[:\s]*\n?\s*(.+?)(?=\n\s*\*\*Why It Works\*\*|\n\s*\*\*Visual|\Z)',
        r'Hook Text[:\s]*\n?\s*(.+?)(?=\n\s*Why It Works|\n\s*Visual|\Z)',
        r'1\.\s*\*\*Hook Text\*\*[:\s]*\n?\s*(.+?)(?=\n\s*2\.|\n\s*\*\*Why|$)'
    ]
    
    for pattern in text_patterns:
        text_match = re.search(pattern, section, re.DOTALL | re.IGNORECASE)
        if text_match:
            # Clean up the text - remove extra quotes, trim
            text = text_match.group(1).strip()
            # Remove surrounding quotes if present
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            elif text.startswith("'") and text.endswith("'"):
                text = text[1:-1]
            hook['text'] = text.strip()
            break
    
    # If we still don't have text, take first non-empty line
    if 'text' not in hook:
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        if lines:
            # Skip lines that look like headers
            for line in lines:
                if not re.match(r'^\*\*.*\*\*$', line) and not re.match(r'^\d+\.', line):
                    hook['text'] = line.strip('"\'')
                    break
    
    # Extract psychology
    psych_patterns = [
        r'\*\*Why It Works\*\*[:\s]*\n?\s*(.+?)(?=\n\s*\*\*Visual/Execution Tip\*\*|\n\s*\*\*Visual Tip\*\*|\n\s*---|\Z)',
        r'Why It Works[:\s]*\n?\s*(.+?)(?=\n\s*Visual/Execution Tip|\n\s*Visual Tip|\n\s*---|\Z)',
        r'2\.\s*\*\*Why It Works\*\*[:\s]*\n?\s*(.+?)(?=\n\s*3\.|\n\s*\*\*Visual|$)'
    ]
    
    for pattern in psych_patterns:
        psych_match = re.search(pattern, section, re.DOTALL | re.IGNORECASE)
        if psych_match:
            hook['psychology'] = psych_match.group(1).strip()
            break
    
    # Extract visual tip
    visual_patterns = [
        r'\*\*Visual/Execution Tip\*\*[:\s]*\n?\s*(.+?)(?=\n\s*---|\n\s*###|\Z)',
        r'\*\*Visual Tip\*\*[:\s]*\n?\s*(.+?)(?=\n\s*---|\n\s*###|\Z)',
        r'Visual/Execution Tip[:\s]*\n?\s*(.+?)(?=\n\s*---|\n\s*###|\Z)',
        r'3\.\s*\*\*Visual/Execution Tip\*\*[:\s]*\n?\s*(.+?)(?=\n\s*---|\n\s*###|\Z)'
    ]
    
    for pattern in visual_patterns:
        visual_match = re.search(pattern, section, re.DOTALL | re.IGNORECASE)
        if visual_match:
            hook['visual'] = visual_match.group(1).strip()
            break
    
    return hook if hook else None

def parse_fallback_hooks(ai_response: str) -> list:
    """Fallback parsing if regex fails"""
    hooks = []
    lines = ai_response.split('\n')
    
    current_hook = {}
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if 'hook text' in line.lower() or line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            if current_hook and 'text' in current_hook:
                hooks.append(current_hook)
            current_hook = {'text': line.replace('**Hook Text**:', '').replace('**Hook Text**:', '').strip().strip('"')}
        elif 'why it works' in line.lower():
            current_hook['psychology'] = line.replace('**Why It Works**:', '').replace('**Why It Works**:', '').strip()
        elif 'visual' in line.lower():
            current_hook['visual'] = line.replace('**Visual/Execution Tip**:', '').replace('**Visual Tip**:', '').strip()
    
    # Don't forget the last hook
    if current_hook and 'text' in current_hook:
        hooks.append(current_hook)
    
    # Ensure we have 3 hooks
    while len(hooks) < 3:
        hooks.append({
            'text': f'Hook {len(hooks)+1}: Engaging hook about your topic',
            'psychology': 'Creates curiosity and engagement',
            'visual': 'Use text overlay and engaging visuals'
        })
    
    return hooks[:3]  # Return max 3 hooks

def get_hook_type_guidelines(hook_type: str) -> str:
    guidelines = {
        "question": "• Must make viewer answer internally\n• Should be personally relevant\n• Creates immediate engagement\n• Leads naturally to content",
        "shocking": "• Stat/fact must be genuinely surprising\n• Should challenge assumptions\n• Source credibility helps\n• Visual representation powerful",
        "story": "• Personal/relatable anecdote\n• Should have emotional hook\n• Quick setup (2-3 sentences)\n• Clear connection to topic",
        "controversy": "• Bold stance or unpopular opinion\n• Should be defendable\n• Creates discussion/engagement\n• Know your audience limits",
        "howto": "• Clear benefit promised\n• Should seem achievable\n• Specific, not vague\n• Results-oriented language",
        "fear": "• Pain point identification\n• Solution promised\n• Should be legitimate concern\n• Empowering, not paralyzing"
    }
    return guidelines.get(hook_type, "• Grab attention\n• Create curiosity\n• Promise value\n• Lead to content")

def get_topic_guidance(topic: str) -> str:
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ["ai", "artificial", "generated", "machine learning"]):
        return "• Focus on technology, futurism, ethics\n• Highlight uncanny valley, implications\n• Use tech-savvy but accessible language"
    elif any(word in topic_lower for word in ["review", "product", "service", "app"]):
        return "• Focus on value, features, pros/cons\n• Highlight pain points and solutions\n• Use authentic, experience-based language"
    elif any(word in topic_lower for word in ["tutorial", "how to", "guide", "learn"]):
        return "• Focus on transformation, results\n• Highlight before/after, ease of learning\n• Use empowering, step-by-step language"
    elif any(word in topic_lower for word in ["vlog", "personal", "story", "day in life"]):
        return "• Focus on authenticity, connection\n• Highlight relatable moments, emotions\n• Use conversational, intimate language"
    else:
       return "• Tailor hooks specifically to this topic\n• Use topic-relevant language and examples\n• Make hooks feel custom, not generic"


# ========== RESULT ==========  <-- This comes AFTER the helper functions
@app.get("/result")
async def show_result(
    platform: str = Query(...),
    type: str = Query(...),
    content: str = Query(...),
    audience: str = Query(...),
    tone: str = Query(...),
    topic: str = Query(...)
):
    # TEST MODE - Set to False for real API
    TEST_MODE = True
    
    try:
        if TEST_MODE:
            # Clean mock data with PROPER formatting
            ai_text = f'''HOOK 1 TEXT: "I found a website where two AIs battle to create fake people. The results are terrifyingly real."
WHY IT WORKS: Combines AI intrigue with uncanny valley fascination. The "battle" metaphor makes it dramatic.
VISUAL TIP: Split screen showing AI "painter" vs AI "detective" with facial close-ups.

HOOK 2 TEXT: "What if every face you see online was fake? This website proves it's possible."
WHY IT WORKS: Philosophical question about reality vs AI. Creates immediate "what if" curiosity.
VISUAL TIP: Rapid montage of AI faces with "FAKE" watermark appearing.

HOOK 3 TEXT: "The AI arms race to create perfect humans is happening now. I tested the frontlines."
WHY IT WORKS: "Arms race" framing adds urgency. Positional authority as tester.
VISUAL TIP: War room aesthetic with maps and "AI vs AI" battlefield graphic.'''
        else:
            # BETTER PROMPT for real API
            hook_prompt = f"""Create 3 viral YouTube hooks about this topic: {topic}

IMPORTANT: Do NOT repeat the topic description. Create ORIGINAL, ENGAGING hooks.

For each hook, provide ONLY:
1. HOOK TEXT: [The exact hook wording in quotes]
2. WHY IT WORKS: [Brief psychology explanation]
3. VISUAL TIP: [How to execute visually]

Make hooks URGENT, CURIOUS, and STOPPING.

Topic context: {topic}"""
            
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You are a viral YouTube hook expert. Create ORIGINAL hooks, do not repeat the input."},
                        {"role": "user", "content": hook_prompt}
                    ],
                    "stream": False,
                    "temperature": 0.8  # More creative
                },
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}")
            
            ai_text = response.json()["choices"][0]["message"]["content"]
        
        # SIMPLE PARSER
        hooks = []
        current_hook = {}
        
        for line in ai_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            
            if 'hook' in line_lower and 'text' in line_lower:
                if current_hook and current_hook.get('text'):
                    hooks.append(current_hook)
                # Extract text
                text = line.split(':', 1)[1].strip() if ':' in line else line
                text = text.strip('"')
                current_hook = {'text': text}
            elif 'why it works' in line_lower and 'psychology' not in current_hook:
                current_hook['psychology'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif 'visual tip' in line_lower and 'visual' not in current_hook:
                current_hook['visual'] = line.split(':', 1)[1].strip() if ':' in line else line
        
        if current_hook and current_hook.get('text'):
            hooks.append(current_hook)
        
        # Fallback if parsing fails
        if not hooks:
            hooks = [
                {'text': 'The AI face generator that\'s too realistic to be comfortable', 'psychology': 'Uncanny valley fascination', 'visual': 'Close-up face montage'},
                {'text': 'Two AIs in an endless battle to create and detect fake humans', 'psychology': 'Dramatic conflict narrative', 'visual': 'Split screen battle animation'},
                {'text': 'What if every person you see online was AI-generated?', 'psychology': 'Reality-questioning curiosity', 'visual': 'Reality vs AI comparison'}
            ]
        
        hooks = hooks[:3]
        
        # YOUR TURQUOISE COLOR: #0d96c1
        TURQUOISE = "#0d96c1"
        TURQUOISE_LIGHT = "#ecfeff"
        TURQUOISE_DARK = "#0c4a6e"
        
        # Build hook cards with YOUR turquoise theme
        hooks_html = ""
        for i, hook in enumerate(hooks):
            hooks_html += f'''
<div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; border: 2px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.1);">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <div style="background: {TURQUOISE}; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
            {i+1}
        </div>
        <h3 style="margin: 0; color: {TURQUOISE};">Hook {i+1}</h3>
    </div>
    
    <!-- MAIN HOOK TEXT -->
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.5rem; font-weight: 600;">
            <i class="fas fa-quote-left"></i> HOOK TEXT
        </div>
        <div style="font-size: 1.2rem; line-height: 1.5; padding: 1.5rem; background: {TURQUOISE_LIGHT}; border-radius: 8px; border-left: 4px solid {TURQUOISE}; color: {TURQUOISE_DARK}; font-family: 'Georgia', serif;">
            "{hook.get('text', 'No hook text available')}"
        </div>
    </div>
    
    <!-- Tips -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
        <div style="padding: 0.75rem; border-radius: 6px; background: {TURQUOISE_LIGHT}; border: 1px solid #a5f3fc;">
            <div style="font-size: 0.8rem; color: {TURQUOISE}; margin-bottom: 0.25rem; font-weight: 600;">
                <i class="fas fa-brain"></i> Why It Works
            </div>
            <div style="font-size: 0.9rem; color: {TURQUOISE_DARK};">
                {hook.get('psychology', 'Creates engagement')}
            </div>
        </div>
        
        <div style="padding: 0.75rem; border-radius: 6px; background: {TURQUOISE_LIGHT}; border: 1px solid #a5f3fc;">
            <div style="font-size: 0.8rem; color: {TURQUOISE}; margin-bottom: 0.25rem; font-weight: 600;">
                <i class="fas fa-video"></i> Visual Tip
            </div>
            <div style="font-size: 0.9rem; color: {TURQUOISE_DARK};">
                {hook.get('visual', 'Use engaging visuals')}
            </div>
        </div>
    </div>
</div>
'''
        
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; color: {TURQUOISE};">
            <i class="fas fa-fish-hook"></i>
        </div>
        <h1 style="color: {TURQUOISE};">Hook Options Ready!</h1>
        <p style="color: #64748b;">For <strong>{platform.title()}</strong> • <strong>{type.title()}</strong> • <strong>{audience.title()}</strong></p>
        <div style="background: {TURQUOISE_LIGHT}; padding: 0.75rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #a5f3fc;">
            <p style="color: {TURQUOISE_DARK}; margin: 0;"><i class="fas fa-bullseye"></i> <strong>Topic:</strong> {topic[:100]}{'...' if len(topic) > 100 else ''}</p>
        </div>
    </div>
    
    {hooks_html}
    
    <div style="text-align: center; margin-top: 3rem;">
        <a href="wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-fish-hook"></i> Create More Hooks
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
    
    return HTMLResponse(layout("Hook Options", result_content))

# ========== HELPER FUNCTIONS ==========
# PUT THESE RIGHT HERE, AFTER /process BUT BEFORE /result

def get_platform_requirements(platform: str) -> str:
    requirements = {
        "tiktok": "• MUST grab attention in FIRST 1-2 seconds\n• Use trending sounds/text-on-screen\n• Fast cuts, high energy\n• Clear value proposition immediately",
        "youtube": "• Beat the 5-second skip\n• State value within 10 seconds\n• Use curiosity gap\n• Preview what's coming",
        "instagram": "• Visual-first hooks\n• Text overlay crucial\n• Reels format (9:16)\n• Quick setup, fast payoff",
        "linkedin": "• Professional/value-first\n• Problem/solution framing\n• Credibility indicators\n• Clear target audience",
        "twitter": "• Thread starter hooks\n• Controversy/curiosity\n• Short, punchy\n• Retweetable",
        "facebook": "• Storytelling hooks\n• Emotional connection\n• Shareable content\n• Community-focused"
    }
    return requirements.get(platform, "• Grab attention immediately\n• Clear value proposition\n• Platform-appropriate tone")

def get_hook_type_guidelines(hook_type: str) -> str:
    guidelines = {
        "question": "• Must make viewer answer internally\n• Should be personally relevant\n• Creates immediate engagement\n• Leads naturally to content",
        "shocking": "• Stat/fact must be genuinely surprising\n• Should challenge assumptions\n• Source credibility helps\n• Visual representation powerful",
        "story": "• Personal/relatable anecdote\n• Should have emotional hook\n• Quick setup (2-3 sentences)\n• Clear connection to topic",
        "controversy": "• Bold stance or unpopular opinion\n• Should be defendable\n• Creates discussion/engagement\n• Know your audience limits",
        "howto": "• Clear benefit promised\n• Should seem achievable\n• Specific, not vague\n• Results-oriented language",
        "fear": "• Pain point identification\n• Solution promised\n• Should be legitimate concern\n• Empowering, not paralyzing"
    }
    return guidelines.get(hook_type, "• Grab attention\n• Create curiosity\n• Promise value\n• Lead to content")

def get_topic_guidance(topic: str) -> str:
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ["ai", "artificial", "generated", "machine learning"]):
        return "• Focus on technology, futurism, ethics\n• Highlight uncanny valley, implications\n• Use tech-savvy but accessible language"
    elif any(word in topic_lower for word in ["review", "product", "service", "app"]):
        return "• Focus on value, features, pros/cons\n• Highlight pain points and solutions\n• Use authentic, experience-based language"
    elif any(word in topic_lower for word in ["tutorial", "how to", "guide", "learn"]):
        return "• Focus on transformation, results\n• Highlight before/after, ease of learning\n• Use empowering, step-by-step language"
    elif any(word in topic_lower for word in ["vlog", "personal", "story", "day in life"]):
        return "• Focus on authenticity, connection\n• Highlight relatable moments, emotions\n• Use conversational, intimate language"
    else:
        return "• Tailor hooks specifically to this topic\n• Use topic-relevant language and examples\n• Make hooks feel custom, not generic"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
             

# ---------- PROMPTS WIZARD -----------
# This tells Python to look in root folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now this imports from ROOT layout.py
from layout import layout

app = FastAPI()






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
            <a href="wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
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
            <a href="wizard" role="button" class="secondary">Back</a>
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
@app.post("/prompt-wizard/process")
async def process_prompt(
    goal: str = Form(...),
    audience: str = Form(...),
    platform: str = Form(...),
    style: str = Form(...),
    tone: str = Form(...),
    prompt: str = Form(...)
):
    DEEPSEEK_KEY = os.getenv("PROMPT_WIZARD_API_KEY")
    
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
        <a href="wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-hat-wizard"></i> Create Another Prompt
        </a>
        <a href="" role="button" style="background: #64748b; border-color: #64748b;">
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
    

# ---------- THUMBNAIL WIZARD -----------
# This tells Python to look in root folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now this imports from ROOT layout.py
from layout import layout
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Create necessary directories
os.makedirs("uploads", exist_ok=True)

# API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

print("=" * 50)
print("AI THUMBNAIL WIZARD")
print(f"DEEPSEEK_API_KEY loaded: {'✅ Yes' if DEEPSEEK_API_KEY else '❌ No - Add to .env'}")
print("=" * 50)



# Add this debug endpoint to see the full layout
@app.get("/debug-layout")
async def debug_layout():
    # Show what layout() produces with minimal content
    test_content = "<h1>Test</h1>"
    full_html = layout("Test", test_content)
    
    # Return first 2000 chars to see navbar
    return HTMLResponse(f"<pre>{full_html[:2000]}</pre>")



# ========== HOME / UPLOAD PAGE ==========
@app.get("/")
async def home():
    content = '''
    <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <div style="margin-bottom: 3rem;">
            <div style="font-size: 4rem; color: var(--primary); margin-bottom: 1rem;">
                <i class="fas fa-hat-wizard"></i>
            </div>
            <h1 style="color: var(--primary);">Thumbnail Wizard</h1>
            <p style="color: #6b7280; font-size: 1.2rem;">
                AI-Powered Thumbnail Analysis & Optimization
            </p>
        </div>
        
        <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <form action="/analyze" method="post" enctype="multipart/form-data">
                
                <div style="margin-bottom: 2rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; text-align: left;">
                        <i class="fas fa-globe"></i> Platform
                    </label>
                    <select name="platform" style="width: 100%; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #d1d5db;">
                        <option value="youtube">YouTube (1280×720)</option>
                        <option value="tiktok">TikTok/Shorts (1080×1920)</option>
                        <option value="instagram">Instagram (1080×1080)</option>
                        <option value="facebook">Facebook (1200×630)</option>
                        <option value="linkedin">LinkedIn (1200×627)</option>
                        <option value="twitter">Twitter/X (1200×675)</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 2rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; text-align: left;">
                        <i class="fas fa-image"></i> Upload Your Thumbnail
                    </label>
                    <input type="file" name="image" accept="image/*" required
                           style="width: 100%; padding: 1rem; border: 2px dashed #d1d5db; border-radius: 0.5rem; background: #f9fafb;">
                    <small style="display: block; margin-top: 0.5rem; color: #6b7280; text-align: left;">
                        JPG, PNG, or GIF • Max 5MB
                    </small>
                </div>
                
                <div style="margin-bottom: 2rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: bold; text-align: left;">
                        <i class="fas fa-comment-alt"></i> Content Context (Helps AI)
                    </label>
                    <textarea name="description" rows="3" 
                              placeholder="Tell us about this thumbnail: What's the video/article about? Who's the target audience? What's the main goal?"
                              style="width: 100%; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid #d1d5db;"></textarea>
                    <small style="display: block; margin-top: 0.5rem; color: #6b7280; text-align: left;">
                        Optional but highly recommended for personalized feedback
                    </small>
                </div>
                
                <button type="submit" style="width: 100%; padding: 1rem; background: var(--primary); color: white; border: none; border-radius: 0.5rem; font-size: 1.1rem; cursor: pointer; transition: all 0.2s;">
                    <i class="fas fa-magic"></i> Analyze with AI Wizard
                </button>
                
                <div style="margin-top: 1rem; padding: 1rem; background: #f0f9ff; border-radius: 0.5rem;">
                    <p style="color: var(--primary); margin: 0; font-size: 0.9rem;">
                        <i class="fas fa-bolt"></i> Powered by DeepSeek AI • Analysis takes 10-20 seconds
                    </p>
                </div>
            </form>
        </div>
        
        <!-- Features -->
        <div style="margin-top: 3rem;">
            <h3 style="color: var(--primary); text-align: center; margin-bottom: 1.5rem;">
                <i class="fas fa-star"></i> What Our AI Analyzes
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 2rem; color: var(--primary); margin-bottom: 0.5rem;">
                        <i class="fas fa-eye"></i>
                    </div>
                    <h4 style="margin: 0;">Visual Hierarchy</h4>
                    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;">What viewers notice first</p>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 2rem; color: var(--primary); margin-bottom: 0.5rem;">
                        <i class="fas fa-text-height"></i>
                    </div>
                    <h4 style="margin: 0;">Readability Score</h4>
                    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;">Text clarity on all devices</p>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 2rem; color: var(--primary); margin-bottom: 0.5rem;">
                        <i class="fas fa-palette"></i>
                    </div>
                    <h4 style="margin: 0;">Color Psychology</h4>
                    <p style="font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;">Emotional impact of colors</p>
                </div>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Thumbnail Wizard", content))

# ========== AI ANALYSIS ==========
@app.post("/analyze")
async def analyze_thumbnail(
    image: UploadFile = File(...),
    platform: str = Form("youtube"),
    description: str = Form("")
):
    # Save uploaded image
    analysis_id = str(uuid.uuid4())[:8]
    upload_path = f"uploads/{analysis_id}_{image.filename}"
    
    with open(upload_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)
    
    # Convert image to base64 for display
    try:
        img = Image.open(upload_path)
        # Resize for display
        img.thumbnail((400, 400))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        display_base64 = base64.b64encode(buffered.getvalue()).decode()
        has_image = True
    except Exception as e:
        display_base64 = None
        has_image = False
    
    # Show loading page
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-hat-wizard"></i>
        </div>
        
        <h1 style="color: var(--primary);">AI Wizard is Analyzing...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            DeepSeek AI is reviewing your {platform} thumbnail
        </p>
        
        <div style="width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; margin: 2rem 0; overflow: hidden;">
            <div style="height: 100%; background: linear-gradient(90deg, var(--primary), #a78bfa); border-radius: 4px; animation: loading 2s infinite; width: 60%;"></div>
        </div>
        
        <style>
            @keyframes loading {{
                0% {{ transform: translateX(-100%); }}
                100% {{ transform: translateX(350%); }}
            }}
        </style>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            <i class="fas fa-clock"></i> AI analysis takes 10-20 seconds
        </p>
        
        <meta http-equiv="refresh" content="2;url=/analyze_result?analysis_id={analysis_id}&platform={platform}&description={description}">
    </div>
    '''
    
    return HTMLResponse(layout("Analyzing...", loading_content))

# ========== ANALYSIS RESULT ==========
@app.get("/analyze_result")
async def analyze_result(
    analysis_id: str,
    platform: str = "youtube",
    description: str = ""
):
    # Get the latest uploaded image for this analysis
    uploads_dir = "uploads"
    latest_file = None
    if os.path.exists(uploads_dir):
        files = [f for f in os.listdir(uploads_dir) if analysis_id in f]
        if files:
            latest_file = os.path.join(uploads_dir, files[0])
    
    # Convert image to base64 for display
    display_base64 = None
    if latest_file:
        try:
            img = Image.open(latest_file)
            img.thumbnail((400, 400))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            display_base64 = base64.b64encode(buffered.getvalue()).decode()
        except:
            pass
    
    # Get AI analysis
    analysis = get_ai_thumbnail_analysis(platform, description)
    
    # Build the result page
    content = f'''
    <div style="max-width: 1000px; margin: 0 auto;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; color: var(--primary);">
                <i class="fas fa-check-circle"></i>
            </div>
            <h1 style="color: var(--primary);">AI Analysis Complete</h1>
            <p style="color: #64748b;">
                <strong>{platform.title()}</strong> thumbnail • 
                {'✅ Using DeepSeek AI' if DEEPSEEK_API_KEY else '⚠️ Enhanced Analysis (add API key for real AI)'}
            </p>
        </div>
        
        <!-- Thumbnail Preview & Score -->
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; margin-bottom: 3rem;">
            <!-- Score Card -->
            <div style="background: white; border-radius: 1rem; padding: 2rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 4rem; font-weight: bold; color: var(--primary); margin-bottom: 1rem;">
                    {analysis["score"]}/10
                </div>
                <div style="height: 12px; background: #e5e7eb; border-radius: 6px; margin-bottom: 1rem; overflow: hidden;">
                    <div style="height: 100%; width: {analysis["score"] * 10}%; background: var(--primary);"></div>
                </div>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">Overall Score</p>
                
    '''
    
    if display_base64:
        content += f'''
                <div style="margin-top: 2rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem;">
                    <img src="data:image/png;base64,{display_base64}" style="max-width: 100%; border-radius: 0.5rem;">
                    <p style="color: #6b7280; margin-top: 0.5rem; font-size: 0.9rem;">Your Thumbnail</p>
                </div>
        '''
    
    content += f'''
                <div style="margin-top: 1.5rem; padding: 1rem; background: #f0f9ff; border-radius: 0.75rem;">
                    <p style="color: var(--primary); margin: 0; font-size: 0.9rem;">
                        <i class="fas fa-bolt"></i> Potential CTR improvement: <strong>{analysis["estimated_ctr_improvement"]}</strong>
                    </p>
                </div>
            </div>
            
            <!-- Overall Assessment -->
            <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: var(--primary); margin-bottom: 1rem;">
                    <i class="fas fa-clipboard-check"></i> AI Assessment
                </h3>
                <p style="color: #4b5563; line-height: 1.6; margin-bottom: 2rem;">{analysis["overall"]}</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <!-- Strengths -->
                    <div>
                        <h4 style="color: #10b981; margin-bottom: 1rem;">
                            <i class="fas fa-check-circle"></i> What Works Well
                        </h4>
                        <ul style="list-style: none; padding: 0; margin: 0;">
    '''
    
    for strength in analysis["strengths"]:
        content += f'''
                            <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                                <i class="fas fa-check" style="color: #10b981; position: absolute; left: 0;"></i> {strength}
                            </li>
        '''
    
    content += '''
                        </ul>
                    </div>
                    
                    <!-- Improvements -->
                    <div>
                        <h4 style="color: #f59e0b; margin-bottom: 1rem;">
                            <i class="fas fa-exclamation-circle"></i> Areas for Improvement
                        </h4>
                        <ul style="list-style: none; padding: 0; margin: 0;">
    '''
    
    for improvement in analysis["improvements"]:
        content += f'''
                            <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                                <i class="fas fa-arrow-up" style="color: #f59e0b; position: absolute; left: 0;"></i> {improvement}
                            </li>
        '''
    
    content += f'''
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Actionable Fixes -->
        <div style="background: white; border-radius: 1rem; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="color: var(--primary); margin-bottom: 1.5rem;">
                <i class="fas fa-tools"></i> Actionable Fixes You Can Implement Now
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
    '''
    
    for i, fix in enumerate(analysis["actionable_fixes"]):
        content += f'''
                <div style="background: #f9fafb; padding: 1.25rem; border-radius: 0.75rem; border-left: 4px solid var(--primary);">
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <div style="background: var(--primary); color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0;">
                            {i+1}
                        </div>
                        <p style="margin: 0; color: #4b5563;">{fix}</p>
                    </div>
                </div>
        '''
    
    content += f'''
            </div>
        </div>
        
        <!-- AI Suggestions -->
        <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;">
            <h3 style="color: var(--primary); margin-bottom: 1.5rem;">
                <i class="fas fa-lightbulb"></i> AI Creative Suggestions
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
    '''
    
    for suggestion in analysis["ai_suggestions"]:
        content += f'''
                <div style="background: white; padding: 1.25rem; border-radius: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <div style="color: var(--secondary); font-size: 1.25rem;">
                            <i class="fas fa-sparkles"></i>
                        </div>
                        <p style="margin: 0; color: #4b5563;">{suggestion}</p>
                    </div>
                </div>
        '''
    
    content += f'''
            </div>
        </div>
        
        <!-- Platform Specific -->
        <div style="background: white; border-radius: 1rem; padding: 2rem; margin-bottom: 3rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">
                <i class="fas fa-mobile-alt"></i> {platform.title()}-Specific Optimization
            </h3>
            <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; border-left: 4px solid var(--secondary);">
                <p style="margin: 0; color: #4b5563; line-height: 1.6;">{analysis["platform_specific"]}</p>
            </div>
        </div>
        
        <!-- CTA -->
        <div style="text-align: center; margin-bottom: 3rem;">
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="/" role="button" style="padding: 1rem 2rem;">
                    <i class="fas fa-redo"></i> Analyze Another Thumbnail
                </a>
                <a href="#" role="button" class="secondary" style="padding: 1rem 2rem; background: var(--secondary);">
                    <i class="fas fa-download"></i> Save This Report
                </a>
            </div>
        </div>
        
        <!-- Upgrade CTA -->
        <div style="background: linear-gradient(135deg, var(--primary), #7c3aed); color: white; border-radius: 1rem; padding: 2rem; text-align: center;">
            <h3 style="margin-bottom: 1rem;">
                <i class="fas fa-crown"></i> Want AI to Create Thumbnails For You?
            </h3>
            <p style="margin-bottom: 1.5rem; opacity: 0.9;">Coming soon: AI thumbnail generation with one click</p>
            
            <a href="#" role="button" style="background: white; color: var(--primary); border: none; padding: 1rem 2rem;">
                <i class="fas fa-bell"></i> Notify Me When Ready
            </a>
        </div>
    </div>
    '''
    
    return HTMLResponse(layout("Analysis Results", content))

def get_ai_thumbnail_analysis(platform: str, description: str = "") -> dict:
    """Get AI analysis from DeepSeek API"""
    
    if not DEEPSEEK_API_KEY:
        return get_mock_analysis(platform)
    
    try:
        # Enhanced prompt for better analysis
        prompt = f"""As a professional thumbnail designer with expertise in viral content and conversion optimization, analyze this thumbnail for {platform}.

CONTEXT: {description if description else "General content thumbnail"}

Please provide a comprehensive analysis including:

1. SCORE: Overall effectiveness score 1-10
2. OVERALL: Brief summary assessment
3. STRENGTHS: 3-4 things that work well
4. IMPROVEMENTS: 3-4 specific areas needing improvement
5. ACTIONABLE_FIXES: 4-5 concrete, implementable fixes
6. AI_SUGGESTIONS: 3-4 creative AI-powered suggestions
7. PLATFORM_SPECIFIC: Optimization tips for {platform}
8. ESTIMATED_CTR_IMPROVEMENT: Estimated click-through rate improvement percentage if fixes are implemented

Be specific, data-driven, and practical. Focus on what actually drives clicks and engagement on {platform}. Provide actionable advice that a non-designer can implement.

Return as valid JSON only."""

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": """You are ThumbnailGPT, an expert thumbnail designer with 15+ years experience creating viral thumbnails for top YouTubers, brands, and content creators. You analyze thumbnails based on proven psychological principles, platform-specific best practices, and conversion rate optimization data. You provide specific, actionable feedback that users can implement immediately to improve their click-through rates."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            
            # Try to extract JSON
            try:
                # Clean the response
                ai_response = ai_response.strip()
                # Remove markdown code blocks if present
                if ai_response.startswith("```"):
                    lines = ai_response.split('\n')
                    ai_response = '\n'.join(lines[1:-1]) if lines[-1] == "```" else '\n'.join(lines[1:])
                
                # Parse JSON
                analysis = json.loads(ai_response)
                
                # Validate required fields
                required_fields = ["score", "overall", "strengths", "improvements", 
                                 "actionable_fixes", "ai_suggestions", "platform_specific", 
                                 "estimated_ctr_improvement"]
                
                for field in required_fields:
                    if field not in analysis:
                        analysis[field] = get_mock_analysis(platform)[field]
                
                return analysis
                
            except json.JSONDecodeError:
                print("Failed to parse AI response as JSON")
                return get_mock_analysis(platform)
                
        else:
            print(f"DeepSeek API error: {response.status_code}")
            return get_mock_analysis(platform)
            
    except Exception as e:
        print(f"Error calling DeepSeek: {str(e)}")
        return get_mock_analysis(platform)

def get_mock_analysis(platform: str) -> dict:
    """High-quality mock analysis when API is not available"""
    return {
        "score": 7.8,
        "overall": f"This thumbnail shows solid fundamentals for {platform} with good composition and color usage. However, it lacks some key elements that drive high click-through rates on this platform. With a few strategic improvements, you could see significant engagement increases.",
        
        "strengths": [
            "Effective use of contrasting colors that grab attention in feeds",
            "Clear focal point that immediately tells viewers what to look at",
            "Good text-to-image ratio appropriate for mobile viewing",
            "Appropriate use of negative space for clean composition"
        ],
        
        "improvements": [
            "Text needs to be 40-50% larger for better mobile readability",
            "Missing human face/eyes which typically increase CTR by 30-40%",
            "Could use stronger emotional hook in the imagery",
            "Lacks a clear call-to-action element"
        ],
        
        "actionable_fixes": [
            f"Increase all text size by at least 50% for {platform} mobile optimization",
            "Add a human face looking at the camera or text (increases engagement significantly)",
            "Apply a subtle vignette or glow effect to draw attention to the center",
            "Increase color saturation by 20% for more scroll-stopping power",
            "Add a border or drop shadow to text for better readability"
        ],
        
        "ai_suggestions": [
            "Try using the 'rule of thirds' to position key elements more effectively",
            "Experiment with complementary color schemes (e.g., orange/blue, purple/yellow)",
            "Consider adding an arrow or pointer element to guide viewer attention",
            "Test adding social proof elements like '1M views' or 'Trending' badges"
        ],
        
        "platform_specific": get_platform_tips(platform),
        
        "estimated_ctr_improvement": "45-65% with suggested optimizations"
    }

def get_platform_tips(platform: str) -> str:
    """Get detailed platform-specific tips"""
    tips = {
        "youtube": """YouTube thumbnails are critical for click-through rate. Key optimization tips:
1. BRIGHT COLORS: Use vibrant, high-contrast colors that stand out in search results
2. HUMAN FACES: Close-up faces with expressive emotions (especially eyes looking at camera) increase CTR by 35%
3. MINIMAL TEXT: 3-5 words maximum, large and bold, readable at thumbnail size
4. MYSTERY & CURIOSITY: Create intrigue without giving everything away
5. CONSISTENCY: Use similar style/colors across your channel for brand recognition
6. TESTING: Always A/B test thumbnails using YouTube's built-in testing feature""",
        
        "tiktok": """TikTok/Shorts thumbnails need to work at small sizes and auto-play:
1. ACTION FRAMES: Choose frames showing movement or dramatic expressions
2. BRIGHT & BOLD: High saturation colors perform best in fast-scrolling feeds
3. MINIMAL TEXT: Most viewers won't pause to read, so text should be minimal
4. FACES SELL: Emotional human faces (surprise, joy, shock) drive engagement
5. FIRST 3 SECONDS: Thumbnail should represent the most engaging moment
6. BRAND COLORS: Consistent color scheme helps with channel recognition""",
        
        "instagram": """Instagram values aesthetics and consistency:
1. GRID VIEW: Thumbnail must work in 3×3 grid at small size
2. BRAND AESTHETIC: Maintain consistent filters, colors, and style
3. REELS OPTIMIZATION: For Reels, choose frames with action or transformation
4. TEXT OVERLAY: Many users watch without sound, so text can help
5. QUALITY OVER QUANTITY: High-quality, professional imagery performs better
6. STORYTELLING: Thumbnail should hint at the story or value in the post""",
        
        "facebook": """Facebook thumbnails often auto-play without sound:
1. TEXT NECESSARY: Include clear text overlay since many watch muted
2. EMOTIONAL HOOK: Images that evoke emotion (surprise, curiosity, humor) perform best
3. NEWS VALUE: For articles, make it look newsworthy and urgent
4. FACEBOOK BLUE: Blue accents can increase trust and recognition
5. SQUARE FORMAT: Works best across News Feed and mobile
6. CALL TO ACTION: Subtle arrows or 'Watch Now' text can improve clicks""",
        
        "linkedin": """LinkedIn requires professional yet engaging thumbnails:
1. CLEAN & PROFESSIONAL: Avoid overly flashy or casual styles
2. DATA VISUALIZATION: Infographics and charts perform exceptionally well
3. BRAND COLORS: Use your company's color palette
4. TEXT CLARITY: Professional fonts, good contrast, readable on all devices
5. VALUE PROPOSITION: Clearly show what value the content provides
6. CREDIBILITY ELEMENTS: Logos, certifications, or expert photos add authority""",
        
        "twitter": """Twitter/X thumbnails need to stand out in busy timelines:
1. HIGH CONTRAST: Must be visible at very small sizes
2. CONTROVERSY/INTRIGUE: Controversial or intriguing images get more clicks
3. MINIMALIST: Simple compositions work best at small sizes
4. BRIGHT COLORS: Stand out against Twitter's white/light background
5. TEXT ESSENTIAL: Many users need text to understand context
6. URGENCY: Creates a fear of missing out (FOMO)"""
    }
    return tips.get(platform, tips["youtube"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
    

# ---------- VIDEO WIZARD -----------
app = FastAPI()
# You'll need a different AI key for video analysis (GPT-4 Vision maybe)
DEEPSEEK_KEY = os.getenv("VIDEO_WIZARD_API_KEY")  # Might need different model



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
            <i class="fas fa-video"></i><br>
            Video Alchemy
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            AI-powered video optimization. Get platform-specific fixes in 6 steps.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-magic"></i> Start Video Wizard
            </a>
        </div>
        
        <div class="card-grid">
            <div class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube</h3>
                <p>Increase retention & views</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok</h3>
                <p>Master the algorithm</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram</h3>
                <p>Reels & IGTV optimization</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn</h3>
                <p>Professional video tips</p>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Home", content))

# ========== STEP 1: PLATFORM ==========
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 1: Choose Platform</h1>
        <p style="text-align: center; color: #6b7280;">
            Where is your video published or will be published?
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step2?platform=youtube" class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube</h3>
                <p>Long-form, monetization</p>
            </a>
            
            <a href="/wizard/step2?platform=tiktok" class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok</h3>
                <p>Short-form, viral potential</p>
            </a>
            
            <a href="/wizard/step2?platform=instagram" class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram</h3>
                <p>Reels, Stories, IGTV</p>
            </a>
            
            <a href="/wizard/step2?platform=linkedin" class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn</h3>
                <p>Professional, B2B</p>
            </a>
            
            <a href="/wizard/step2?platform=facebook" class="step-card">
                <i class="fab fa-facebook"></i>
                <h3>Facebook</h3>
                <p>Groups, Pages, viral</p>
            </a>
            
            <a href="/wizard/step2?platform=twitter" class="step-card">
                <i class="fab fa-twitter"></i>
                <h3>Twitter/X</h3>
                <p>Short clips, threads</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" role="button" class="secondary">Cancel</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 1: Platform", content))

# ========== STEP 2: VIDEO TYPE ==========
@app.get("/wizard/step2")
async def step2(platform: str = Query("youtube")):
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 2: Video Type</h1>
        <p style="text-align: center; color: #6b7280;">
            What kind of video is this?
        </p>
        
        <p style="text-align: center;"><strong>Platform:</strong> {platform.title()}</p>
        
        <div class="card-grid">
            <a href="/wizard/step3?platform={platform}&type=tutorial" class="step-card">
                <i class="fas fa-chalkboard-teacher"></i>
                <h3>Tutorial</h3>
                <p>How-to, educational</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=vlog" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Vlog</h3>
                <p>Personal, day-in-life</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=review" class="step-card">
                <i class="fas fa-star"></i>
                <h3>Review</h3>
                <p>Product, service, media</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=entertainment" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Entertainment</h3>
                <p>Comedy, skits, fun</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=educational" class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Educational</h3>
                <p>Deep dive, explainer</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Marketing, pitch, update</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="wizard" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 2: Video Type", content))

# ========== STEP 3: GOAL ==========
@app.get("/wizard/step3")
async def step3(platform: str = Query("youtube"), type: str = Query("tutorial")):
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 3: Choose Goal</h1>
        <p style="text-align: center; color: #6b7280;">
            What do you want to improve?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step4?platform={platform}&type={type}&goal=retention" class="step-card">
                <i class="fas fa-clock"></i>
                <h3>Retention</h3>
                <p>Keep viewers watching longer</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=views" class="step-card">
                <i class="fas fa-eye"></i>
                <h3>More Views</h3>
                <p>Increase view count</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=algorithm" class="step-card">
                <i class="fas fa-robot"></i>
                <h3>Algorithm</h3>
                <p>Better platform ranking</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=engagement" class="step-card">
                <i class="fas fa-comments"></i>
                <h3>Engagement</h3>
                <p>More likes, comments, shares</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=seo" class="step-card">
                <i class="fas fa-search"></i>
                <h3>SEO</h3>
                <p>Better search visibility</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=conversion" class="step-card">
                <i class="fas fa-shopping-cart"></i>
                <h3>Conversion</h3>
                <p>More clicks, sales, signups</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step2?platform={platform}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 3: Goal", content))

# ========== STEP 4: AUDIENCE ==========
@app.get("/wizard/step4")
async def step4(platform: str = Query("youtube"), type: str = Query("tutorial"), goal: str = Query("retention")):
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 4: Choose Audience</h1>
        <p style="text-align: center; color: #6b7280;">
            Who is your target viewer?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()} • 
            <strong>Goal:</strong> {goal.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=beginners" class="step-card">
                <i class="fas fa-baby"></i>
                <h3>Beginners</h3>
                <p>New to the topic</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=intermediate" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Intermediate</h3>
                <p>Some experience</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=experts" class="step-card">
                <i class="fas fa-user-graduate"></i>
                <h3>Experts</h3>
                <p>Advanced knowledge</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=general" class="step-card">
                <i class="fas fa-users"></i>
                <h3>General</h3>
                <p>Broad audience</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Professionals, B2B</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=creators" class="step-card">
                <i class="fas fa-paint-brush"></i>
                <h3>Creators</h3>
                <p>Other content creators</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step3?platform={platform}&type={type}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 4: Audience", content))

# ========== STEP 5: TONE ==========
@app.get("/wizard/step5")
async def step5(platform: str = Query("youtube"), type: str = Query("tutorial"), goal: str = Query("retention"), audience: str = Query("beginners")):
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
            What's the video's personality?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()} • 
            <strong>Goal:</strong> {goal.title()} • 
            <strong>Audience:</strong> {audience.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=friendly" class="step-card">
                <i class="fas fa-smile"></i>
                <h3>Friendly</h3>
                <p>Warm, approachable</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=professional" class="step-card">
                <i class="fas fa-suitcase"></i>
                <h3>Professional</h3>
                <p>Formal, business-like</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=energetic" class="step-card">
                <i class="fas fa-bolt"></i>
                <h3>Energetic</h3>
                <p>Fast-paced, exciting</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=calm" class="step-card">
                <i class="fas fa-spa"></i>
                <h3>Calm</h3>
                <p>Relaxed, soothing</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=humorous" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Humorous</h3>
                <p>Funny, entertaining</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=authoritative" class="step-card">
                <i class="fas fa-crown"></i>
                <h3>Authoritative</h3>
                <p>Expert, confident</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step4?platform={platform}&type={type}&goal={goal}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 5: Tone", content))

# ========== STEP 6: VIDEO INPUT ==========
@app.get("/wizard/step6")
async def step6(
    platform: str = Query("youtube"),
    type: str = Query("tutorial"),
    goal: str = Query("retention"),
    audience: str = Query("beginners"),
    tone: str = Query("friendly")
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
        
        <h1 style="text-align: center; color: var(--primary);">Step 6: Video Details</h1>
        <p style="text-align: center; color: #6b7280;">
            Tell us about your video
        </p>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Selections:</h3>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 1rem 0;">
                <div><strong>Platform:</strong><br>{platform.title()}</div>
                <div><strong>Type:</strong><br>{type.title()}</div>
                <div><strong>Goal:</strong><br>{goal.title()}</div>
                <div><strong>Audience:</strong><br>{audience.title()}</div>
                <div><strong>Tone:</strong><br>{tone.title()}</div>
            </div>
        </div>
        
        <div style="background: #f0f9ff; border: 2px solid #10b981; border-radius: 0.75rem; padding: 1rem; margin: 1rem 0;">
    <p style="margin: 0; color: #065f46; display: flex; align-items: center; gap: 0.5rem;">
        <i class="fas fa-lightbulb" style="color: #10b981;"></i>
        <strong>Pro Tip:</strong> Even brief descriptions work! AI analyzes 
        <strong>video structure & platform optimization</strong>, not specific content.
    </p>
</div>

        <form action="/process" method="POST">
            <input type="hidden" name="platform" value="{platform}">
            <input type="hidden" name="type" value="{type}">
            <input type="hidden" name="goal" value="{goal}">
            <input type="hidden" name="audience" value="{audience}">
            <input type="hidden" name="tone" value="{tone}">
            
            <div style="margin: 2rem 0;">
                <label for="video_url">
                    <strong>YouTube Video URL:</strong>
                    <p style="color: #6b7280; margin: 0.5rem 0;">Paste a public YouTube link (we'll analyze the title, description, etc.)</p>
                </label>
                <input type="url" id="video_url" name="video_url" 
                       placeholder="https://www.youtube.com/watch?v=..." 
                       class="url-input">
            </div>
            
            <div style="margin: 2rem 0;">
    <label for="video_description">
        <strong>Video Description:</strong>
        <p style="color: #6b7280; margin: 0.5rem 0;">
            Describe your video's <strong>core content only</strong>.
            <span style="color: #ef4444; display: block; margin-top: 0.5rem; font-size: 0.9rem;">
                ⚠️ Skip ad/sponsorship segments. AI analyzes based on this description.
            </span>
        </p>
    </label>
    <textarea id="video_description" name="video_description" rows="6" 
              placeholder="Example: 'Tutorial showing 3 paper airplane designs. Starts with basic dart, then Nakamura lock, finally Suzanne for distance. Key moments: 0:30 basic fold, 1:45 advanced technique, 3:20 flight test.'"
              style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem;"></textarea>
</div>
            
            <div style="text-align: center; margin: 2rem 0;">
                <button type="submit" style="padding: 1rem 3rem; font-size: 1.2rem;">
                    <i class="fas fa-chart-line"></i> Analyze & Optimize Video
                </button>
                <p style="margin-top: 1rem; color: #6b7280;">
                    <i class="fas fa-clock"></i> AI analysis takes 15-30 seconds
                </p>
            </div>
        </form>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience={audience}" 
               role="button" class="secondary">Back</a>
        </div>
    </div>

    

    '''
    return HTMLResponse(layout("Step 6: Video Details", content))

# ========== PROCESS ==========
@app.post("/thumbnail-wizard/process")
async def process_video(
    platform: str = Form(...),
    type: str = Form(...),
    goal: str = Form(...),
    audience: str = Form(...),
    tone: str = Form(...),
    video_url: str = Form(""),
    video_description: str = Form("")
):
    DEEPSEEK_KEY = os.getenv("THUMBNAIL_WIZARD_API_KEY")
    # Show loading page
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-chart-line"></i>
        </div>
        
        <h1 style="color: var(--primary);">Analyzing Your Video...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Checking {platform.title()} best practices for {type} videos...
        </p>
        
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            Analyzing: {video_url[:50] if video_url else "Your video description"}...
        </p>
        
        <!-- Auto-refresh to result after 3 seconds -->
        <meta http-equiv="refresh" content="3;url=/result?platform={platform}&type={type}&goal={goal}&audience={audience}&tone={tone}&video_url={video_url}&video_description={video_description}">
    </div>
    '''
    
    return HTMLResponse(layout("Analyzing...", loading_content))

# ========== RESULT ==========
@app.get("/result")
async def show_result(
    platform: str = Query(...),
    type: str = Query(...),
    goal: str = Query(...),
    audience: str = Query(...),
    tone: str = Query(...),
    video_url: str = Query(""),
    video_description: str = Query("")
):
    # For now, simulate AI analysis until we implement real YouTube API + GPT-4 Vision
    analysis_prompt = f"""You are a video STRUCTURE optimization expert for {platform}.

VIDEO CONTEXT:
- Platform: {platform}
- Video type: {type}
- Target audience: {audience}
- Desired tone: {tone}
- Goal: {goal}

USER'S BRIEF DESCRIPTION: "{video_description}"

NOTE: User provided a brief description. This analysis focuses on 
STRUCTURAL optimization for a "{type}" style video on {platform}. 
The advice applies regardless of the specific subject matter.

YOUR TASK: Provide STRUCTURAL optimization advice ONLY.
DO NOT analyze if the content is accurate or good.
DO NOT make assumptions about specific video content.

FOCUS ON:
1. **Hook suggestions** (first 5-10 seconds)
2. **Retention strategies** (prevent viewer drop-off)
3. **{platform} SEO** (titles, description, tags optimization)
4. **Engagement tactics** (CTAs, comments, community)
5. **Thumbnail & title synergy**
6. **Platform-specific features** (chapters, end screens, etc.)

CRITICAL: Format your response EXACTLY like this example:

OVERALL SCORE: 8/10 - {platform} optimization potential based on current structure

HOOK SUGGESTIONS:
1. "Hook text here" - Brief explanation why it works for this audience
2. "Hook text here" - Brief explanation why it works for this audience
3. "Hook text here" - Brief explanation why it works for this audience

RETENTION STRATEGIES:
- Strategy 1: Explanation and implementation tip
- Strategy 2: Explanation and implementation tip
- Strategy 3: Explanation and implementation tip

PLATFORM SEO:
- Title optimization: Specific title suggestions with keywords
- Description template: Template with placeholders
- Tag suggestions: Top 5-7 relevant tags
- Chapter recommendations: Specific timestamps and titles

ENGAGEMENT TACTICS:
- CTA placement: Where and how to ask for engagement
- Comment strategy: How to seed and respond to comments
- Community building: Specific steps for this video type

THUMBNAIL & TITLE SYNERGY:
- Visual elements to include: Specific items or emotions
- Text overlay: Exact text to use (short)
- Color psychology: Colors that work for this audience/tone

PLATFORM FEATURES:
- Specific features to use: Chapters, end screens, cards, etc.
- Implementation tips: How to set them up for this video
- Timing suggestions: When to trigger them

QUICK WINS (<10 minute fixes):
1. Quick fix 1
2. Quick fix 2
3. Quick fix 3

LONG-TERM STRATEGY:
- Next video planning: How to follow up
- Series potential: If applicable
- Audience growth: Specific tactics for this niche

IMPORTANT: Always start with "OVERALL SCORE: X/10" where X is a number 1-10, followed by a brief explanation."""
    
    try:
        # For now, use text-only analysis. Later: YouTube API + GPT-4 Vision
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a video optimization expert for YouTube, TikTok, Instagram, and LinkedIn. Format your responses exactly as requested."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "stream": False
            },
            timeout=45
        )
        
        if response.status_code == 200:
            ai_text = response.json()["choices"][0]["message"]["content"]
            
            # YOUR TURQUOISE COLOR: #0d96c1
            TURQUOISE = "#0d96c1"
            TURQUOISE_LIGHT = "#ecfeff"
            TURQUOISE_DARK = "#0c4a6e"
            
            # Parse AI response into sections
            sections = {}
            current_section = None
            current_content = []
            
            for line in ai_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if line starts a new section (ends with colon)
                if line.endswith(':'):
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = line.rstrip(':')
                    current_content = []
                elif current_section:
                    current_content.append(line)
            
            # Save last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Build analysis cards
            analysis_html = ""
            
            # Define section icons and order
            section_config = [
                ("HOOK SUGGESTIONS", "fa-fish-hook", "Start strong with these hooks"),
                ("RETENTION STRATEGIES", "fa-chart-line", "Keep viewers watching"),
                ("PLATFORM SEO", "fa-search", "Optimize for discovery"),
                ("ENGAGEMENT TACTICS", "fa-comments", "Build community"),
                ("THUMBNAIL & TITLE SYNERGY", "fa-eye", "Increase click-through"),
                ("PLATFORM FEATURES", "fa-cogs", "Use platform tools"),
                ("QUICK WINS", "fa-bolt", "Fast improvements"),
                ("LONG-TERM STRATEGY", "fa-chess-board", "Sustainable growth")
            ]
            
            for i, (section_title, icon, description) in enumerate(section_config):
                if section_title in sections:
                    content = sections[section_title]
                    # Format bullet points and numbered lists
                    formatted_content = content.replace('- ', '<span style="color: #0c4a6e;">•</span> ')
                    formatted_content = formatted_content.replace('1. ', '<br><span style="font-weight: bold; color: #0d96c1;">1.</span> ')
                    formatted_content = formatted_content.replace('2. ', '<br><span style="font-weight: bold; color: #0d96c1;">2.</span> ')
                    formatted_content = formatted_content.replace('3. ', '<br><span style="font-weight: bold; color: #0d96c1;">3.</span> ')
                    
                    analysis_html += f'''
<div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; border: 2px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.1);">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <div style="background: {TURQUOISE}; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
            <i class="fas {icon}"></i>
        </div>
        <div>
            <h3 style="margin: 0; color: {TURQUOISE};">{section_title.replace('_', ' ').title()}</h3>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: #64748b;">{description}</p>
        </div>
    </div>
    
    <div style="font-size: 1rem; line-height: 1.6; color: {TURQUOISE_DARK}; padding: 1rem; background: {TURQUOISE_LIGHT}; border-radius: 8px; border-left: 4px solid {TURQUOISE};">
        {formatted_content}
    </div>
</div>
'''
            
            # Add overall score if present - IMPROVED PARSING
            if "OVERALL SCORE" in ai_text:
                # Better score extraction from the text
                score_line = None
                for line in ai_text.split('\n'):
                    if "OVERALL SCORE" in line or "SCORE:" in line or "/10" in line:
                        score_line = line.strip()
                        break
                
                score = "8"  # default
                if score_line:
                    # Extract numeric score with regex
                    import re
                    score_match = re.search(r'(\d+(?:\.\d+)?)/10', score_line)
                    if score_match:
                        score = score_match.group(1)
                    else:
                        # Try to find any number before /10
                        score_match = re.search(r'(\d+(?:\.\d+)?)\s*/10', ai_text)
                        if score_match:
                            score = score_match.group(1)
                
                # Get score explanation if available
                score_explanation = ""
                if "OVERALL SCORE" in sections:
                    score_text = sections["OVERALL SCORE"]
                    # Remove the numeric score part for explanation
                    score_explanation = re.sub(r'\d+(?:\.\d+)?/10[:\s]*', '', score_text).strip()
                    if score_explanation and len(score_explanation) > 200:
                        score_explanation = score_explanation[:200] + "..."
                
                # Determine score color
                try:
                    score_num = float(score)
                    if score_num >= 8:
                        score_color = "#059669"  # emerald
                        score_icon = "fa-trophy"
                    elif score_num >= 6:
                        score_color = TURQUOISE  # your turquoise
                        score_icon = "fa-chart-line"
                    elif score_num >= 4:
                        score_color = "#d97706"  # amber
                        score_icon = "fa-exclamation-triangle"
                    else:
                        score_color = "#dc2626"  # red
                        score_icon = "fa-exclamation-circle"
                except:
                    score_color = TURQUOISE
                    score_icon = "fa-star"
                
                score_html = f'''
<div style="background: white; border-radius: 12px; padding: 2rem; margin: 2rem 0; border: 3px solid {score_color}; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15); text-align: center;">
    <div style="font-size: 0.9rem; color: {score_color}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
        <i class="fas {score_icon}"></i> Platform Optimization Score
    </div>
    <div style="font-size: 4rem; font-weight: bold; color: {score_color}; margin: 0.5rem 0; line-height: 1;">
        {score}<span style="font-size: 2rem; opacity: 0.7;">/10</span>
    </div>
    <div style="font-size: 1.1rem; color: #374151; margin-top: 0.5rem;">
        {platform.title()} • {type.title()} • {audience.title()}
    </div>
    {f'<div style="font-size: 0.95rem; color: #4b5563; margin-top: 1rem; padding: 0.75rem; background: {TURQUOISE_LIGHT}; border-radius: 6px; border-left: 3px solid {score_color};">{score_explanation}</div>' if score_explanation else ''}
    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 1.5rem;">
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-video"></i> {type.title()}</span>
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-users"></i> {audience.title()}</span>
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-bullseye"></i> {goal.title()}</span>
    </div>
</div>
'''
                # Insert at beginning
                analysis_html = score_html + analysis_html
            else:
                # If no score found, create a default score card
                score_html = f'''
<div style="background: white; border-radius: 12px; padding: 2rem; margin: 2rem 0; border: 3px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.15); text-align: center;">
    <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
        <i class="fas fa-chart-line"></i> Platform Optimization Score
    </div>
    <div style="font-size: 4rem; font-weight: bold; color: {TURQUOISE}; margin: 0.5rem 0; line-height: 1;">
        8<span style="font-size: 2rem; opacity: 0.7;">/10</span>
    </div>
    <div style="font-size: 0.95rem; color: #4b5563; margin-top: 1rem; padding: 0.75rem; background: {TURQUOISE_LIGHT}; border-radius: 6px;">
        <i class="fas fa-info-circle"></i> Based on structural analysis of your {type.lower()} video for {platform}
    </div>
    <div style="font-size: 1.1rem; color: #374151; margin-top: 1rem;">
        {platform.title()} • {type.title()} • {audience.title()}
    </div>
</div>
'''
                analysis_html = score_html + analysis_html
            
            result_content = f'''
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; color: {TURQUOISE};">
            <i class="fas fa-chart-line"></i>
        </div>
        <h1 style="color: {TURQUOISE};">Video Analysis Complete!</h1>
        <p style="color: #64748b;">Optimized for <strong>{platform.title()}</strong> • <strong>{type.title()}</strong> • <strong>{goal.title()}</strong></p>
        <div style="background: {TURQUOISE_LIGHT}; padding: 0.75rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #a5f3fc;">
            <p style="color: {TURQUOISE_DARK}; margin: 0;"><i class="fas fa-file-alt"></i> <strong>Video Description:</strong> {video_description[:100]}{'...' if len(video_description) > 100 else ''}</p>
        </div>
    </div>
    
    {analysis_html}
    
    <div style="text-align: center; margin-top: 3rem;">
        <a href="wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-video"></i> Analyze Another Video
        </a>
        <a href="/" role="button" style="background: #64748b; border-color: #64748b;">
            <i class="fas fa-home"></i> Dashboard
        </a>
    </div>
</div>
'''
        else:
            TURQUOISE = "#0d96c1"
            result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> API Error</h1>
    <p>Analysis failed. Status: {response.status_code}</p>
    <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone={tone}" 
       role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Try Again</a>
</div>
'''
    except Exception as e:
        TURQUOISE = "#0d96c1"
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> Analysis Error</h1>
    <p>{str(e)}</p>
    <p><small>Note: Full video analysis requires YouTube API access. Currently using description-only analysis.</small></p>
    <a href="/" role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Start Over</a>
</div>
'''
    
    return HTMLResponse(layout("Analysis Results", result_content))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port than Prompt Wizard

