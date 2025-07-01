# File: models/database.py
# Enhanced database models for premium audit system

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import DATABASE_PATH

def get_db_connection():
    """Get database connection with proper configuration"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_database():
    """Initialize SQLite database with enhanced schema for premium audits"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Enhanced audits table with premium features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                url TEXT NOT NULL,
                company TEXT DEFAULT '',
                industry TEXT DEFAULT '',
                audit_type TEXT DEFAULT 'free',
                payment_amount REAL DEFAULT 0,
                payment_status TEXT DEFAULT 'pending',
                stripe_session_id TEXT DEFAULT '',
                overall_score INTEGER DEFAULT 0,
                business_impact_rating TEXT DEFAULT '',
                estimated_monthly_revenue_loss REAL DEFAULT 0,
                annual_opportunity_cost REAL DEFAULT 0,
                implementation_complexity TEXT DEFAULT '',
                expected_roi_timeline TEXT DEFAULT '',
                technical_score INTEGER DEFAULT 0,
                content_score INTEGER DEFAULT 0,
                ai_readiness_score INTEGER DEFAULT 0,
                voice_search_score INTEGER DEFAULT 0,
                schema_markup_score INTEGER DEFAULT 0,
                competitive_position_score INTEGER DEFAULT 0,
                audit_data TEXT,
                pdf_report_path TEXT DEFAULT '',
                email_sent INTEGER DEFAULT 0,
                email_sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                customer_ip TEXT DEFAULT '',
                user_agent TEXT DEFAULT ''
            )
        ''')
        
        # Premium customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS premium_customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                company TEXT DEFAULT '',
                industry TEXT DEFAULT '',
                total_audits INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0,
                first_purchase_date TIMESTAMP,
                last_purchase_date TIMESTAMP,
                customer_lifetime_value REAL DEFAULT 0,
                referral_source TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Business metrics table for tracking performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                free_audits_count INTEGER DEFAULT 0,
                premium_audits_count INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                average_score REAL DEFAULT 0,
                email_open_rate REAL DEFAULT 0,
                refund_requests INTEGER DEFAULT 0,
                customer_satisfaction REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lead tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                url TEXT NOT NULL,
                company TEXT DEFAULT '',
                industry TEXT DEFAULT '',
                lead_source TEXT DEFAULT 'organic',
                utm_source TEXT DEFAULT '',
                utm_medium TEXT DEFAULT '',
                utm_campaign TEXT DEFAULT '',
                converted_to_premium INTEGER DEFAULT 0,
                conversion_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Email campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                campaign_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                sent_at TIMESTAMP,
                opened_at TIMESTAMP,
                clicked_at TIMESTAMP,
                converted_at TIMESTAMP,
                audit_id INTEGER,
                FOREIGN KEY (audit_id) REFERENCES audits (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audits_email ON audits(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audits_created_at ON audits(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audits_audit_type ON audits(audit_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audits_payment_status ON audits(payment_status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_premium_customers_email ON premium_customers(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)')

def save_audit_data(email: str, url: str, audit_data: dict, **kwargs):
    """Save enhanced audit data to database with proper transaction handling"""
    
    # Extract additional data
    company = kwargs.get('company', '')
    industry = kwargs.get('industry', '')
    audit_type = kwargs.get('audit_type', audit_data.get('audit_type', 'free'))
    payment_amount = kwargs.get('payment_amount', audit_data.get('payment_amount', 0))
    customer_ip = kwargs.get('customer_ip', '')
    user_agent = kwargs.get('user_agent', '')
    
    # Extract scores from audit data
    executive_summary = audit_data.get('executive_summary', {})
    category_scores = audit_data.get('category_scores', {})
    
    overall_score = executive_summary.get('overall_score', audit_data.get('overall_score', 0))
    business_impact = executive_summary.get('business_impact_rating', '')
    monthly_loss = executive_summary.get('estimated_monthly_revenue_loss', 0)
    annual_cost = executive_summary.get('annual_opportunity_cost', 0)
    complexity = executive_summary.get('implementation_complexity', '')
    roi_timeline = executive_summary.get('expected_roi_timeline', '')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('BEGIN TRANSACTION')
            
            # Insert audit data
            cursor.execute('''
                INSERT INTO audits (
                    email, url, company, industry, audit_type, payment_amount,
                    overall_score, business_impact_rating, estimated_monthly_revenue_loss,
                    annual_opportunity_cost, implementation_complexity, expected_roi_timeline,
                    technical_score, content_score, ai_readiness_score, voice_search_score,
                    schema_markup_score, competitive_position_score, audit_data,
                    customer_ip, user_agent, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                email, url, company, industry, audit_type, payment_amount,
                overall_score, business_impact, monthly_loss, annual_cost, complexity, roi_timeline,
                category_scores.get('technical_seo', 0),
                category_scores.get('content_quality', 0),
                category_scores.get('ai_readiness', 0),
                category_scores.get('voice_search', 0),
                category_scores.get('schema_markup', 0),
                category_scores.get('competitive_position', 0),
                json.dumps(audit_data),
                customer_ip, user_agent, datetime.now()
            ))
            
            audit_id = cursor.lastrowid
            
            # Update or create premium customer record if premium audit
            if audit_type == 'premium':
                # Check if customer exists
                cursor.execute('''
                    SELECT id, total_audits, total_spent, first_purchase_date 
                    FROM premium_customers WHERE email = ?
                ''', (email,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing customer
                    cursor.execute('''
                        UPDATE premium_customers 
                        SET company = ?, industry = ?, total_audits = total_audits + 1, 
                            total_spent = total_spent + ?, last_purchase_date = ?,
                            customer_lifetime_value = customer_lifetime_value + ?
                        WHERE email = ?
                    ''', (company, industry, payment_amount, datetime.now(), payment_amount, email))
                else:
                    # Insert new customer
                    cursor.execute('''
                        INSERT INTO premium_customers (
                            email, company, industry, total_audits, total_spent,
                            first_purchase_date, last_purchase_date, customer_lifetime_value
                        ) VALUES (?, ?, ?, 1, ?, ?, ?, ?)
                    ''', (email, company, industry, payment_amount, datetime.now(), datetime.now(), payment_amount))
            
            cursor.execute('COMMIT')
            return audit_id
            
        except Exception as e:
            cursor.execute('ROLLBACK')
            raise e

def save_lead_data(email: str, url: str, **kwargs):
    """Save lead data for marketing tracking"""
    company = kwargs.get('company', '')
    industry = kwargs.get('industry', '')
    lead_source = kwargs.get('lead_source', 'organic')
    utm_source = kwargs.get('utm_source', '')
    utm_medium = kwargs.get('utm_medium', '')
    utm_campaign = kwargs.get('utm_campaign', '')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO leads (
                email, url, company, industry, lead_source,
                utm_source, utm_medium, utm_campaign
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, url, company, industry, lead_source, utm_source, utm_medium, utm_campaign))

def update_payment_status(audit_id: int, payment_status: str, stripe_session_id: str = ''):
    """Update payment status for an audit"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE audits 
            SET payment_status = ?, stripe_session_id = ?
            WHERE id = ?
        ''', (payment_status, stripe_session_id, audit_id))

def mark_email_sent(audit_id: int, pdf_path: str = ''):
    """Mark audit email as sent"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE audits 
            SET email_sent = 1, email_sent_at = ?, pdf_report_path = ?
            WHERE id = ?
        ''', (datetime.now(), pdf_path, audit_id))

def get_business_metrics(days: int = 30) -> Dict:
    """Get business metrics for the last N days"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get audit statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total_audits,
                COUNT(CASE WHEN audit_type = 'free' THEN 1 END) as free_audits,
                COUNT(CASE WHEN audit_type = 'premium' THEN 1 END) as premium_audits,
                SUM(CASE WHEN audit_type = 'premium' THEN payment_amount ELSE 0 END) as revenue,
                AVG(overall_score) as avg_score,
                COUNT(CASE WHEN email_sent = 1 THEN 1 END) as emails_sent
            FROM audits 
            WHERE created_at > datetime('now', ? || ' days')
        ''', (-days,))
        
        metrics = cursor.fetchone()
        
        # Get conversion rate
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT email) as unique_visitors,
                COUNT(CASE WHEN audit_type = 'premium' THEN 1 END) as premium_conversions
            FROM audits 
            WHERE created_at > datetime('now', ? || ' days')
        ''', (-days,))
        
        conversion_data = cursor.fetchone()
        
        # Get top performing pages/sources
        cursor.execute('''
            SELECT industry, COUNT(*) as count
            FROM audits 
            WHERE created_at > datetime('now', ? || ' days') AND industry != ''
            GROUP BY industry
            ORDER BY count DESC
            LIMIT 5
        ''', (-days,))
        
        top_industries = cursor.fetchall()
        
        conversion_rate = 0
        if conversion_data[0] > 0:
            conversion_rate = (conversion_data[1] / conversion_data[0]) * 100
        
        return {
            'total_audits': metrics[0] or 0,
            'free_audits': metrics[1] or 0,
            'premium_audits': metrics[2] or 0,
            'revenue': metrics[3] or 0,
            'average_score': round(metrics[4] or 0, 1),
            'emails_sent': metrics[5] or 0,
            'unique_visitors': conversion_data[0] or 0,
            'conversion_rate': round(conversion_rate, 2),
            'top_industries': [{'industry': row[0], 'count': row[1]} for row in top_industries]
        }

def get_premium_customer_data(email: str) -> Optional[Dict]:
    """Get premium customer data"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM premium_customers WHERE email = ?
        ''', (email,))
        
        result = cursor.fetchone()
        
        if result:
            return {
                'email': result[1],
                'company': result[2],
                'industry': result[3],
                'total_audits': result[4],
                'total_spent': result[5],
                'first_purchase_date': result[6],
                'last_purchase_date': result[7],
                'customer_lifetime_value': result[8]
            }
        
        return None

