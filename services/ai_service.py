# File: services/ai_service.py
# Enhanced AI service for $997 premium audit

import openai
import requests
import json
from typing import Dict, List
from config.settings import OPENAI_API_KEY, OPENROUTER_API_KEY, OPENROUTER_BASE_URL

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def analyze_with_ai(website_data: Dict) -> Dict:
    """Enhanced AI analysis worth $997 - comprehensive business-grade audit"""
    
    # Enhanced prompt for premium $997 audit
    premium_prompt = f"""
    You are conducting a $997 enterprise-level AI SEO audit that must deliver exceptional business value. 
    This audit should provide actionable insights worth 10x the investment cost.

    WEBSITE ANALYSIS DATA:
    URL: {website_data.get('url', 'N/A')}
    Title: {website_data.get('title', 'N/A')}
    Meta Description: {website_data.get('meta_description', 'N/A')}
    H1 Tags: {website_data.get('h1_tags', [])}
    Content Length: {website_data.get('content_length', 0)} characters
    Schema Markup: {website_data.get('has_schema', False)}
    Schema Types: {website_data.get('schema_types', [])}
    Images without Alt: {website_data.get('images_without_alt', 0)}/{website_data.get('images', 0)}
    SSL Certificate: {website_data.get('ssl_certificate', False)}
    Internal Links: {website_data.get('internal_links', 0)}
    External Links: {website_data.get('external_links', 0)}
    
    Content Sample: {website_data.get('content_text', '')[:3000]}

    CONDUCT A COMPREHENSIVE $997-VALUE ANALYSIS INCLUDING:

    1. BUSINESS IMPACT ASSESSMENT
    - Estimate current monthly organic traffic loss
    - Calculate revenue impact at $50 per visitor
    - Project 12-month opportunity cost
    - Benchmark against industry standards

    2. COMPETITOR INTELLIGENCE 
    - Identify likely top 5 competitors based on content/industry
    - Analyze competitive advantages they may have
    - Find content gaps and opportunities
    - Estimate their traffic and market share

    3. AI SEARCH DOMINATION STRATEGY
    - Google AI Overview optimization recommendations
    - ChatGPT/Perplexity visibility strategy
    - Voice search optimization roadmap
    - Schema markup enhancement plan

    4. TECHNICAL SEO PRIORITY MATRIX
    - Critical issues (fix in weeks 1-2)
    - High-impact improvements (weeks 3-6) 
    - Long-term optimizations (weeks 7-12)
    - Resource requirements for each

    5. CONTENT STRATEGY BLUEPRINT
    - AI-optimized content recommendations
    - Topic clusters for authority building
    - Question-based content for voice search
    - Semantic keyword opportunities

    6. 90-DAY IMPLEMENTATION ROADMAP
    - Week-by-week action items
    - Priority ranking with business impact scores
    - Resource allocation recommendations
    - Success metrics and KPIs to track

    Provide analysis in this JSON format:
    {{
        "executive_summary": {{
            "overall_score": 0-100,
            "business_impact_rating": "Critical/High/Medium/Low",
            "estimated_monthly_traffic_loss": 0,
            "estimated_monthly_revenue_loss": 0,
            "implementation_complexity": "Low/Medium/High",
            "expected_roi_timeline": "30/60/90 days"
        }},
        "category_scores": {{
            "technical_seo": 0-100,
            "content_quality": 0-100,
            "ai_readiness": 0-100,
            "voice_search": 0-100,
            "schema_markup": 0-100,
            "competitive_position": 0-100
        }},
        "competitor_analysis": {{
            "likely_competitors": [
                {{
                    "domain": "competitor1.com",
                    "competitive_advantage": "explanation",
                    "content_gaps": ["gap1", "gap2"],
                    "estimated_traffic": "high/medium/low"
                }}
            ],
            "market_opportunity": "detailed analysis",
            "competitive_recommendations": ["action1", "action2"]
        }},
        "critical_issues": [
            {{
                "issue": "specific problem",
                "business_impact": "high/medium/low", 
                "implementation_effort": "1-4 weeks",
                "expected_improvement": "specific outcome",
                "priority_score": 1-10
            }}
        ],
        "ai_search_strategy": {{
            "google_ai_optimization": [
                "specific recommendation with implementation steps"
            ],
            "chatgpt_visibility": [
                "strategies to appear in AI responses"
            ],
            "voice_search_plan": [
                "voice search optimization tactics"
            ],
            "schema_roadmap": [
                "schema markup implementation plan"
            ]
        }},
        "content_blueprint": {{
            "priority_topics": [
                {{
                    "topic": "content topic",
                    "search_volume": "estimated volume",
                    "difficulty": "low/medium/high",
                    "business_value": "revenue potential",
                    "ai_opportunity": "AI search potential"
                }}
            ],
            "content_gaps": ["missing content areas"],
            "semantic_opportunities": ["related keyword clusters"]
        }},
        "implementation_roadmap": {{
            "weeks_1_2": {{
                "critical_fixes": ["immediate actions"],
                "expected_impact": "projected improvements",
                "resource_requirements": "time/people needed"
            }},
            "weeks_3_6": {{
                "high_impact_improvements": ["medium-term actions"],
                "expected_impact": "projected improvements", 
                "resource_requirements": "time/people needed"
            }},
            "weeks_7_12": {{
                "long_term_optimizations": ["strategic actions"],
                "expected_impact": "projected improvements",
                "resource_requirements": "time/people needed"
            }}
        }},
        "roi_projections": {{
            "30_day_impact": {{
                "traffic_increase": "percentage",
                "revenue_increase": "dollar amount",
                "key_improvements": ["specific gains"]
            }},
            "90_day_impact": {{
                "traffic_increase": "percentage", 
                "revenue_increase": "dollar amount",
                "market_position": "competitive improvement"
            }},
            "12_month_potential": {{
                "traffic_increase": "percentage",
                "revenue_increase": "dollar amount", 
                "roi_multiple": "10x, 20x, etc"
            }}
        }},
        "success_metrics": {{
            "kpis_to_track": ["specific metrics"],
            "measurement_tools": ["recommended tools"],
            "reporting_frequency": "weekly/monthly",
            "success_benchmarks": ["target numbers"]
        }},
        "next_steps": {{
            "immediate_actions": ["first 3 things to do"],
            "resource_procurement": ["tools/people needed"],
            "timeline_milestones": ["key dates and goals"],
            "risk_mitigation": ["potential challenges and solutions"]
        }}
    }}

    Make this analysis comprehensive enough to justify $997 investment with clear ROI potential.
    """
    
    # Try OpenAI first
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an elite SEO consultant who charges $2500 for comprehensive audits. Your analysis must be thorough, actionable, and business-focused. Every recommendation should have clear ROI potential."
                },
                {"role": "user", "content": premium_prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        ai_analysis = json.loads(response.choices[0].message.content)
        
        # Enhance with additional calculated metrics
        ai_analysis = enhance_analysis_with_metrics(ai_analysis, website_data)
        
        return ai_analysis
        
    except Exception as openai_error:
        print(f"OpenAI failed: {openai_error}, trying OpenRouter...")
        
        # Fallback to OpenRouter
        try:
            return analyze_with_openrouter(premium_prompt)
        except Exception as openrouter_error:
            print(f"OpenRouter also failed: {openrouter_error}")
            # Return enhanced fallback analysis for $997 value
            return generate_premium_fallback_analysis(website_data)

def analyze_with_openrouter(prompt: str) -> Dict:
    """Use OpenRouter as fallback AI service with enhanced prompt"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-4",
        "messages": [
            {
                "role": "system", 
                "content": "You are an elite SEO consultant who charges $2500 for comprehensive audits. Your analysis must be thorough, actionable, and business-focused."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        timeout=90
    )
    
    response.raise_for_status()
    result = response.json()
    
    ai_analysis = json.loads(result['choices'][0]['message']['content'])
    return ai_analysis

def enhance_analysis_with_metrics(analysis: Dict, website_data: Dict) -> Dict:
    """Add calculated business metrics to justify $997 price"""
    
    # Calculate more realistic business metrics
    content_length = website_data.get('content_length', 0)
    images_total = website_data.get('images', 0)
    images_without_alt = website_data.get('images_without_alt', 0)
    has_schema = website_data.get('has_schema', False)
    
    # Enhanced scoring algorithm for business impact
    if content_length < 500:
        traffic_loss_factor = 0.8
    elif content_length < 1500:
        traffic_loss_factor = 0.6
    else:
        traffic_loss_factor = 0.3
        
    alt_text_factor = (images_without_alt / max(images_total, 1)) * 0.4
    schema_factor = 0.3 if not has_schema else 0.1
    
    # More realistic traffic loss estimates
    base_monthly_visitors = 2500  # Conservative estimate for small business
    estimated_loss_percentage = min(0.7, traffic_loss_factor + alt_text_factor + schema_factor)
    
    analysis['executive_summary']['estimated_monthly_traffic_loss'] = int(base_monthly_visitors * estimated_loss_percentage)
    analysis['executive_summary']['estimated_monthly_revenue_loss'] = int(analysis['executive_summary']['estimated_monthly_traffic_loss'] * 50)
    
    # Add 12-month opportunity cost
    annual_opportunity = analysis['executive_summary']['estimated_monthly_revenue_loss'] * 12
    analysis['executive_summary']['annual_opportunity_cost'] = annual_opportunity
    
    # Enhanced ROI projections based on issues found
    critical_issues_count = len(analysis.get('critical_issues', []))
    if critical_issues_count >= 5:
        roi_multiplier = 15
    elif critical_issues_count >= 3:
        roi_multiplier = 10
    else:
        roi_multiplier = 7
        
    analysis['roi_projections']['investment_roi'] = f"{roi_multiplier}x return on $997 investment"
    analysis['roi_projections']['break_even_timeline'] = "30-45 days"
    
    return analysis

def generate_premium_fallback_analysis(website_data: Dict) -> Dict:
    """Generate comprehensive fallback analysis if both AI services fail"""
    
    issues = []
    recommendations = []
    score = 60  # Conservative baseline
    
    # Enhanced issue detection for $997 value
    content_length = website_data.get('content_length', 0)
    if content_length < 1000:
        issues.append({
            "issue": "Insufficient content depth for AI search visibility",
            "business_impact": "high",
            "implementation_effort": "2-3 weeks", 
            "expected_improvement": "40% increase in AI search mentions",
            "priority_score": 9
        })
        recommendations.append("Create comprehensive, AI-optimized content covering user questions in depth")
        score -= 15
    
    if not website_data.get('title'):
        issues.append({
            "issue": "Missing or inadequate title tag optimization",
            "business_impact": "high",
            "implementation_effort": "1 week",
            "expected_improvement": "25% improvement in click-through rates", 
            "priority_score": 10
        })
        score -= 10
    
    if not website_data.get('meta_description'):
        issues.append({
            "issue": "Missing meta descriptions reducing AI extraction potential",
            "business_impact": "medium",
            "implementation_effort": "1 week",
            "expected_improvement": "15% improvement in search visibility",
            "priority_score": 8
        })
        score -= 8
    
    if not website_data.get('has_schema'):
        issues.append({
            "issue": "Complete absence of structured data markup",
            "business_impact": "critical", 
            "implementation_effort": "3-4 weeks",
            "expected_improvement": "60% improvement in AI search understanding",
            "priority_score": 10
        })
        recommendations.append("Implement comprehensive schema markup for all content types")
        score -= 20
    
    images_without_alt = website_data.get('images_without_alt', 0)
    if images_without_alt > 0:
        issues.append({
            "issue": f"{images_without_alt} images lacking accessibility and SEO optimization",
            "business_impact": "medium",
            "implementation_effort": "1-2 weeks",
            "expected_improvement": "10% improvement in page comprehension by AI",
            "priority_score": 6
        })
        score -= 5
    
    # Calculate business impact
    estimated_traffic_loss = max(1000, 3000 - (score * 30))
    estimated_revenue_loss = estimated_traffic_loss * 50
    
    return {
        "executive_summary": {
            "overall_score": max(20, score),
            "business_impact_rating": "High" if score < 50 else "Medium",
            "estimated_monthly_traffic_loss": estimated_traffic_loss,
            "estimated_monthly_revenue_loss": estimated_revenue_loss,
            "annual_opportunity_cost": estimated_revenue_loss * 12,
            "implementation_complexity": "Medium",
            "expected_roi_timeline": "45-60 days"
        },
        "category_scores": {
            "technical_seo": max(30, score - 10),
            "content_quality": max(25, score - 15),
            "ai_readiness": max(20, score - 25),
            "voice_search": max(25, score - 20),
            "schema_markup": 20 if website_data.get('has_schema') else 0,
            "competitive_position": max(30, score - 5)
        },
        "competitor_analysis": {
            "likely_competitors": [
                {
                    "domain": "industry-leader.com",
                    "competitive_advantage": "Strong AI search optimization and comprehensive content strategy",
                    "content_gaps": ["In-depth guides", "FAQ sections", "Local optimization"],
                    "estimated_traffic": "high"
                }
            ],
            "market_opportunity": "Significant opportunity to capture market share through AI search optimization",
            "competitive_recommendations": [
                "Implement structured data to match competitor capabilities",
                "Create comprehensive content to fill identified gaps",
                "Optimize for voice search queries competitors are missing"
            ]
        },
        "critical_issues": issues,
        "ai_search_strategy": {
            "google_ai_optimization": [
                "Implement FAQ schema for Google AI Overview inclusion",
                "Create question-and-answer content format",
                "Optimize for featured snippet opportunities"
            ],
            "chatgpt_visibility": [
                "Create authoritative, cite-worthy content",
                "Implement proper attribution markup",
                "Build topic authority through comprehensive coverage"
            ],
            "voice_search_plan": [
                "Optimize for conversational, long-tail keywords",
                "Create content that answers specific user questions",
                "Implement local SEO for voice search queries"
            ],
            "schema_roadmap": [
                "Phase 1: Basic Organization and Website schema",
                "Phase 2: Product/Service specific schema",
                "Phase 3: Advanced FAQ and How-To schema"
            ]
        },
        "content_blueprint": {
            "priority_topics": [
                {
                    "topic": "Industry-specific how-to guides",
                    "search_volume": "high",
                    "difficulty": "medium",
                    "business_value": "high revenue potential",
                    "ai_opportunity": "Strong potential for AI search inclusion"
                }
            ],
            "content_gaps": [
                "Comprehensive FAQ sections",
                "Step-by-step tutorials", 
                "Industry comparison guides"
            ],
            "semantic_opportunities": [
                "Long-tail question-based keywords",
                "Related topic clusters",
                "Local search optimization"
            ]
        },
        "implementation_roadmap": {
            "weeks_1_2": {
                "critical_fixes": [
                    "Implement basic schema markup",
                    "Optimize title tags and meta descriptions",
                    "Add alt text to all images"
                ],
                "expected_impact": "25% improvement in search visibility",
                "resource_requirements": "20-30 hours of development time"
            },
            "weeks_3_6": {
                "high_impact_improvements": [
                    "Create comprehensive FAQ content",
                    "Implement advanced schema types",
                    "Optimize for voice search queries"
                ],
                "expected_impact": "40% improvement in AI search presence",
                "resource_requirements": "40-50 hours of content and technical work"
            },
            "weeks_7_12": {
                "long_term_optimizations": [
                    "Build topic authority through content clusters",
                    "Implement local SEO optimization",
                    "Create industry comparison content"
                ],
                "expected_impact": "60% overall improvement in search performance",
                "resource_requirements": "60-80 hours of strategic content development"
            }
        },
        "roi_projections": {
            "30_day_impact": {
                "traffic_increase": "20-30%",
                "revenue_increase": f"${estimated_revenue_loss * 0.3:,.0f}",
                "key_improvements": ["Better AI search visibility", "Improved click-through rates"]
            },
            "90_day_impact": {
                "traffic_increase": "50-70%", 
                "revenue_increase": f"${estimated_revenue_loss * 0.7:,.0f}",
                "market_position": "Strong competitive positioning in AI search"
            },
            "12_month_potential": {
                "traffic_increase": "100-150%",
                "revenue_increase": f"${estimated_revenue_loss * 1.5 * 12:,.0f}",
                "roi_multiple": "12x return on $997 investment"
            },
            "investment_roi": "10-15x return on $997 investment",
            "break_even_timeline": "30-45 days"
        },
        "success_metrics": {
            "kpis_to_track": [
                "Organic traffic growth",
                "AI search mentions", 
                "Voice search rankings",
                "Featured snippet captures",
                "Conversion rate improvements"
            ],
            "measurement_tools": ["Google Analytics", "Search Console", "AI search monitoring tools"],
            "reporting_frequency": "weekly for first month, then monthly",
            "success_benchmarks": ["20% traffic increase in 30 days", "5 new featured snippets", "50% improvement in AI search visibility"]
        },
        "next_steps": {
            "immediate_actions": [
                "Audit current schema markup implementation",
                "Identify top 10 questions customers ask",
                "Compile list of all images needing alt text"
            ],
            "resource_procurement": [
                "Technical SEO specialist (part-time)",
                "Content writer familiar with AI optimization",
                "Schema markup validation tools"
            ],
            "timeline_milestones": [
                "Week 2: All critical technical fixes completed",
                "Week 6: New content strategy launched", 
                "Week 12: Full AI search optimization implemented"
            ],
            "risk_mitigation": [
                "Start with low-risk technical improvements",
                "Test changes in staging environment",
                "Monitor rankings daily during implementation"
            ]
        }
    }