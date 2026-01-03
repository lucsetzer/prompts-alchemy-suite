# home.py - UPDATED with your corrections
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
