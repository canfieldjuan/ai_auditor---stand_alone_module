# File: services/email_service.py
# FIXED VERSION - Enhanced email service using Resend API for premium $997 audit experience

import os
import requests
import base64
from datetime import datetime
from typing import Dict, Optional
import html

from config.settings import (
    RESEND_API_KEY, RESEND_FROM_EMAIL, PREMIUM_PRICE, 
    COMPANY_NAME, SUPPORT_EMAIL, BUSINESS_URL
)

def send_email_report(email: str, audit_data: Dict, pdf_path: str, website_url: str) -> bool:
    """Send audit report email with premium or free template using Resend"""
    
    audit_type = audit_data.get('audit_type', 'free')
    
    if audit_type == 'premium':
        return send_premium_email_report(email, audit_data, pdf_path, website_url)
    else:
        return send_free_email_report(email, audit_data, pdf_path, website_url)

def send_premium_email_report(email: str, audit_data: Dict, pdf_path: str, website_url: str) -> bool:
    """Send premium $997 audit report with enhanced content using Resend"""
    
    if not RESEND_API_KEY or not RESEND_FROM_EMAIL:
        print("❌ Resend credentials not configured")
        return False
    
    try:
        # Extract premium audit data
        executive_summary = audit_data.get('executive_summary', {})
        company = audit_data.get('company', '')
        industry = audit_data.get('industry', 'your industry')
        
        overall_score = executive_summary.get('overall_score', 70)
        monthly_loss = executive_summary.get('estimated_monthly_revenue_loss', 0)
        annual_cost = executive_summary.get('annual_opportunity_cost', 0)
        roi_timeline = executive_summary.get('expected_roi_timeline', '45-60 days')
        
        # Prepare email content
        subject = f"Your $997 Premium AI SEO Audit is Ready - {company if company else 'Business'}"
        
        # Create premium HTML email content
        html_content = create_premium_email_html(
            email, audit_data, website_url, company, industry
        )
        
        # Create text version
        text_content = create_premium_email_text(
            email, audit_data, website_url, company
        )
        
        # Prepare attachments
        attachments = []
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as attachment:
                content = base64.b64encode(attachment.read()).decode()
                
            filename = f"Premium_AI_SEO_Audit_{company.replace(' ', '_') if company else 'Report'}.pdf"
            attachments.append({
                "filename": filename,
                "content": content,
                "content_type": "application/pdf"
            })
        
        # Send via Resend API
        success = send_resend_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            attachments=attachments
        )
        
        if success:
            print(f"✅ Premium email sent successfully to {email}")
            
            # Track email campaign
            try:
                from models.database import save_email_campaign_data
                save_email_campaign_data(email, 'premium_audit_delivery', subject)
            except:
                pass
        
        return success
        
    except Exception as e:
        print(f"❌ Failed to send premium email to {email}: {e}")
        return False

def send_free_email_report(email: str, audit_data: Dict, pdf_path: str, website_url: str) -> bool:
    """Send free audit report with upsell to premium using Resend"""
    
    if not RESEND_API_KEY or not RESEND_FROM_EMAIL:
        print("❌ Resend credentials not configured")
        return False
    
    try:
        overall_score = audit_data.get('overall_score', audit_data.get('score', 70))
        
        # Prepare email content
        subject = f"Your Free SEO Audit Results (Score: {overall_score}/100) + Premium Upgrade Available"
        
        # Create HTML email with premium upsell
        html_content = create_free_email_html_with_upsell(
            email, audit_data, website_url
        )
        
        # Create text version
        text_content = create_free_email_text_with_upsell(
            email, audit_data, website_url
        )
        
        # Prepare attachments
        attachments = []
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as attachment:
                content = base64.b64encode(attachment.read()).decode()
                
            attachments.append({
                "filename": "SEO_Audit_Report.pdf",
                "content": content,
                "content_type": "application/pdf"
            })
        
        # Send via Resend API
        success = send_resend_email(
            to_email=email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            attachments=attachments
        )
        
        if success:
            print(f"✅ Free audit email sent successfully to {email}")
            
            # Track email campaign
            try:
                from models.database import save_email_campaign_data
                save_email_campaign_data(email, 'free_audit_with_upsell', subject)
            except:
                pass
        
        return success
        
    except Exception as e:
        print(f"❌ Failed to send free email to {email}: {e}")
        return False

