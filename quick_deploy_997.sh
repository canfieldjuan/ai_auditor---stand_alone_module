#!/bin/bash
# File: quick_deploy_997.sh
# Quick implementation script for $997 premium audit model

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Check if running with proper permissions
check_permissions() {
    if [ ! -w . ]; then
        error "No write permission in current directory. Please run from your project directory."
    fi
}

# Create directory structure
create_directories() {
    log "📁 Creating directory structure..."
    
    directories=(
        "reports" "cache" "logs" "static" "data"
        "config" "models" "services" "routes" "utils" "tests"
        "deploy"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        info "Created: $dir/"
    done
    
    # Create __init__.py files
    packages=("config" "models" "services" "routes" "utils" "tests")
    for package in "${packages[@]}"; do
        touch "$package/__init__.py"
        info "Created: $package/__init__.py"
    done
}

# Setup virtual environment
setup_venv() {
    log "🐍 Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        info "Virtual environment created"
    else
        warn "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    info "pip upgraded"
}

# Install dependencies
install_dependencies() {
    log "📦 Installing dependencies..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt not found. Please ensure all files are in place."
    fi
    
    pip install -r requirements.txt
    info "Dependencies installed successfully"
}

# Setup environment configuration
setup_environment() {
    log "⚙️ Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            warn ".env file created from template"
            warn "IMPORTANT: Update .env with your actual API keys and settings!"
        else
            error ".env.example not found. Cannot create .env file."
        fi
    else
        info ".env file already exists"
    fi
}

# Validate critical settings
validate_configuration() {
    log "🔍 Validating configuration..."
    
    if [ -f ".env" ]; then
        source .env 2>/dev/null || warn "Could not source .env file"
        
        # Check critical settings
        missing_configs=()
        
        if [ -z "${OPENAI_API_KEY:-}" ] && [ -z "${OPENROUTER_API_KEY:-}" ]; then
            missing_configs+=("AI API key (OPENAI_API_KEY or OPENROUTER_API_KEY)")
        fi
        
        if [ -z "${STRIPE_SECRET_KEY:-}" ]; then
            missing_configs+=("STRIPE_SECRET_KEY")
        fi
        
        if [ -z "${EMAIL_USER:-}" ] || [ -z "${EMAIL_PASS:-}" ]; then
            missing_configs+=("Email settings (EMAIL_USER and EMAIL_PASS)")
        fi
        
        if [ -z "${SECRET_KEY:-}" ] || [ "${SECRET_KEY:-}" = "your-secret-key-here-change-in-production" ]; then
            missing_configs+=("SECRET_KEY (must be changed from default)")
        fi
        
        if [ ${#missing_configs[@]} -gt 0 ]; then
            warn "Missing critical configuration:"
            for config in "${missing_configs[@]}"; do
                warn "  - $config"
            done
            warn "Please update .env file before running the application"
        else
            info "✅ All critical configurations appear to be set"
        fi
    fi
}

# Initialize database
init_database() {
    log "🗄️ Initializing database..."
    
    python3 -c "
from models.database import init_database
try:
    init_database()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
    exit(1)
    " || error "Database initialization failed"
}

# Run tests
run_tests() {
    log "🧪 Running tests..."
    
    if [ -f "tests/test_api.py" ]; then
        python3 -m pytest tests/ -v --tb=short || warn "Some tests failed"
    else
        warn "Test files not found - skipping tests"
    fi
}

# Create necessary files if missing
create_missing_files() {
    log "📄 Creating missing configuration files..."
    
    # Create simple app.py if missing
    if [ ! -f "app.py" ]; then
        cat > app.py << 'EOF'
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Create necessary directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('cache', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    @app.route('/')
    def index():
        if os.path.exists('static/landing.html'):
            return send_from_directory('static', 'landing.html')
        elif os.path.exists('static/index.html'):
            return send_from_directory('static', 'index.html')
        else:
            return "Welcome to Premium AI SEO Audit! Please add your landing page to static/landing.html"

    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'version': '3.0.0'})
    
    @app.route('/api/test')
    def test_api():
        return jsonify({'message': 'API is working!', 'premium_model': True})

    # Register API routes
    try:
        from routes.api_routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        print("✓ API routes registered successfully")
    except Exception as e:
        print(f"✗ Failed to register API routes: {e}")
    
    # Initialize database
    try:
        from models.database import init_database
        init_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
    
    # Setup logging
    try:
        from utils.logging_config import setup_logging
        setup_logging(app)
        print("✓ Logging configured successfully")
    except Exception as e:
        print(f"✗ Failed to setup logging: {e}")
    
    return app

if __name__ == '__main__':
    print("Starting Premium AI SEO Audit application...")
    app = create_app()
    print("\nApplication running on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF
        info "Created app.py"
    fi
    
    # Create simple run script
    if [ ! -f "run.py" ]; then
        cat > run.py << 'EOF'
#!/usr/bin/env python3
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
EOF
        chmod +x run.py
        info "Created run.py"
    fi
}

# Setup legal pages
setup_legal_pages() {
    log "⚖️ Setting up legal pages..."
    
    # Create static files for legal pages (simplified versions)
    if [ ! -f "static/terms.html" ]; then
        echo "<!DOCTYPE html><html><head><title>Terms of Service</title></head><body><h1>Terms of Service</h1><p>Coming soon...</p></body></html>" > static/terms.html
        info "Created basic static/terms.html"
    fi
    
    if [ ! -f "static/privacy.html" ]; then
        echo "<!DOCTYPE html><html><head><title>Privacy Policy</title></head><body><h1>Privacy Policy</h1><p>Coming soon...</p></body></html>" > static/privacy.html
        info "Created basic static/privacy.html"
    fi
    
    if [ ! -f "static/refund.html" ]; then
        echo "<!DOCTYPE html><html><head><title>Refund Policy</title></head><body><h1>Refund Policy</h1><p>30-day money-back guarantee. Contact support@yourdomain.com</p></body></html>" > static/refund.html
        info "Created basic static/refund.html"
    fi
}

# Generate summary report
generate_summary() {
    log "📊 Generating implementation summary..."
    
    cat << EOF

${GREEN}========================================${NC}
${GREEN}  PREMIUM AI SEO AUDIT IMPLEMENTATION  ${NC}
${GREEN}========================================${NC}

${BLUE}✅ COMPLETED SETUP:${NC}
• Directory structure created
• Virtual environment configured
• Dependencies installed
• Database initialized
• Configuration files created
• Legal pages prepared

${YELLOW}⚠️  REQUIRED NEXT STEPS:${NC}

1. ${YELLOW}UPDATE .env FILE:${NC}
   Edit .env with your actual API keys:
   - OPENAI_API_KEY or OPENROUTER_API_KEY
   - STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY
   - EMAIL_USER and EMAIL_PASS
   - Change SECRET_KEY from default

2. ${YELLOW}ADD YOUR CONTENT:${NC}
   - Update static/landing.html with your premium landing page
   - Update legal pages (static/terms.html, static/privacy.html, static/refund.html)
   - Add your company branding and contact information

3. ${YELLOW}CONFIGURE STRIPE:${NC}
   - Set up Stripe account at https://stripe.com
   - Add webhook endpoint for payment processing
   - Test payment flow with test keys first

4. ${YELLOW}EMAIL SETUP:${NC}
   - Configure Gmail app password OR custom SMTP
   - Test email delivery

${BLUE}🚀 TO START THE APPLICATION:${NC}

Development:
${GREEN}source venv/bin/activate${NC}
${GREEN}python app.py${NC}

Production:
${GREEN}source venv/bin/activate${NC}
${GREEN}python run_production.py${NC}

${BLUE}🌐 APPLICATION ENDPOINTS:${NC}
• Landing Page: http://localhost:5000/
• Free Audit: http://localhost:5000/api/audit
• Health Check: http://localhost:5000/health
• Legal Pages: http://localhost:5000/static/terms.html

${BLUE}💰 BUSINESS MODEL READY:${NC}
• Premium Audit: \$997 one-time payment
• Comprehensive 25+ page reports
• AI-powered analysis
• 30-day money-back guarantee
• Stripe payment processing

${YELLOW}📋 VALIDATION CHECKLIST:${NC}
□ .env file updated with real API keys
□ Stripe account configured
□ Email delivery tested
□ Landing page customized
□ Legal pages updated
□ Payment flow tested
□ First premium audit delivered

${GREEN}🎯 REVENUE TARGETS:${NC}
Conservative: 10 audits/month = \$9,970/month
Realistic: 25 audits/month = \$24,925/month
Optimistic: 50 audits/month = \$49,850/month

${BLUE}📞 NEED HELP?${NC}
Check logs in: logs/seo_auditor.log
Test with: curl http://localhost:5000/health

${GREEN}Ready to start generating revenue with premium AI SEO audits!${NC}

EOF
}

# Main deployment function
main() {
    log "🚀 Starting Premium AI SEO Audit implementation..."
    
    check_permissions
    create_directories
    setup_venv
    install_dependencies
    create_missing_files
    setup_environment
    setup_legal_pages
    init_database
    validate_configuration
    run_tests
    
    log "🎉 Implementation completed successfully!"
    generate_summary
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "venv")
        log "Setting up virtual environment only..."
        setup_venv
        ;;
    "deps")
        log "Installing dependencies only..."
        setup_venv
        install_dependencies
        ;;
    "db")
        log "Initializing database only..."
        setup_venv
        init_database
        ;;
    "test")
        log "Running tests only..."
        setup_venv
        run_tests
        ;;
    "validate")
        log "Validating configuration only..."
        validate_configuration
        ;;
    *)
        echo "Usage: $0 [deploy|venv|deps|db|test|validate]"
        echo ""
        echo "Commands:"
        echo "  deploy   - Full deployment (default)"
        echo "  venv     - Setup virtual environment only"
        echo "  deps     - Install dependencies only"
        echo "  db       - Initialize database only"
        echo "  test     - Run tests only"
        echo "  validate - Validate configuration only"
        exit 1
        ;;
esac