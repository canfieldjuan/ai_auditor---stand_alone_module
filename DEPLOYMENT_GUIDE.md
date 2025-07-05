# 🚀 DEPLOYMENT GUIDE: Integrating App.py with Services

## 📋 **Current Status**
- ✅ **Backup Created**: Original app.py saved to `app_backup_original.py`
- ✅ **Test Version Ready**: `app_integrated_test.py` created with full integration
- ✅ **Test Suite Available**: `test_integration.py` for validation
- ✅ **Environment File Exists**: `.env` file found

## 🔧 **Pre-Deployment Checklist**

### 1. Environment Variables (Check your .env file)
Your `.env` file should contain:

```bash
# OpenAI Configuration (Required for AI analysis)
OPENAI_API_KEY=sk-...your-openai-key...

# OR OpenRouter as fallback
OPENROUTER_API_KEY=sk-...your-openrouter-key...

# Stripe Configuration (Already working)
STRIPE_SECRET_KEY=sk_...your-stripe-secret...
STRIPE_PUBLISHABLE_KEY=pk_...your-stripe-publishable...

# Email Configuration (Required for sending reports)
RESEND_API_KEY=re_...your-resend-api-key...
FROM_EMAIL=noreply@yourdomain.com
FROM_NAME=AI SEO Auditor

# Optional: Legacy email fallback
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### 2. Required Dependencies
Ensure these are in your requirements.txt and installed:
- openai (for AI analysis)
- resend (for email delivery)
- reportlab (for PDF generation)
- beautifulsoup4 (for web scraping)
- stripe (already working)

## 🧪 **Testing Phase (Do This First!)**

### Step 1: Test the Integration
```bash
# Run the test suite to check everything
python test_integration.py
```

### Step 2: Test the Integrated App
```bash
# Run the integrated app on port 5001 (different from your main app)
python app_integrated_test.py
```

Then test in browser:
- http://localhost:5001/ (should show your landing page)
- http://localhost:5001/health (should show service status)
- Try the test audit button on the landing page

### Step 3: Compare Results
1. **Current app** (port 5000): Returns demo data
2. **Integrated app** (port 5001): Should return real analysis if APIs configured

## 🚀 **Deployment Options**

### Option 1: Gradual Deployment (Recommended)
Only replace the test-audit endpoint first:

```python
# In your current app.py, replace the test_audit function with:
@app.route('/api/test-audit', methods=['POST'])
def test_audit():
    try:
        data = request.get_json()
        url = data.get('url')
        email = data.get('email')
        
        # Try real audit first
        try:
            from services.seo_auditor import SEOAuditor
            auditor = SEOAuditor()
            result = auditor.run_full_audit(url, email)
            
            if result.get('success'):
                # Convert to frontend format and return
                return jsonify({
                    'visibilityScore': result.get('score', 70),
                    'aiOverviewScore': result.get('categories', {}).get('ai_readiness', 45),
                    'chatgptScore': result.get('categories', {}).get('ai_readiness', 0),
                    # ... rest of conversion
                })
        except:
            pass  # Fall back to demo data
        
        # Original demo data as fallback
        # ... (keep existing demo code)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

### Option 2: Full Deployment
Replace entire app.py:

```bash
# Backup current (already done)
cp app.py app_backup_current.py

# Deploy integrated version
cp app_integrated_test.py app.py

# Update the port back to 5000 in the new app.py
# Change: app.run(debug=True, host='0.0.0.0', port=5001)
# To:     app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🔍 **What Changes**

### Before Integration:
- `/api/test-audit` returns hardcoded demo data
- No real AI analysis
- No actual email delivery
- No PDF report generation

### After Integration:
- `/api/test-audit` runs real AI analysis on websites
- Generates actual business impact calculations
- Sends professional email reports with PDF attachments
- Falls back to demo data if services unavailable

## 🛡️ **Safety Features Built In**

1. **Graceful Degradation**: If AI APIs fail, falls back to demo data
2. **Service Validation**: Checks if each service is available before using
3. **Error Handling**: Comprehensive try/catch blocks
4. **Backup Plan**: Original functionality preserved as fallback

## 📊 **Expected Results**

### With Proper API Keys:
- **Real website analysis** using OpenAI or OpenRouter
- **Actual PDF reports** (25+ pages)
- **Professional emails** sent via Resend
- **Business impact calculations** based on real data

### Without API Keys:
- **Demo data** (same as current)
- **No emails sent** (graceful failure)
- **All payment functionality** still works perfectly

## ⚠️ **Rollback Plan**

If anything goes wrong:

```bash
# Immediate rollback
cp app_backup_original.py app.py

# Restart your server
python app.py
```

## 🎯 **Recommended Deployment Sequence**

1. **Test**: Run `python test_integration.py`
2. **Configure**: Add missing API keys to `.env`
3. **Test Integration**: Run `python app_integrated_test.py`
4. **Validate**: Test the audit functionality manually
5. **Deploy**: Replace app.py when satisfied
6. **Monitor**: Watch logs for any issues

## 💡 **Pro Tips**

- Start with OpenRouter API (easier to get) if you don't have OpenAI
- Resend API is free for 3,000 emails/month
- Keep demo data as fallback for reliability
- Monitor logs to see which services are working

Would you like me to help you run through any of these steps?
