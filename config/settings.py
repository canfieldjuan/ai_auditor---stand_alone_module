# File: config/settings.py
# Enhanced configuration settings for premium $997 audit model

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Settings
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Database
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/seo_auditor.db')

# Directories
REPORTS_DIR = os.getenv('REPORTS_DIR', 'reports')
CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
LOGS_DIR = os.getenv('LOGS_DIR', 'logs')
STATIC_DIR = os.getenv('STATIC_DIR', 'static')

# Email Configuration - Resend API
RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@aiauditortool.com')  # Your verified domain email
FROM_NAME = os.getenv('FROM_NAME', 'Premium AI SEO Audit')
RESEND_FROM_EMAIL = FROM_EMAIL  # Alias for backward compatibility

# Legacy email settings (kept for backward compatibility)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.resend.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587')) if os.getenv('EMAIL_PORT', '587').isdigit() else 587
EMAIL_USER = os.getenv('EMAIL_USER', '')  # Not used with Resend API
EMAIL_PASS = os.getenv('EMAIL_PASS', '')  # Not used with Resend API

# AI API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')

# Stripe Payment Configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# Premium Audit Settings
try:
    PREMIUM_PRICE = int(os.getenv('PREMIUM_PRICE', '997'))
except ValueError:
    PREMIUM_PRICE = 997

try:
    PREMIUM_SLOTS_PER_MONTH = int(os.getenv('PREMIUM_SLOTS_PER_MONTH', '20'))
except ValueError:
    PREMIUM_SLOTS_PER_MONTH = 20

try:
    PREMIUM_DELIVERY_HOURS = int(os.getenv('PREMIUM_DELIVERY_HOURS', '24'))
except ValueError:
    PREMIUM_DELIVERY_HOURS = 24

# Business Configuration
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Premium AI SEO Audit')
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@aiauditortool.com')
BUSINESS_URL = os.getenv('BUSINESS_URL', 'https://aiauditortool.com')

# Rate Limiting
try:
    RATE_LIMIT_PER_IP = int(os.getenv('RATE_LIMIT_PER_IP', '100'))
except ValueError:
    RATE_LIMIT_PER_IP = 100

try:
    RATE_LIMIT_PER_EMAIL = int(os.getenv('RATE_LIMIT_PER_EMAIL', '50'))
except ValueError:
    RATE_LIMIT_PER_EMAIL = 50

try:
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))
except ValueError:
    RATE_LIMIT_WINDOW = 3600

# Cache Settings
try:
    CACHE_TTL = int(os.getenv('CACHE_TTL', '7200'))
except ValueError:
    CACHE_TTL = 7200

try:
    PREMIUM_CACHE_TTL = int(os.getenv('PREMIUM_CACHE_TTL', '0'))
except ValueError:
    PREMIUM_CACHE_TTL = 0

# Analytics & Tracking
GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')
FACEBOOK_PIXEL_ID = os.getenv('FACEBOOK_PIXEL_ID', '')

# Email Marketing
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID', '')

# Business Metrics (for ROI calculations)
try:
    VISITOR_VALUE_USD = int(os.getenv('VISITOR_VALUE_USD', '50'))
except ValueError:
    VISITOR_VALUE_USD = 50

try:
    CONVERSION_RATE = float(os.getenv('CONVERSION_RATE', '0.02'))
except ValueError:
    CONVERSION_RATE = 0.02

# Security Settings
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
try:
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))
except ValueError:
    MAX_CONTENT_LENGTH = 16777216

# Audit Configuration
try:
    MAX_CONCURRENT_AUDITS = int(os.getenv('MAX_CONCURRENT_AUDITS', '5'))
except ValueError:
    MAX_CONCURRENT_AUDITS = 5

try:
    AUDIT_TIMEOUT_SECONDS = int(os.getenv('AUDIT_TIMEOUT_SECONDS', '300'))
except ValueError:
    AUDIT_TIMEOUT_SECONDS = 300

# ✅ **FIXED: Added the missing ENABLED_MODULES configuration**
ENABLED_MODULES = [
    'technical_seo',
    'content',
    'keywords',
    'backlinks',
    'recommendations',
    'quick_wins',
]

# Feature Flags
ENABLE_FREE_AUDITS = os.getenv('ENABLE_FREE_AUDITS', 'True').lower() == 'true'
ENABLE_PREMIUM_AUDITS = os.getenv('ENABLE_PREMIUM_AUDITS', 'True').lower() == 'true'
ENABLE_STRIPE_PAYMENTS = os.getenv('ENABLE_STRIPE_PAYMENTS', 'True').lower() == 'true'
ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'True').lower() == 'true'

# Legal/Compliance
PRIVACY_POLICY_URL = os.getenv('PRIVACY_POLICY_URL', '/privacy')
TERMS_OF_SERVICE_URL = os.getenv('TERMS_OF_SERVICE_URL', '/terms')
REFUND_POLICY_URL = os.getenv('REFUND_POLICY_URL', '/refund')

# Create required directories and ensure database compatibility
db_dir = os.path.dirname(DATABASE_PATH)
directories = [REPORTS_DIR, CACHE_DIR, LOGS_DIR, STATIC_DIR]
if db_dir:  # Only add if not empty string
    directories.append(db_dir)

for directory in directories:
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create directory {directory}: {e}")

