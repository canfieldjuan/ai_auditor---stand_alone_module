# app.py
# Main Flask application file - handles all API endpoints and serves the frontend

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import stripe
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Stripe keys from environment
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

if not STRIPE_SECRET_KEY or not STRIPE_PUBLISHABLE_KEY:
    print("⚠️  WARNING: Stripe keys not found in .env file")
    print("Please create a .env file with STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY")

stripe.api_key = STRIPE_SECRET_KEY

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Create necessary directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('cache', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Basic routes
    @app.route('/')
    def index():
        # Serve the index_997.html file
        if os.path.exists('static/index_997.html'):
            return send_from_directory('static', 'index_997.html')
        else:
            return "Index.html not found in static directory", 404

    @app.route('/landing')
    def landing():
        return send_from_directory('static', 'landing.html')

    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'version': '2.0.0'})
    
    @app.route('/api/test')
    def test_api():
        return jsonify({'message': 'API is working!'})

    # API endpoint to get Stripe configuration
    @app.route('/api/config')
    def get_config():
        return jsonify({
            'stripePublishableKey': STRIPE_PUBLISHABLE_KEY
        })

    # API endpoint to create payment intent
    @app.route('/api/create-payment-intent', methods=['POST'])
    def create_payment_intent():
        try:
            data = request.get_json()
            
            # Create a PaymentIntent with Stripe
            intent = stripe.PaymentIntent.create(
                amount=data.get('amount', 99700),  # $997 in cents
                currency='usd',
                metadata={
                    'website': data.get('website', ''),
                    'email': data.get('email', ''),
                    'company': data.get('company', '')
                }
            )
            
            return jsonify({
                'clientSecret': intent.client_secret
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # API endpoint to activate license after payment
    @app.route('/api/activate-license', methods=['POST'])
    def activate_license():
        try:
            data = request.get_json()
            payment_intent_id = data.get('paymentIntentId')
            
            # Verify the payment with Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if payment_intent.status == 'succeeded':
                # Here you would:
                # 1. Create user account in your database
                # 2. Send welcome email with credentials
                # 3. Set up their white-label access
                
                # For now, we'll just return success
                print(f"License activated for: {data.get('email')}")
                print(f"Company: {data.get('company')}")
                print(f"Website: {data.get('website')}")
                
                return jsonify({
                    'success': True,
                    'message': 'License activated successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Payment not completed'
                }), 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # API endpoint for test audit
    @app.route('/api/test-audit', methods=['POST'])
    def test_audit():
        try:
            data = request.get_json()
            url = data.get('url')
            email = data.get('email')
            
            # Here you would run your actual AI SEO audit logic
            # For now, we'll return demo data
            
            # Simulate some processing
            import time
            time.sleep(1)  # Remove this in production
            
            # Demo audit results
            audit_results = {
                'visibilityScore': 23,
                'aiOverviewScore': 12,
                'chatgptScore': 0,
                'competitors': [
                    {'name': 'Competitor A', 'score': 78, 'advantage': 'Appears in 6x more AI results'},
                    {'name': 'Competitor B', 'score': 65, 'advantage': 'Dominates voice search queries'},
                    {'name': 'Competitor C', 'score': 54, 'advantage': 'Better semantic structure'},
                    {'name': 'Competitor D', 'score': 47, 'advantage': 'More featured snippets'},
                    {'name': 'Your Website', 'score': 23, 'advantage': '--'}
                ],
                'revenueImpact': {
                    'month1': {'current': -12000, 'optimized': 32000},
                    'month3': {'current': -45000, 'optimized': 156000},
                    'month12': {'current': -240000, 'optimized': 1248000}
                },
                'issues': [
                    {
                        'title': 'Missing Structured Data',
                        'description': '87% of pages lack essential schema markup for AI understanding',
                        'impact': 'high'
                    },
                    {
                        'title': 'Poor Content Structure',
                        'description': 'Content not optimized for featured snippet extraction',
                        'impact': 'high'
                    },
                    {
                        'title': 'No Semantic HTML',
                        'description': 'Missing semantic elements that help AI parse content',
                        'impact': 'medium'
                    },
                    {
                        'title': 'Weak Entity Associations',
                        'description': 'Google Knowledge Graph has limited understanding of your business',
                        'impact': 'medium'
                    }
                ],
                'emailSent': True
            }
            
            # In production, you would:
            # 1. Run actual SEO audit on the URL
            # 2. Generate PDF report
            # 3. Send email with report attached
            
            print(f"Test audit requested for: {url}")
            print(f"Report will be sent to: {email}")
            
            return jsonify(audit_results)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # Try to import and register the API blueprint
    api_error = None
    try:
        from routes.api_routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        print("✓ API routes registered successfully")
    except Exception as e:
        api_error = str(e)
        print(f"✗ Failed to register API routes: {e}")
        
        # Fallback audit endpoint already handled above
    
    # Try to initialize database
    try:
        from models.database import init_database
        init_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
    
    # Try to setup logging
    try:
        from utils.logging_config import setup_logging
        setup_logging(app)
        print("✓ Logging configured successfully")
    except Exception as e:
        print(f"✗ Failed to setup logging: {e}")
    
    print(f"\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule}")
    
    return app

if __name__ == '__main__':
    print("Starting Flask application...")
    app = create_app()
    print("\nFlask is running on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)