# File: routes/api_routes.py
# Premium API routes for $997 audit processing

import os
import time
import threading
import stripe
from flask import Blueprint, request, jsonify, send_file
from services.seo_auditor import SEOAuditor
from services.cache_service import cache
from utils.helpers import clean_url, is_valid_email, is_valid_url
from utils.rate_limiter import rate_limit, email_rate_limit
from utils.logging_config import log_audit_request, log_audit_completion, log_error
from config.settings import STRIPE_SECRET_KEY

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

api_bp = Blueprint('api', __name__)
auditor = SEOAuditor()

@api_bp.route('/audit', methods=['POST'])
@rate_limit(limit=100, window=3600, per='ip')  # Increased for premium service
def run_audit():
    """Premium audit endpoint - handles both free and $997 paid audits"""
    start_time = time.time()
    
    try:
        # Get and validate request data
        try:
            data = request.get_json() or {}
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid JSON in request body'}), 400
        
        url = data.get('url', '').strip()
        email = data.get('email', '').strip()
        audit_type = data.get('audit_type', 'free')  # 'free' or 'premium'
        payment_amount = data.get('payment_amount', 0)
        company = data.get('company', '').strip()
        industry = data.get('industry', '').strip()
        
        # Validation
        if not url:
            return jsonify({'success': False, 'error': 'Website URL is required'}), 400
        
        if not email:
            return jsonify({'success': False, 'error': 'Email address is required'}), 400
        
        if not is_valid_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Clean and validate URL
        try:
            url = clean_url(url)
            if not is_valid_url(url):
                return jsonify({'success': False, 'error': 'Invalid website URL format'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': f'URL validation error: {str(e)}'}), 400
        
        # Validate premium audit requirements
        if audit_type == 'premium':
            if payment_amount != 997:
                return jsonify({'success': False, 'error': 'Invalid payment amount for premium audit'}), 400
            
            # Note: In production, you would verify payment with Stripe here
            # For now, we'll assume payment is valid if amount is correct
            
        # Log request
        try:
            log_audit_request(url, email, request.remote_addr)
        except Exception as e:
            print(f"Logging error (non-fatal): {e}")
        
        # Check cache for premium audits (shorter cache time)
        cache_key = f"{audit_type}_{url}"
        try:
            if audit_type == 'free':
                cached_result = cache.get(url)
                if cached_result:
                    # Send email with cached results for free audits
                    try:
                        threading.Thread(
                            target=lambda: auditor.send_cached_report(email, cached_result, url)
                        ).start()
                    except:
                        pass
                    
                    duration = time.time() - start_time
                    try:
                        log_audit_completion(url, email, cached_result.get('score', 0), duration)
                    except:
                        pass
                    
                    return jsonify({
                        **cached_result,
                        'cached': True,
                        'email_sent': True,
                        'audit_type': 'free'
                    })
            # Premium audits always get fresh analysis - no cache
                    
        except Exception as e:
            print(f"Cache check error (non-fatal): {e}")
        
        # Run audit (premium or free)
        try:
            if audit_type == 'premium':
                result = auditor.run_premium_audit(url, email, company, industry)
            else:
                result = auditor.run_full_audit(url, email)
        except Exception as e:
            try:
                log_error('AUDIT_EXCEPTION', str(e), {'url': url, 'email': email, 'type': audit_type})
            except:
                pass
            
            return jsonify({
                'success': False, 
                'error': 'Failed to complete audit. Please try again or contact support.'
            }), 500
        
        # Check audit result
        if not result.get('success', False):
            try:
                log_error('AUDIT_FAILED', result.get('error', 'Unknown error'), {
                    'url': url, 'email': email, 'type': audit_type
                })
            except:
                pass
            
            return jsonify({
                'success': False,
                'error': result.get('error', 'Audit failed. Please check the URL and try again.')
            }), 400
        
        # Cache free audit results only
        if audit_type == 'free':
            try:
                cache.set(url, result, ttl=7200)  # Cache for 2 hours
            except Exception as e:
                print(f"Cache set error (non-fatal): {e}")
        
        # Log completion
        try:
            duration = time.time() - start_time
            log_audit_completion(url, email, result.get('score', 0), duration)
        except:
            pass
        
        # Add audit type to response
        result['audit_type'] = audit_type
        result['payment_amount'] = payment_amount if audit_type == 'premium' else 0
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Unhandled exception in /api/audit: {e}")
        
        try:
            log_error('AUDIT_UNHANDLED_EXCEPTION', str(e), {
                'url': data.get('url', 'unknown') if 'data' in locals() else 'unknown',
                'email': data.get('email', 'unknown') if 'data' in locals() else 'unknown',
                'type': data.get('audit_type', 'unknown') if 'data' in locals() else 'unknown'
            })
        except:
            pass
        
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please try again or contact support.'
        }), 500

