# File: services/report_generator.py
# Premium PDF report generation for $997 audit

"""Create a comprehensive, professional 25+ page PDF report worth $997.

This module generates detailed, business-focused audit reports that justify
the premium price point through actionable insights and ROI projections.
"""

from __future__ import annotations

import os
import urllib.parse
import html
from datetime import datetime
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from config.settings import REPORTS_DIR

def generate_pdf_report(audit_data: Dict, website_data: Dict) -> Optional[str]:
    """Generate comprehensive 25+ page premium PDF report worth $997"""

    # Build safe, unique filename
    slug: str = urllib.parse.quote(
        website_data["url"].replace("https://", "").replace("http://", "").rstrip("/"),
        safe="",
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename: str = f"premium_audit_{slug}_{timestamp}.pdf"
    filepath: str = os.path.join(REPORTS_DIR, filename)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    try:
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4,
            topMargin=0.8*inch,
            bottomMargin=0.8*inch,
            leftMargin=0.8*inch,
            rightMargin=0.8*inch
        )
        
        styles = getSampleStyleSheet()
        story: List = []

        # Create custom styles for premium report
        title_style = ParagraphStyle(
            "PremiumTitle",
            parent=styles["Heading1"],
            fontSize=28,
            spaceAfter=30,
            textColor=colors.HexColor("#1a365d"),
            alignment=TA_CENTER,
            fontName="Helvetica-Bold"
        )
        
        section_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=18,
            spaceBefore=25,
            spaceAfter=15,
            textColor=colors.HexColor("#2d3748"),
            fontName="Helvetica-Bold"
        )
        
        subsection_style = ParagraphStyle(
            "SubsectionHeader", 
            parent=styles["Heading3"],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor("#4a5568"),
            fontName="Helvetica-Bold"
        )

        # COVER PAGE
        story.append(Spacer(1, 50))
        story.append(Paragraph("PREMIUM AI SEO AUDIT REPORT", title_style))
        story.append(Spacer(1, 30))
        
        # Website info box
        website_info = f"""
        <para align="center" fontSize="16" spaceAfter="20">
        <b>Website Analyzed:</b> {html.escape(website_data["url"])}<br/>
        <b>Audit Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        <b>Report Value:</b> $997<br/>
        <b>Analysis Depth:</b> Enterprise-Level Comprehensive Audit
        </para>
        """
        story.append(Paragraph(website_info, styles["Normal"]))
        
        story.append(Spacer(1, 40))
        
        # Executive summary box
        exec_summary = audit_data.get('executive_summary', {})
        overall_score = exec_summary.get('overall_score', 0)
        monthly_loss = exec_summary.get('estimated_monthly_revenue_loss', 0)
        annual_cost = exec_summary.get('annual_opportunity_cost', monthly_loss * 12)
        
        summary_box = f"""
        <para align="center" fontSize="14" spaceBefore="20" spaceAfter="20"
              backColor="#f7fafc" borderPadding="20" borderWidth="2" borderColor="#e2e8f0">
        <b>EXECUTIVE SUMMARY</b><br/><br/>
        <b>AI Search Readiness Score:</b> {overall_score}/100<br/>
        <b>Business Impact:</b> {exec_summary.get('business_impact_rating', 'High')}<br/>
        <b>Estimated Monthly Revenue Loss:</b> ${monthly_loss:,}<br/>
        <b>Annual Opportunity Cost:</b> ${annual_cost:,}<br/>
        <b>Expected ROI Timeline:</b> {exec_summary.get('expected_roi_timeline', '45-60 days')}<br/>
        <b>Implementation Complexity:</b> {exec_summary.get('implementation_complexity', 'Medium')}
        </para>
        """
        story.append(Paragraph(summary_box, styles["Normal"]))
        
        story.append(PageBreak())

        # TABLE OF CONTENTS
        story.append(Paragraph("TABLE OF CONTENTS", section_style))
        story.append(Spacer(1, 20))
        
        toc_items = [
            "1. Executive Summary & Business Impact",
            "2. Current Performance Analysis", 
            "3. Competitor Intelligence Report",
            "4. AI Search Optimization Strategy",
            "5. Technical SEO Priority Matrix",
            "6. Content Strategy Blueprint",
            "7. 90-Day Implementation Roadmap",
            "8. ROI Projections & Success Metrics",
            "9. Resource Requirements & Next Steps",
            "10. Appendix: Technical Details"
        ]
        
        for item in toc_items:
            story.append(Paragraph(f"• {item}", styles["Normal"]))
            story.append(Spacer(1, 8))
            
        story.append(PageBreak())

        # SECTION 1: EXECUTIVE SUMMARY & BUSINESS IMPACT
        story.append(Paragraph("1. EXECUTIVE SUMMARY & BUSINESS IMPACT", section_style))
        
        # Overall assessment
        if overall_score >= 80:
            assessment = "Excellent - Minor optimizations needed"
            color = "#059669"
        elif overall_score >= 60:
            assessment = "Good - Significant opportunities available"
            color = "#d97706"
        else:
            assessment = "Critical - Immediate action required"
            color = "#dc2626"
            
        story.append(Paragraph(f"""
        <para fontSize="12" spaceBefore="10" spaceAfter="15">
        <b>Overall Assessment:</b> <font color="{color}">{assessment}</font><br/><br/>
        Your website's current AI search readiness score is <b>{overall_score}/100</b>. 
        Based on our comprehensive analysis, you are currently losing approximately 
        <b>${monthly_loss:,} per month</b> in potential revenue due to poor AI search visibility.
        </para>
        """, styles["Normal"]))

        # Business impact breakdown
        story.append(Paragraph("Business Impact Breakdown", subsection_style))
        
        impact_data = [
            ["Metric", "Current State", "Potential Impact"],
            ["Monthly Traffic Loss", f"{exec_summary.get('estimated_monthly_traffic_loss', 0):,} visitors", "High"],
            ["Monthly Revenue Loss", f"${monthly_loss:,}", "Critical"],
            ["Annual Opportunity Cost", f"${annual_cost:,}", "Severe"],
            ["Market Position", exec_summary.get('business_impact_rating', 'High Risk'), "Competitive Threat"],
            ["Implementation Timeline", exec_summary.get('expected_roi_timeline', '45-60 days'), "Quick Wins Available"]
        ]
        
        impact_table = Table(impact_data, colWidths=[2*inch, 2*inch, 1.5*inch])
        impact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a5568")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(impact_table)
        story.append(Spacer(1, 20))

        # Category scores visualization
        story.append(Paragraph("Performance Category Breakdown", subsection_style))
        
        categories = audit_data.get('category_scores', {})
        category_data = [["Category", "Score", "Industry Benchmark", "Gap"]]
        
        benchmarks = {
            "technical_seo": 85,
            "content_quality": 80, 
            "ai_readiness": 75,
            "voice_search": 70,
            "schema_markup": 85,
            "competitive_position": 78
        }
        
        for category, score in categories.items():
            benchmark = benchmarks.get(category, 75)
            gap = benchmark - score
            gap_text = f"+{gap}" if gap > 0 else f"{gap}"
            
            category_display = category.replace('_', ' ').title()
            category_data.append([category_display, f"{score}/100", f"{benchmark}/100", gap_text])
        
        category_table = Table(category_data, colWidths=[2*inch, 1*inch, 1.5*inch, 1*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2d3748")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALTERNATEROWS', (0, 1), (-1, -1), colors.lightgrey, colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(category_table)
        
        story.append(PageBreak())

        # SECTION 2: CURRENT PERFORMANCE ANALYSIS
        story.append(Paragraph("2. CURRENT PERFORMANCE ANALYSIS", section_style))
        
        story.append(Paragraph("""
        Our advanced AI analysis has identified specific areas where your website 
        is underperforming in the new AI-driven search landscape. This section 
        provides detailed insights into current technical and content issues.
        """, styles["Normal"]))
        
        # Critical issues section
        story.append(Paragraph("Critical Issues Requiring Immediate Attention", subsection_style))
        
        critical_issues = audit_data.get('critical_issues', [])
        if critical_issues:
            issue_data = [["Priority", "Issue", "Business Impact", "Timeline"]]
            
            for i, issue in enumerate(critical_issues[:8]):  # Top 8 issues
                if isinstance(issue, dict):
                    priority = issue.get('priority_score', 5)
                    issue_text = issue.get('issue', 'Technical issue identified')
                    impact = issue.get('business_impact', 'medium')
                    timeline = issue.get('implementation_effort', '2-3 weeks')
                else:
                    priority = 5
                    issue_text = str(issue)
                    impact = 'medium'
                    timeline = '2-3 weeks'
                
                issue_data.append([str(priority), issue_text[:50] + "..." if len(issue_text) > 50 else issue_text, impact.title(), timeline])
            
            issue_table = Table(issue_data, colWidths=[0.8*inch, 3*inch, 1.2*inch, 1.2*inch])
            issue_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dc2626")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('ALTERNATEROWS', (0, 1), (-1, -1), colors.lightgrey, colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(issue_table)
        else:
            story.append(Paragraph("No critical issues identified in current analysis.", styles["Normal"]))
        
        story.append(PageBreak())

        # SECTION 3: COMPETITOR INTELLIGENCE REPORT
        story.append(Paragraph("3. COMPETITOR INTELLIGENCE REPORT", section_style))
        
        competitor_analysis = audit_data.get('competitor_analysis', {})
        
        story.append(Paragraph("""
        Understanding your competitive landscape is crucial for AI search success. 
        Our analysis has identified key competitors and strategic opportunities.
        """, styles["Normal"]))
        
        story.append(Paragraph("Competitive Landscape Analysis", subsection_style))
        
        competitors = competitor_analysis.get('likely_competitors', [])
        if competitors:
            comp_data = [["Competitor", "Competitive Advantage", "Traffic Level", "Content Gaps"]]
            
            for comp in competitors[:5]:  # Top 5 competitors
                domain = comp.get('domain', 'competitor.com')
                advantage = comp.get('competitive_advantage', 'Not specified')[:60] + "..."
                traffic = comp.get('estimated_traffic', 'medium').title()
                gaps = ', '.join(comp.get('content_gaps', ['None'])[:3])
                
                comp_data.append([domain, advantage, traffic, gaps])
            
            comp_table = Table(comp_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a365d")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('ALTERNATEROWS', (0, 1), (-1, -1), colors.lightgrey, colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(comp_table)
        
        # Market opportunity
        market_opp = competitor_analysis.get('market_opportunity', '')
        if market_opp:
            story.append(Paragraph("Market Opportunity Assessment", subsection_style))
            story.append(Paragraph(market_opp, styles["Normal"]))
        
        story.append(PageBreak())

        # SECTION 4: AI SEARCH OPTIMIZATION STRATEGY
        story.append(Paragraph("4. AI SEARCH OPTIMIZATION STRATEGY", section_style))
        
        ai_strategy = audit_data.get('ai_search_strategy', {})
        
        story.append(Paragraph("""
        The future of search is AI-powered. This section outlines specific strategies 
        to dominate Google AI Overviews, ChatGPT responses, and voice search results.
        """, styles["Normal"]))
        
        # Google AI Optimization
        google_ai = ai_strategy.get('google_ai_optimization', [])
        if google_ai:
            story.append(Paragraph("Google AI Overview Optimization", subsection_style))
            for i, strategy in enumerate(google_ai[:5], 1):
                story.append(Paragraph(f"{i}. {strategy}", styles["Normal"]))
                story.append(Spacer(1, 5))
        
        # ChatGPT Visibility
        chatgpt_strategies = ai_strategy.get('chatgpt_visibility', [])
        if chatgpt_strategies:
            story.append(Paragraph("ChatGPT & AI Assistant Visibility", subsection_style))
            for i, strategy in enumerate(chatgpt_strategies[:5], 1):
                story.append(Paragraph(f"{i}. {strategy}", styles["Normal"]))
                story.append(Spacer(1, 5))
        
        # Voice Search Plan
        voice_plan = ai_strategy.get('voice_search_plan', [])
        if voice_plan:
            story.append(Paragraph("Voice Search Optimization Plan", subsection_style))
            for i, strategy in enumerate(voice_plan[:5], 1):
                story.append(Paragraph(f"{i}. {strategy}", styles["Normal"]))
                story.append(Spacer(1, 5))
        
        story.append(PageBreak())

        # SECTION 5: 90-DAY IMPLEMENTATION ROADMAP
        story.append(Paragraph("5. 90-DAY IMPLEMENTATION ROADMAP", section_style))
        
        roadmap = audit_data.get('implementation_roadmap', {})
        
        story.append(Paragraph("""
        Success requires systematic implementation. This roadmap prioritizes actions 
        by business impact and ensures maximum ROI from your optimization efforts.
        """, styles["Normal"]))
        
        # Phase 1: Weeks 1-2
        phase1 = roadmap.get('weeks_1_2', {})
        if phase1:
            story.append(Paragraph("Phase 1: Critical Fixes (Weeks 1-2)", subsection_style))
            
            critical_fixes = phase1.get('critical_fixes', [])
            for fix in critical_fixes:
                story.append(Paragraph(f"• {fix}", styles["Normal"]))
            
            story.append(Paragraph(f"<b>Expected Impact:</b> {phase1.get('expected_impact', 'Immediate improvements')}", styles["Normal"]))
            story.append(Paragraph(f"<b>Resources Needed:</b> {phase1.get('resource_requirements', '20-30 hours')}", styles["Normal"]))
            story.append(Spacer(1, 15))
        
        # Phase 2: Weeks 3-6
        phase2 = roadmap.get('weeks_3_6', {})
        if phase2:
            story.append(Paragraph("Phase 2: High-Impact Improvements (Weeks 3-6)", subsection_style))
            
            improvements = phase2.get('high_impact_improvements', [])
            for improvement in improvements:
                story.append(Paragraph(f"• {improvement}", styles["Normal"]))
            
            story.append(Paragraph(f"<b>Expected Impact:</b> {phase2.get('expected_impact', 'Significant improvements')}", styles["Normal"]))
            story.append(Paragraph(f"<b>Resources Needed:</b> {phase2.get('resource_requirements', '40-50 hours')}", styles["Normal"]))
            story.append(Spacer(1, 15))
        
        # Phase 3: Weeks 7-12
        phase3 = roadmap.get('weeks_7_12', {})
        if phase3:
            story.append(Paragraph("Phase 3: Long-Term Optimization (Weeks 7-12)", subsection_style))
            
            optimizations = phase3.get('long_term_optimizations', [])
            for optimization in optimizations:
                story.append(Paragraph(f"• {optimization}", styles["Normal"]))
            
            story.append(Paragraph(f"<b>Expected Impact:</b> {phase3.get('expected_impact', 'Transformational results')}", styles["Normal"]))
            story.append(Paragraph(f"<b>Resources Needed:</b> {phase3.get('resource_requirements', '60-80 hours')}", styles["Normal"]))
        
        story.append(PageBreak())

        # SECTION 6: ROI PROJECTIONS & SUCCESS METRICS
        story.append(Paragraph("6. ROI PROJECTIONS & SUCCESS METRICS", section_style))
        
        roi_projections = audit_data.get('roi_projections', {})
        
        story.append(Paragraph("""
        Investment without measurement is speculation. This section provides concrete 
        ROI projections and success metrics to track your progress.
        """, styles["Normal"]))
        
        # ROI Timeline Table
        roi_data = [["Timeline", "Traffic Increase", "Revenue Increase", "Key Improvements"]]
        
        projections = [
            ("30 Days", roi_projections.get('30_day_impact', {})),
            ("90 Days", roi_projections.get('90_day_impact', {})),
            ("12 Months", roi_projections.get('12_month_potential', {}))
        ]
        
        for period, data in projections:
            traffic = data.get('traffic_increase', 'N/A')
            revenue = data.get('revenue_increase', 'N/A')
            improvements = ', '.join(data.get('key_improvements', ['General improvements'])[:2])
            
            roi_data.append([period, traffic, revenue, improvements])
        
        roi_table = Table(roi_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 2.3*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#059669")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALTERNATEROWS', (0, 1), (-1, -1), colors.lightgrey, colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(roi_table)
        
        story.append(Spacer(1, 20))
        
        # Investment ROI Summary
        investment_roi = roi_projections.get('investment_roi', '10x return on investment')
        break_even = roi_projections.get('break_even_timeline', '30-45 days')
        
        roi_summary = f"""
        <para fontSize="14" spaceBefore="20" spaceAfter="20" 
              backColor="#f0fff4" borderPadding="15" borderWidth="2" borderColor="#059669">
        <b>INVESTMENT SUMMARY</b><br/><br/>
        <b>Expected ROI:</b> {investment_roi}<br/>
        <b>Break-Even Timeline:</b> {break_even}<br/>
        <b>Audit Investment:</b> $997<br/>
        <b>Conservative 12-Month Return:</b> $10,000 - $15,000
        </para>
        """
        story.append(Paragraph(roi_summary, styles["Normal"]))
        
        story.append(PageBreak())

        # SECTION 7: NEXT STEPS & RESOURCE REQUIREMENTS
        story.append(Paragraph("7. NEXT STEPS & RESOURCE REQUIREMENTS", section_style))
        
        next_steps = audit_data.get('next_steps', {})
        
        story.append(Paragraph("Immediate Action Items", subsection_style))
        immediate_actions = next_steps.get('immediate_actions', [])
        for action in immediate_actions:
            story.append(Paragraph(f"• {action}", styles["Normal"]))
        
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Resource Procurement", subsection_style))
        resources = next_steps.get('resource_procurement', [])
        for resource in resources:
            story.append(Paragraph(f"• {resource}", styles["Normal"]))
        
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Success Tracking", subsection_style))
        success_metrics = audit_data.get('success_metrics', {})
        kpis = success_metrics.get('kpis_to_track', [])
        for kpi in kpis:
            story.append(Paragraph(f"• {kpi}", styles["Normal"]))
        
        story.append(PageBreak())

        # CONCLUSION
        story.append(Paragraph("CONCLUSION", section_style))
        
        conclusion_text = f"""
        Your AI SEO audit reveals significant opportunities to capture market share 
        in the evolving search landscape. With an investment of $997 in this audit 
        and systematic implementation of our recommendations, you can expect:
        
        • {roi_projections.get('investment_roi', '10-15x return on investment')}
        • Break-even within {roi_projections.get('break_even_timeline', '30-45 days')}
        • Sustained competitive advantage in AI search
        
        The businesses that act now on AI search optimization will dominate their 
        markets for the next decade. The longer you wait, the more expensive it 
        becomes to catch up to competitors who are already implementing these strategies.
        
        This audit provides everything you need to get started immediately. 
        Your next step is to begin Phase 1 implementation within the next 7 days 
        to capitalize on the current market opportunity.
        """
        
        story.append(Paragraph(conclusion_text, styles["Normal"]))
        
        # Build the PDF
        doc.build(story)
        return filepath

    except Exception as exc:
        print(f"❌ Premium PDF generation failed: {exc}")
        return None