# Database Migration Helper
def ensure_database_schema():
    """Ensure database has all required columns for premium features"""
    import sqlite3

    required_columns = [
        ('company', 'TEXT DEFAULT ""'),
        ('industry', 'TEXT DEFAULT ""'),
        ('audit_type', 'TEXT DEFAULT "free"'),
        ('payment_amount', 'REAL DEFAULT 0'),
        ('payment_status', 'TEXT DEFAULT "pending"'),
        ('stripe_session_id', 'TEXT DEFAULT ""'),
        ('overall_score', 'INTEGER DEFAULT 0'),
        ('business_impact_rating', 'TEXT DEFAULT ""'),
        ('estimated_monthly_revenue_loss', 'REAL DEFAULT 0'),
        ('annual_opportunity_cost', 'REAL DEFAULT 0'),
        ('implementation_complexity', 'TEXT DEFAULT ""'),
        ('expected_roi_timeline', 'TEXT DEFAULT ""'),
        ('technical_score', 'INTEGER DEFAULT 0'),
        ('content_score', 'INTEGER DEFAULT 0'),
        ('ai_readiness_score', 'INTEGER DEFAULT 0'),
        ('voice_search_score', 'INTEGER DEFAULT 0'),
        ('schema_markup_score', 'INTEGER DEFAULT 0'),
        ('competitive_position_score', 'INTEGER DEFAULT 0'),
        ('audit_data', 'TEXT'),
        ('pdf_report_path', 'TEXT DEFAULT ""'),
        ('email_sent', 'INTEGER DEFAULT 0'),  # Fixed: Use INTEGER instead of BOOLEAN
        ('email_sent_at', 'TIMESTAMP'),
        ('completed_at', 'TIMESTAMP'),
        ('customer_ip', 'TEXT DEFAULT ""'),
        ('user_agent', 'TEXT DEFAULT ""')
    ]

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Check if audits table exists first
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='audits'
        """)
        
        if not cursor.fetchone():
            # Create basic audits table if it doesn't exist
            cursor.execute("""
                CREATE TABLE audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created basic audits table")

        # Check existing columns and add missing ones
        cursor.execute("PRAGMA table_info(audits)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        for col_name, col_def in required_columns:
            if col_name not in existing_columns:
                try:
                    alter_stmt = f'ALTER TABLE audits ADD COLUMN {col_name} {col_def}'
                    cursor.execute(alter_stmt)
                    print(f"Added column: {col_name}")
                except Exception as e:
                    print(f"Warning: Could not add column {col_name}: {e}")

        conn.commit()
        conn.close()
        print("Database migration completed successfully")

    except Exception as e:
        print(f"Database migration error: {e}")
        # Don't fail app startup if migration fails

# Auto-migrate database on import (only run once per startup)
if not hasattr(ensure_database_schema, '_migration_run'):
    print("=== RUNNING DATABASE MIGRATION ===")
    try:
        ensure_database_schema()
        ensure_database_schema._migration_run = True
        print("=== MIGRATION COMPLETE ===")
    except Exception as e:
        print(f"Database migration error: {e}")
        print("=== MIGRATION FAILED ===")

# Validation
def validate_configuration():
    """Validate critical configuration settings"""
    errors = []

    # Check AI API keys
    if not OPENAI_API_KEY and not OPENROUTER_API_KEY:
        errors.append("Either OPENAI_API_KEY or OPENROUTER_API_KEY must be set")

    # Check Resend settings for email notifications
    if ENABLE_EMAIL_NOTIFICATIONS and not RESEND_API_KEY:
        errors.append("RESEND_API_KEY must be set for email notifications")

    # Check email domain configuration
    if ENABLE_EMAIL_NOTIFICATIONS and not FROM_EMAIL:
        errors.append("FROM_EMAIL must be set with a verified domain")

    # Check Stripe settings for premium audits
    if ENABLE_PREMIUM_AUDITS and ENABLE_STRIPE_PAYMENTS:
        if not STRIPE_SECRET_KEY:
            errors.append("STRIPE_SECRET_KEY must be set for premium audits")
        if not STRIPE_PUBLISHABLE_KEY:
            errors.append("STRIPE_PUBLISHABLE_KEY must be set for premium audits")

    # Check business settings
    if not SUPPORT_EMAIL:
        errors.append("SUPPORT_EMAIL should be set for customer support")

    return errors

# Configuration summary for debugging
def get_config_summary():
    """Get configuration summary (without sensitive data)"""
    return {
        'debug': DEBUG,
        'features': {
            'free_audits': ENABLE_FREE_AUDITS,
            'premium_audits': ENABLE_PREMIUM_AUDITS,
            'stripe_payments': ENABLE_STRIPE_PAYMENTS,
            'email_notifications': ENABLE_EMAIL_NOTIFICATIONS
        },
        'premium': {
            'price': PREMIUM_PRICE,
            'slots_per_month': PREMIUM_SLOTS_PER_MONTH,
            'delivery_hours': PREMIUM_DELIVERY_HOURS
        },
        'api_keys': {
            'openai_configured': bool(OPENAI_API_KEY),
            'openrouter_configured': bool(OPENROUTER_API_KEY),
            'stripe_configured': bool(STRIPE_SECRET_KEY),
            'resend_configured': bool(RESEND_API_KEY)
        },
        'email': {
            'service': 'Resend',
            'from_email': FROM_EMAIL,
            'from_name': FROM_NAME
        },
        'rate_limits': {
            'per_ip': RATE_LIMIT_PER_IP,
            'per_email': RATE_LIMIT_PER_EMAIL,
            'window_hours': RATE_LIMIT_WINDOW / 3600
        }
    }