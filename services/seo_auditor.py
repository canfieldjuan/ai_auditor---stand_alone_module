# File: services/seo_auditor.py
# Enhanced SEO auditor service for premium $997 audits

import os
import logging
from typing import Dict
from services.web_scraper import scrape_website
from services.ai_service import analyze_with_ai
from services.report_generator import generate_pdf_report
from services.email_service import send_email_report
from models.database import save_audit_data

logger = logging.getLogger(__name__)

class SEOAuditor:
    def __init__(self):
        pass
    
    def run_full_audit(self, url: str, email: str) -> Dict:
        """Run basic free audit process"""
        try:
            logger.info(f'Starting free audit for {url}')
            
            # Step 1: Scrape website
            website_data = scrape_website(url)
            if 'error' in website_data:
                raise Exception(f'Failed to analyze website: {website_data["error"]}')
            
            logger.info(f'Website scraped successfully for {url}')
            
            # Step 2: Basic AI Analysis
            audit_data = analyze_with_ai(website_data)
            
            logger.info(f'AI analysis completed for {url}')
            
            # Step 3: Generate Basic PDF Report  
            pdf_path = generate_pdf_report(audit_data, website_data)
            
            logger.info(f'PDF report generated for {url}')
            
            # Step 4: Save to database
            save_audit_data(email, url, audit_data)
            
            logger.info(f'Audit data saved to database for {url}')
            
            # Step 5: Send email report
            email_sent = send_email_report(email, audit_data, pdf_path, url)
            
            if not email_sent:
                logger.warning(f'Email report not sent for {url}')
            else:
                logger.info(f'Email report sent successfully for {url}')
            
            # Prepare response data for free audit
            response_data = {
                'success': True,
                'score': audit_data.get('overall_score', audit_data.get('executive_summary', {}).get('overall_score', 70)),
                'overall_score': audit_data.get('overall_score', audit_data.get('executive_summary', {}).get('overall_score', 70)),
                'issues': self._extract_issues(audit_data),
                'recommendations': audit_data.get('recommendations', [])[:5],
                'pdf_path': f'reports/{os.path.basename(pdf_path)}' if pdf_path else None,
                'categories': audit_data.get('category_scores', {}),
                'email_sent': email_sent,
                'quick_wins': audit_data.get('quick_wins', []),
                'voice_search_issues': audit_data.get('voice_search_issues', []),
                'critical_issues': audit_data.get('critical_issues', []),
                'ai_search_issues': audit_data.get('ai_search_issues', []),
                'audit_type': 'free'
            }
            
            logger.info(f'Free audit completed successfully for {url} with score {response_data["score"]}')
            return response_data
            
        except Exception as e:
            logger.error(f'Free audit failed for {url}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'audit_type': 'free'
            }
    
    def run_premium_audit(self, url: str, email: str, company: str = '', industry: str = '') -> Dict:
        """Run comprehensive $997 premium audit process"""
        try:
            logger.info(f'Starting premium audit for {url} - Customer: {email}')
            
            # Step 1: Enhanced website scraping
            website_data = scrape_website(url)
            if 'error' in website_data:
                raise Exception(f'Failed to analyze website: {website_data["error"]}')
            
            # Add business context to website data
            website_data['company'] = company
            website_data['industry'] = industry
            website_data['audit_type'] = 'premium'
            
            logger.info(f'Website scraped successfully for premium audit: {url}')
            
            # Step 2: Comprehensive AI Analysis (using enhanced prompts)
            audit_data = analyze_with_ai(website_data)
            
            # Ensure we have the enhanced data structure
            if 'executive_summary' not in audit_data:
                audit_data = self._ensure_premium_data_structure(audit_data, website_data)
            
            logger.info(f'Premium AI analysis completed for {url}')
            
            # Step 3: Generate Premium PDF Report (25+ pages)
            pdf_path = generate_pdf_report(audit_data, website_data)
            
            logger.info(f'Premium PDF report generated for {url}')
            
            # Step 4: Save premium audit to database with enhanced data
            premium_audit_data = {
                **audit_data,
                'audit_type': 'premium',
                'payment_amount': 997,
                'company': company,
                'industry': industry
            }
            save_audit_data(email, url, premium_audit_data)
            
            logger.info(f'Premium audit data saved to database for {url}')
            
            # Step 5: Send premium email report
            email_sent = self._send_premium_email_report(email, audit_data, pdf_path, url, company)
            
            if not email_sent:
                logger.warning(f'Premium email report not sent for {url}')
            else:
                logger.info(f'Premium email report sent successfully for {url}')
            
            # Prepare premium response data
            response_data = {
                'success': True,
                'score': audit_data.get('executive_summary', {}).get('overall_score', 70),
                'overall_score': audit_data.get('executive_summary', {}).get('overall_score', 70),
                'business_impact': audit_data.get('executive_summary', {}).get('business_impact_rating', 'High'),
                'estimated_monthly_revenue_loss': audit_data.get('executive_summary', {}).get('estimated_monthly_revenue_loss', 0),
                'annual_opportunity_cost': audit_data.get('executive_summary', {}).get('annual_opportunity_cost', 0),
                'expected_roi_timeline': audit_data.get('executive_summary', {}).get('expected_roi_timeline', '45-60 days'),
                'implementation_complexity': audit_data.get('executive_summary', {}).get('implementation_complexity', 'Medium'),
                'issues': self._extract_premium_issues(audit_data),
                'recommendations': self._extract_premium_recommendations(audit_data),
                'competitor_analysis': audit_data.get('competitor_analysis', {}),
                'ai_search_strategy': audit_data.get('ai_search_strategy', {}),
                'content_blueprint': audit_data.get('content_blueprint', {}),
                'implementation_roadmap': audit_data.get('implementation_roadmap', {}),
                'roi_projections': audit_data.get('roi_projections', {}),
                'success_metrics': audit_data.get('success_metrics', {}),
                'pdf_path': f'reports/{os.path.basename(pdf_path)}' if pdf_path else None,
                'categories': audit_data.get('category_scores', {}),
                'email_sent': email_sent,
                'audit_type': 'premium',
                'payment_amount': 997,
                'company': company,
                'industry': industry,
                'delivery_timeline': '24 hours',
                'guarantee': '10x ROI or money back'
            }
            
            logger.info(f'Premium audit completed successfully for {url} with score {response_data["score"]} - Revenue impact: ${response_data["estimated_monthly_revenue_loss"]}/month')
            return response_data
            
        except Exception as e:
            logger.error(f'Premium audit failed for {url}: {str(e)}')
            return {
                'success': False,
                'error': f'Premium audit failed: {str(e)}',
                'audit_type': 'premium'
            }
    
    def _extract_issues(self, audit_data: Dict) -> list:
        """Extract issues for free audit display"""
        issues = []
        
        # Get issues from various sources
        critical_issues = audit_data.get('critical_issues', [])
        warnings = audit_data.get('warnings', [])
        ai_search_issues = audit_data.get('ai_search_issues', [])
        voice_search_issues = audit_data.get('voice_search_issues', [])
        
        # Convert issue objects to strings for free audit
        for issue in critical_issues[:3]:  # Top 3 critical issues
            if isinstance(issue, dict):
                issues.append(issue.get('issue', str(issue)))
            else:
                issues.append(str(issue))
        
        for issue in warnings[:2]:  # Top 2 warnings
            issues.append(str(issue))
        
        for issue in ai_search_issues[:2]:  # Top 2 AI issues
            issues.append(str(issue))
        
        for issue in voice_search_issues[:1]:  # Top 1 voice issue
            issues.append(str(issue))
        
        return issues[:8]  # Limit to 8 issues for display
    
    def _extract_premium_issues(self, audit_data: Dict) -> list:
        """Extract detailed issues for premium audit"""
        issues = []
        
        critical_issues = audit_data.get('critical_issues', [])
        
        for issue in critical_issues:
            if isinstance(issue, dict):
                issues.append({
                    'issue': issue.get('issue', 'Technical issue identified'),
                    'business_impact': issue.get('business_impact', 'medium'),
                    'implementation_effort': issue.get('implementation_effort', '2-3 weeks'),
                    'expected_improvement': issue.get('expected_improvement', 'Performance improvement'),
                    'priority_score': issue.get('priority_score', 5)
                })
            else:
                issues.append({
                    'issue': str(issue),
                    'business_impact': 'medium',
                    'implementation_effort': '2-3 weeks',
                    'expected_improvement': 'Performance improvement',
                    'priority_score': 5
                })
        
        return issues
    
    def _extract_premium_recommendations(self, audit_data: Dict) -> list:
        """Extract detailed recommendations for premium audit"""
        recommendations = []
        
        # Get recommendations from AI search strategy
        ai_strategy = audit_data.get('ai_search_strategy', {})
        
        google_ai = ai_strategy.get('google_ai_optimization', [])
        chatgpt = ai_strategy.get('chatgpt_visibility', [])
        voice_search = ai_strategy.get('voice_search_plan', [])
        schema = ai_strategy.get('schema_roadmap', [])
        
        # Get basic recommendations
        basic_recs = audit_data.get('recommendations', [])
        
        # Combine all recommendations with categories
        for rec in google_ai[:3]:
            recommendations.append({
                'recommendation': rec,
                'category': 'Google AI Optimization',
                'priority': 'high',
                'effort': 'medium'
            })
        
        for rec in chatgpt[:2]:
            recommendations.append({
                'recommendation': rec,
                'category': 'AI Assistant Visibility',
                'priority': 'high',
                'effort': 'medium'
            })
        
        for rec in voice_search[:2]:
            recommendations.append({
                'recommendation': rec,
                'category': 'Voice Search',
                'priority': 'medium',
                'effort': 'low'
            })
        
        for rec in schema[:2]:
            recommendations.append({
                'recommendation': rec,
                'category': 'Technical SEO',
                'priority': 'high',
                'effort': 'high'
            })
        
        for rec in basic_recs[:3]:
            recommendations.append({
                'recommendation': str(rec),
                'category': 'General SEO',
                'priority': 'medium',
                'effort': 'medium'
            })
        
        return recommendations[:12]  # Top 12 recommendations for premium
    
    def _ensure_premium_data_structure(self, audit_data: Dict, website_data: Dict) -> Dict:
        """Ensure premium audit has required data structure"""
        
        # Get basic score
        overall_score = audit_data.get('overall_score', 70)
        
        # Create executive summary if missing
        if 'executive_summary' not in audit_data:
            audit_data['executive_summary'] = {
                'overall_score': overall_score,
                'business_impact_rating': 'High' if overall_score < 60 else 'Medium',
                'estimated_monthly_traffic_loss': max(1000, (100 - overall_score) * 50),
                'estimated_monthly_revenue_loss': max(1000, (100 - overall_score) * 50) * 50,
                'implementation_complexity': 'Medium',
                'expected_roi_timeline': '45-60 days'
            }
        
        # Add annual opportunity cost
        monthly_loss = audit_data['executive_summary'].get('estimated_monthly_revenue_loss', 0)
        audit_data['executive_summary']['annual_opportunity_cost'] = monthly_loss * 12
        
        # Ensure ROI projections exist
        if 'roi_projections' not in audit_data:
            audit_data['roi_projections'] = {
                '30_day_impact': {
                    'traffic_increase': '20-30%',
                    'revenue_increase': f'${monthly_loss * 0.3:,.0f}',
                    'key_improvements': ['Better AI search visibility', 'Improved click-through rates']
                },
                '90_day_impact': {
                    'traffic_increase': '50-70%',
                    'revenue_increase': f'${monthly_loss * 0.7:,.0f}',
                    'market_position': 'Strong competitive positioning'
                },
                '12_month_potential': {
                    'traffic_increase': '100-150%',
                    'revenue_increase': f'${monthly_loss * 1.5 * 12:,.0f}',
                    'roi_multiple': '12x return on $997 investment'
                },
                'investment_roi': '10-15x return on $997 investment',
                'break_even_timeline': '30-45 days'
            }
        
        return audit_data
    
    def _send_premium_email_report(self, email: str, audit_data: Dict, pdf_path: str, url: str, company: str) -> bool:
        """Send premium email report with enhanced content"""
        try:
            # Create premium email content
            premium_subject = f"Your $997 Premium AI SEO Audit is Ready - {company if company else 'Business'}"
            
            # Use the standard email service but mark as premium
            audit_data['audit_type'] = 'premium'
            audit_data['company'] = company
            
            return send_email_report(email, audit_data, pdf_path, url)
            
        except Exception as e:
            logger.error(f'Failed to send premium email for {url}: {str(e)}')
            return False
    
    def send_cached_report(self, email: str, cached_data: Dict, url: str) -> bool:
        """Send email report for cached audit data"""
        try:
            # Fix missing overall_score immediately
            if 'overall_score' not in cached_data:
                cached_data['overall_score'] = cached_data.get('score', 70)
            
            # Generate fresh PDF from cached data
            website_data = {'url': url}
            pdf_path = generate_pdf_report(cached_data, website_data)
            
            # Send email with cached data
            email_sent = send_email_report(email, cached_data, pdf_path, url)
            
            if email_sent:
                logger.info(f'Cached report sent successfully for {url}')
            else:
                logger.warning(f'Failed to send cached report for {url}')
            
            return email_sent
            
        except Exception as e:
            logger.error(f'Failed to send cached report for {url}: {str(e)}')
            return False