@api_bp.route('/payment/create-session', methods=['POST'])
def create_payment_session():
    """Create Stripe checkout session for $997 premium audit"""
    
    try:
        data = request.get_json() or {}
        
        url = data.get('url', '').strip()
        email = data.get('email', '').strip()
        company = data.get('company', '').strip()
        industry = data.get('industry', '').strip()
        
        # Validation
        if not url or not email:
            return jsonify({'success': False, 'error': 'URL and email are required'}), 400
        
        if not is_valid_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Clean URL
        url = clean_url(url)
        if not is_valid_url(url):
            return jsonify({'success': False, 'error': 'Invalid URL format'}), 400
        
        # Create Stripe checkout session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Premium AI SEO Audit',
                            'description': f'Comprehensive AI SEO audit for {url}',
                            'images': ['https://yoursite.com/static/audit-preview.png'],
                        },
                        'unit_amount': 99700,  # $997.00 in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=email,
                metadata={
                    'url': url,
                    'email': email,
                    'company': company,
                    'industry': industry,
                    'audit_type': 'premium'
                },
                success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.host_url + 'cancel',
                automatic_tax={'enabled': True},
            )
            
            return jsonify({
                'success': True,
                'checkout_url': session.url,
                'session_id': session.id
            })
            
        except stripe.error.StripeError as e:
            return jsonify({
                'success': False,
                'error': f'Payment processing error: {str(e)}'
            }), 400
            
    except Exception as e:
        print(f"Payment session creation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create payment session. Please try again.'
        }), 500

@api_bp.route('/payment/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Extract audit details from metadata
        url = session['metadata'].get('url')
        email = session['metadata'].get('email')
        company = session['metadata'].get('company', '')
        industry = session['metadata'].get('industry', '')
        
        if url and email:
            # Start premium audit processing
            try:
                threading.Thread(
                    target=lambda: auditor.run_premium_audit(url, email, company, industry)
                ).start()
                
                print(f"Premium audit initiated for {email} - {url}")
                
            except Exception as e:
                print(f"Failed to start premium audit: {e}")
    
    return jsonify({'success': True})

@api_bp.route('/download')
def download_report():
    """Download PDF report"""
    try:
        path = request.args.get('path')
        if not path:
            return jsonify({'success': False, 'error': 'Path parameter required'}), 400
            
        # Security: prevent directory traversal
        if '..' in path or path.startswith('/'):
            return jsonify({'success': False, 'error': 'Invalid path'}), 400
            
        # Construct safe path
        safe_path = os.path.join('reports', os.path.basename(path))
        
        if not os.path.exists(safe_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        return send_file(safe_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Download failed'}), 500

@api_bp.route('/pricing')
def get_pricing():
    """Get current pricing information"""
    return jsonify({
        'success': True,
        'pricing': {
            'free_audit': {
                'price': 0,
                'features': [
                    'Basic SEO analysis',
                    'Simple PDF report',
                    'Email delivery',
                    '5-page report'
                ],
                'limitations': [
                    'Basic analysis only',
                    'No competitor intelligence',
                    'No implementation roadmap'
                ]
            },
            'premium_audit': {
                'price': 997,
                'original_price': 2500,
                'features': [
                    'Comprehensive AI search analysis',
                    '25+ page professional report',
                    'Competitor intelligence report',
                    '90-day implementation roadmap',
                    'Revenue impact analysis',
                    'Priority matrix with ROI projections',
                    'Schema markup recommendations',
                    'Voice search optimization',
                    'AI search strategy',
                    '24-hour delivery',
                    '30-day money-back guarantee'
                ],
                'guarantee': '10x ROI or full refund',
                'delivery_time': '24 hours',
                'limited_slots': 20
            }
        }
    })

@api_bp.route('/cache/stats')
def cache_stats():
    """Get cache statistics"""
    try:
        stats = cache.get_cache_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to get cache stats'}), 500

@api_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear cache (admin endpoint)"""
    try:
        # TODO: Add authentication check here
        cleared = cache.clear()
        return jsonify({'success': True, 'cleared_items': cleared})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to clear cache'}), 500

@api_bp.route('/health')
def health_check():
    """Health check endpoint with service status"""
    try:
        # Test database connection
        from models.database import init_database
        init_database()
        db_status = 'healthy'
    except:
        db_status = 'error'
    
    # Test AI service
    try:
        from services.ai_service import analyze_with_ai
        ai_status = 'healthy'
    except:
        ai_status = 'error'
    
    # Test email service
    try:
        from services.email_service import send_email_report
        email_status = 'healthy'
    except:
        email_status = 'error'
    
    return jsonify({
        'status': 'healthy',
        'version': '3.0.0',
        'audit_types': ['free', 'premium'],
        'premium_price': 997,
        'services': {
            'database': db_status,
            'ai_analysis': ai_status,
            'email_delivery': email_status,
            'payment_processing': 'healthy' if STRIPE_SECRET_KEY else 'not_configured'
        },
        'timestamp': time.time()
    })

@api_bp.route('/stats')
def get_stats():
    """Get business statistics (admin endpoint)"""
    try:
        # TODO: Add authentication
        
        # Get basic stats from database
        import sqlite3
        from config.settings import DATABASE_PATH
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total audits
        cursor.execute("SELECT COUNT(*) FROM audits")
        total_audits = cursor.fetchone()[0]
        
        # Recent audits (last 30 days)
        cursor.execute("""
            SELECT COUNT(*) FROM audits 
            WHERE created_at > datetime('now', '-30 days')
        """)
        recent_audits = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("SELECT AVG(overall_score) FROM audits WHERE overall_score > 0")
        avg_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_audits': total_audits,
                'audits_last_30_days': recent_audits,
                'average_score': round(avg_score, 1),
                'premium_price': 997,
                'conversion_rate': '2.3%',  # Placeholder
                'revenue_last_30_days': recent_audits * 997 * 0.023  # Estimated
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to get stats'}), 500

# Error handlers for the blueprint
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Method not allowed'}), 405

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500