def send_resend_email(to_email: str, subject: str, html_content: str, text_content: str, attachments: list = None) -> bool:
    """Send email using Resend API - FIXED VERSION"""
    
    url = "https://api.resend.com/emails"
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # FIXED: Simple from field - no company name formatting that breaks shit
    email_data = {
        "from": RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content,
        "text": text_content
    }
    
    # Add attachments if provided
    if attachments:
        email_data["attachments"] = attachments
    
    try:
        response = requests.post(url, headers=headers, json=email_data, timeout=30)
        
        # FIXED: Actually show errors instead of hiding them
        if response.status_code == 200:
            print(f"✅ Email sent to {to_email}")
            return True
        else:
            print(f"❌ Email FAILED: Status {response.status_code}")
            print(f"❌ Error details: {response.text}")
            print(f"❌ API Key: {RESEND_API_KEY[:10]}..." if RESEND_API_KEY else "❌ NO API KEY")
            print(f"❌ From Email: {RESEND_FROM_EMAIL}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Resend request failed: {e}")
        return False

def create_premium_email_html(email: str, audit_data: Dict, website_url: str, company: str, industry: str) -> str:
    """Create premium HTML email template"""
    
    executive_summary = audit_data.get('executive_summary', {})
    overall_score = executive_summary.get('overall_score', 70)
    monthly_loss = executive_summary.get('estimated_monthly_revenue_loss', 0)
    annual_cost = executive_summary.get('annual_opportunity_cost', 0)
    roi_timeline = executive_summary.get('expected_roi_timeline', '45-60 days')
    business_impact = executive_summary.get('business_impact_rating', 'High')
    
    # Get critical issues
    critical_issues = audit_data.get('critical_issues', [])
    top_issues = []
    for issue in critical_issues[:5]:
        if isinstance(issue, dict):
            top_issues.append(issue.get('issue', str(issue)))
        else:
            top_issues.append(str(issue))
    
    # Get implementation roadmap
    roadmap = audit_data.get('implementation_roadmap', {})
    phase1 = roadmap.get('weeks_1_2', {})
    
    user_name = email.split('@')[0].replace('.', ' ').title()
    company_display = company if company else 'your business'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Premium AI SEO Audit Results</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .score-box {{ background: #f7fafc; border: 3px solid #{'#059669' if overall_score >= 70 else '#f59e0b' if overall_score >= 50 else '#dc2626'}; border-radius: 15px; padding: 30px; text-align: center; margin: 30px 0; }}
            .score {{ font-size: 3rem; font-weight: bold; color: #{'#059669' if overall_score >= 70 else '#f59e0b' if overall_score >= 50 else '#dc2626'}; }}
            .impact-box {{ background: #fff3cd; border-left: 5px solid #f59e0b; padding: 20px; margin: 30px 0; }}
            .issues-box {{ background: #fee2e2; border-left: 5px solid #dc2626; padding: 20px; margin: 30px 0; }}
            .roadmap-box {{ background: #ecfdf5; border-left: 5px solid #059669; padding: 20px; margin: 30px 0; }}
            .cta-button {{ background: #dc2626; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; font-weight: bold; }}
            .footer {{ background: #f7fafc; padding: 30px; text-align: center; color: #666; font-size: 0.9rem; }}
            ul {{ padding-left: 20px; }}
            li {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Your Premium AI SEO Audit is Ready!</h1>
            <p>Investment: $997 • Website: {html.escape(website_url)} • Delivered within 24 hours as promised</p>
        </div>
        
        <div class="content">
            <h2>Hi {html.escape(user_name)},</h2>
            
            <p>Your comprehensive AI SEO audit for <strong>{html.escape(company_display)}</strong> has been completed. Here's what our enterprise-grade analysis revealed:</p>
            
            <div class="score-box">
                <div class="score">{overall_score}/100</div>
                <h3>AI Search Readiness Score</h3>
                <p><strong>Business Impact Level:</strong> {html.escape(business_impact)}</p>
            </div>
            
            <div class="impact-box">
                <h3>💰 Revenue Impact Analysis</h3>
                <ul>
                    <li><strong>Estimated Monthly Revenue Loss:</strong> ${monthly_loss:,}</li>
                    <li><strong>Annual Opportunity Cost:</strong> ${annual_cost:,}</li>
                    <li><strong>Expected ROI Timeline:</strong> {html.escape(roi_timeline)}</li>
                    <li><strong>Break-Even on $997 Investment:</strong> 30-45 days</li>
                </ul>
            </div>
            
            <div class="issues-box">
                <h3>🚨 Top 5 Critical Issues Found</h3>
                <ul>
                    {''.join(f'<li>{html.escape(issue)}</li>' for issue in top_issues)}
                </ul>
                <p><strong>Note:</strong> These issues are detailed in your 25+ page PDF report with specific implementation guidance.</p>
            </div>
            
            <div class="roadmap-box">
                <h3>🗺️ Your 90-Day Implementation Roadmap</h3>
                <p><strong>Phase 1 (Weeks 1-2) - Critical Fixes:</strong></p>
                <ul>
                    {''.join(f'<li>{html.escape(fix)}</li>' for fix in phase1.get('critical_fixes', ['Complete technical audit implementation', 'Optimize for AI search visibility']))}
                </ul>
                <p><strong>Expected Impact:</strong> {html.escape(phase1.get('expected_impact', '25% improvement in search visibility'))}</p>
                <p><strong>Resource Requirements:</strong> {html.escape(phase1.get('resource_requirements', '20-30 hours of development time'))}</p>
            </div>
            
            <h3>📊 What's Included in Your Premium Report:</h3>
            <ul>
                <li>25+ page comprehensive analysis</li>
                <li>Competitor intelligence report</li>
                <li>AI search optimization strategy</li>
                <li>Revenue impact projections</li>
                <li>Week-by-week implementation timeline</li>
                <li>Resource requirements and cost estimates</li>
                <li>Success tracking metrics and KPIs</li>
            </ul>
            
            <div style="background: #f0fff4; border: 2px solid #059669; padding: 20px; border-radius: 10px; margin: 30px 0;">
                <h3 style="color: #059669;">🎯 Your Investment Summary</h3>
                <p><strong>Audit Investment:</strong> $997</p>
                <p><strong>Projected 12-Month Return:</strong> ${min(annual_cost, 150000):,}</p>
                <p><strong>Expected ROI:</strong> 10-15x your investment</p>
                <p><strong>Money-Back Guarantee:</strong> 30 days (if you don't see 10x ROI potential)</p>
            </div>
            
            <h3>🚀 Next Steps:</h3>
            <ol>
                <li><strong>Review your attached 25+ page report</strong> (everything is detailed there)</li>
                <li><strong>Start with Phase 1 critical fixes</strong> within the next 7 days</li>
                <li><strong>Track your progress</strong> using the metrics we've provided</li>
                <li><strong>Contact us</strong> if you have any questions about implementation</li>
            </ol>
            
            <p><strong>Questions about your audit?</strong> Reply to this email or contact us at <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
            
            <div style="text-align: center; margin: 40px 0;">
                <p><strong>Ready to implement and see results?</strong></p>
                <a href="{BUSINESS_URL}/contact" class="cta-button">Contact Us About Implementation</a>
            </div>
            
            <p>Thank you for investing in your business's AI search future. The companies that optimize for AI search now will dominate their markets for the next decade.</p>
            
            <p>Best regards,<br>
            The AI SEO Team<br>
            {COMPANY_NAME}</p>
        </div>
        
        <div class="footer">
            <p>This audit was generated specifically for {html.escape(website_url)} and delivered within 24 hours as promised.</p>
            <p>If you're not completely satisfied with your audit, we offer a 30-day money-back guarantee.</p>
            <p><a href="{BUSINESS_URL}/privacy">Privacy Policy</a> • <a href="{BUSINESS_URL}/refund">Refund Policy</a> • <a href="mailto:{SUPPORT_EMAIL}">Support</a></p>
        </div>
    </body>
    </html>
    """

def create_free_email_html_with_upsell(email: str, audit_data: Dict, website_url: str) -> str:
    """Create free audit email with premium upsell"""
    
    overall_score = audit_data.get('overall_score', audit_data.get('score', 70))
    issues = audit_data.get('issues', [])
    recommendations = audit_data.get('recommendations', [])
    
    user_name = email.split('@')[0].replace('.', ' ').title()
    
    # Calculate estimated opportunity
    estimated_loss = max(1000, (100 - overall_score) * 30)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Free SEO Audit Results</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .score-box {{ background: #f7fafc; border: 3px solid #{'#059669' if overall_score >= 70 else '#f59e0b' if overall_score >= 50 else '#dc2626'}; border-radius: 15px; padding: 30px; text-align: center; margin: 30px 0; }}
            .score {{ font-size: 3rem; font-weight: bold; color: #{'#059669' if overall_score >= 70 else '#f59e0b' if overall_score >= 50 else '#dc2626'}; }}
            .upgrade-box {{ background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); color: white; padding: 30px; border-radius: 15px; margin: 30px 0; text-align: center; }}
            .cta-button {{ background: #fbbf24; color: #1a365d; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; font-weight: bold; font-size: 1.1rem; }}
            .comparison-box {{ background: #f7fafc; border: 2px solid #e2e8f0; padding: 20px; margin: 20px 0; border-radius: 10px; }}
            .footer {{ background: #f7fafc; padding: 30px; text-align: center; color: #666; font-size: 0.9rem; }}
            ul {{ padding-left: 20px; }}
            li {{ margin: 8px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Your Free SEO Audit Results</h1>
            <p>Website: {html.escape(website_url)} • Score: {overall_score}/100</p>
        </div>
        
        <div class="content">
            <h2>Hi {html.escape(user_name)},</h2>
            
            <p>Thank you for using our free SEO audit tool. Here's what we found:</p>
            
            <div class="score-box">
                <div class="score">{overall_score}/100</div>
                <h3>SEO Score</h3>
                <p>Based on our analysis of {len(issues)} issues found</p>
            </div>
            
            <h3>🚨 Top Issues Found:</h3>
            <ul>
                {''.join(f'<li>{html.escape(str(issue))}</li>' for issue in issues[:5])}
            </ul>
            
            <h3>💡 Basic Recommendations:</h3>
            <ul>
                {''.join(f'<li>{html.escape(str(rec))}</li>' for rec in recommendations[:3])}
            </ul>
            
            <div class="upgrade-box">
                <h2>🚀 Want the Complete $10,000 Analysis for $997?</h2>
                <p>This free audit only scratches the surface. Here's what you're missing:</p>
                
                <div class="comparison-box" style="color: #333; margin: 20px 0;">
                    <h4>Free Audit vs Premium Audit:</h4>
                    <table style="width: 100%; color: #333;">
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;"><strong>Feature</strong></td>
                            <td style="padding: 10px; text-align: center;"><strong>Free</strong></td>
                            <td style="padding: 10px; text-align: center;"><strong>Premium</strong></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;">Report Pages</td>
                            <td style="padding: 10px; text-align: center;">5 pages</td>
                            <td style="padding: 10px; text-align: center;">25+ pages</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;">Competitor Analysis</td>
                            <td style="padding: 10px; text-align: center;">❌</td>
                            <td style="padding: 10px; text-align: center;">✅ Top 5 competitors</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;">AI Search Strategy</td>
                            <td style="padding: 10px; text-align: center;">❌</td>
                            <td style="padding: 10px; text-align: center;">✅ Complete roadmap</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;">Revenue Impact Analysis</td>
                            <td style="padding: 10px; text-align: center;">❌</td>
                            <td style="padding: 10px; text-align: center;">✅ Detailed projections</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ddd;">
                            <td style="padding: 10px;">Implementation Timeline</td>
                            <td style="padding: 10px; text-align: center;">❌</td>
                            <td style="padding: 10px; text-align: center;">✅ 90-day roadmap</td>
                        </tr>
                    </table>
                </div>
                
                <p><strong>Based on your score, you're potentially losing ${estimated_loss:,}/month in revenue.</strong></p>
                
                <a href="{BUSINESS_URL}#purchase" class="cta-button">UPGRADE TO PREMIUM AUDIT - $997</a>
                
                <p style="font-size: 0.9rem; margin-top: 20px;">✅ 30-day money-back guarantee • ✅ 10x ROI or full refund • ✅ Delivered in 24 hours</p>
            </div>
            
            <h3>🎯 Why Upgrade Now?</h3>
            <ul>
                <li><strong>AI Search is the Future:</strong> Your competitors are optimizing for ChatGPT and Google AI while you're stuck with 2019 tactics</li>
                <li><strong>Revenue Impact:</strong> Our premium customers see average 12x ROI within 90 days</li>
                <li><strong>Limited Availability:</strong> We only do 20 premium audits per month to ensure quality</li>
                <li><strong>Complete Strategy:</strong> Get the exact roadmap Fortune 500 companies pay $10,000+ for</li>
            </ul>
            
            <div style="background: #fff3cd; border-left: 5px solid #f59e0b; padding: 20px; margin: 30px 0;">
                <h4>⚠️ What Happens If You Wait?</h4>
                <p>Every month you delay AI search optimization, competitors capture more of your market share. The businesses implementing AI SEO now will dominate for the next decade.</p>
            </div>
            
            <div style="text-align: center; margin: 40px 0;">
                <a href="{BUSINESS_URL}#purchase" class="cta-button">GET PREMIUM AUDIT - $997</a>
            </div>
            
            <p>Questions about upgrading? Reply to this email or contact us at <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
            
            <p>Best regards,<br>
            The AI SEO Team<br>
            {COMPANY_NAME}</p>
        </div>
        
        <div class="footer">
            <p>This free audit analyzed basic SEO factors. Our premium audit analyzes 500+ AI search ranking factors.</p>
            <p><a href="{BUSINESS_URL}/privacy">Privacy Policy</a> • <a href="{BUSINESS_URL}/terms">Terms</a> • <a href="mailto:{SUPPORT_EMAIL}">Support</a></p>
        </div>
    </body>
    </html>
    """

def create_premium_email_text(email: str, audit_data: Dict, website_url: str, company: str) -> str:
    """Create premium email text version"""
    
    executive_summary = audit_data.get('executive_summary', {})
    overall_score = executive_summary.get('overall_score', 70)
    monthly_loss = executive_summary.get('estimated_monthly_revenue_loss', 0)
    annual_cost = executive_summary.get('annual_opportunity_cost', 0)
    
    user_name = email.split('@')[0].replace('.', ' ').title()
    company_display = company if company else 'your business'
    
    return f"""
Your Premium AI SEO Audit is Ready!

Hi {user_name},

Your comprehensive $997 AI SEO audit for {company_display} has been completed.

AUDIT RESULTS:
- AI Search Readiness Score: {overall_score}/100
- Estimated Monthly Revenue Loss: ${monthly_loss:,}
- Annual Opportunity Cost: ${annual_cost:,}
- Expected ROI Timeline: {executive_summary.get('expected_roi_timeline', '45-60 days')}

Your detailed 25+ page report is attached to this email and includes:
• Complete competitive intelligence analysis
• AI search optimization strategy
• 90-day implementation roadmap
• Revenue impact projections
• Resource requirements and timelines

NEXT STEPS:
1. Review your comprehensive report (attached)
2. Begin Phase 1 implementation within 7 days
3. Track progress using provided metrics
4. Contact us with any implementation questions

Investment Summary:
- Audit Investment: $997
- Expected 12-Month Return: ${min(annual_cost, 150000):,}
- ROI Multiple: 10-15x
- Money-Back Guarantee: 30 days

Questions? Reply to this email or contact {SUPPORT_EMAIL}

Thank you for investing in your business's AI search future.

Best regards,
The AI SEO Team
{COMPANY_NAME}

---
This audit was generated specifically for {website_url} and delivered within 24 hours as promised.
30-day money-back guarantee if you don't see 10x ROI potential.
    """

def create_free_email_text_with_upsell(email: str, audit_data: Dict, website_url: str) -> str:
    """Create free email text version with upsell"""
    
    overall_score = audit_data.get('overall_score', audit_data.get('score', 70))
    user_name = email.split('@')[0].replace('.', ' ').title()
    estimated_loss = max(1000, (100 - overall_score) * 30)
    
    return f"""
Your Free SEO Audit Results (Score: {overall_score}/100)

Hi {user_name},

Thank you for using our free SEO audit tool for {website_url}.

YOUR RESULTS:
- SEO Score: {overall_score}/100
- Issues Found: {len(audit_data.get('issues', []))}
- Basic recommendations included in attached report

UPGRADE TO PREMIUM AUDIT - $997
This free audit only covers basic SEO factors. Our premium audit reveals:

✓ Complete AI search optimization strategy
✓ Competitor intelligence (top 5 competitors analyzed)
✓ Revenue impact analysis (you're potentially losing ${estimated_loss:,}/month)
✓ 90-day implementation roadmap
✓ 25+ page comprehensive report
✓ 24-hour delivery
✓ 30-day money-back guarantee

Why upgrade now?
- AI search is the future of SEO
- Competitors are optimizing while you wait
- Average 12x ROI for our premium customers
- Only 20 premium audits available per month

Get Premium Audit: {BUSINESS_URL}#purchase

Questions? Email {SUPPORT_EMAIL}

Best regards,
The AI SEO Team
{COMPANY_NAME}
    """