def get_audit_history(email: str, limit: int = 10) -> List[Dict]:
    """Get audit history for a customer"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, url, audit_type, overall_score, payment_amount, 
                   created_at, completed_at, email_sent
            FROM audits 
            WHERE email = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (email, limit))
        
        results = cursor.fetchall()
        
        return [{
            'id': row[0],
            'url': row[1],
            'audit_type': row[2],
            'score': row[3],
            'payment_amount': row[4],
            'created_at': row[5],
            'completed_at': row[6],
            'email_sent': bool(row[7])  # Convert integer to boolean
        } for row in results]

def save_email_campaign_data(email: str, campaign_type: str, subject: str, audit_id: int = None):
    """Save email campaign tracking data"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO email_campaigns (
                email, campaign_type, subject, sent_at, audit_id
            ) VALUES (?, ?, ?, ?, ?)
        ''', (email, campaign_type, subject, datetime.now(), audit_id))

def update_daily_metrics():
    """Update daily business metrics summary"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        # Get today's metrics
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN audit_type = 'free' THEN 1 END) as free_count,
                COUNT(CASE WHEN audit_type = 'premium' THEN 1 END) as premium_count,
                SUM(CASE WHEN audit_type = 'premium' THEN payment_amount ELSE 0 END) as revenue,
                AVG(overall_score) as avg_score
            FROM audits 
            WHERE DATE(created_at) = ?
        ''', (today,))
        
        daily_data = cursor.fetchone()
        
        # Calculate conversion rate
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT email) as visitors,
                COUNT(CASE WHEN audit_type = 'premium' THEN 1 END) as conversions
            FROM audits 
            WHERE DATE(created_at) = ?
        ''', (today,))
        
        conversion_data = cursor.fetchone()
        
        conversion_rate = 0
        if conversion_data[0] > 0:
            conversion_rate = (conversion_data[1] / conversion_data[0]) * 100
        
        # Insert or update daily metrics
        cursor.execute('''
            INSERT OR REPLACE INTO business_metrics (
                date, free_audits_count, premium_audits_count, revenue,
                conversion_rate, average_score
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            today, daily_data[0], daily_data[1], daily_data[2] or 0,
            conversion_rate, daily_data[3] or 0
        ))

def get_recent_audit_data(audit_id: int) -> Optional[Dict]:
    """Get recent audit data for debugging/testing"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT audit_data, overall_score, technical_score, content_score
            FROM audits WHERE id = ?
        ''', (audit_id,))
        
        result = cursor.fetchone()
        if result:
            try:
                audit_data = json.loads(result[0]) if result[0] else {}
                return {
                    'audit_data': audit_data,
                    'overall_score': result[1],
                    'technical_score': result[2],
                    'content_score': result[3]
                }
            except json.JSONDecodeError:
                return None
        return None