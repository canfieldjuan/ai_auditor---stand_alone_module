# DEVELOPMENT NOTES - Important Package Version Issues

## ❌ **CRITICAL: Resend Package Version Error**

**Date**: December 2024
**Issue**: resend==0.6.1 does not exist
**Error**: `ERROR: Could not find a version that satisfies the requirement resend==0.6.1`

### Available Resend Versions:
- 0.1.0, 0.1.1, 0.2.0, 0.3.0, 0.4.0, 0.5.1, 0.5.2
- **0.6.0** ✅ (exists)
- **0.6.1** ❌ (DOES NOT EXIST - never use this)
- 0.7.0, 0.7.1, 0.7.2, 0.8.0
- 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.2.0
- 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.1, 2.6.0, 2.7.0, 2.8.0
- **2.10.0** ✅ (latest stable - use this)

### ✅ **CORRECT USAGE:**
```
resend==2.10.0  # Current latest
resend>=2.0.0   # Any recent version
```

### ❌ **NEVER USE:**
```
resend==0.6.1   # This version does not exist!
```

## 📝 **Other Package Version Notes**

### OpenAI Package:
- **0.28.1**: Legacy API style (`openai.ChatCompletion.create`)
- **1.x+**: New API style (`client.chat.completions.create`)
- Current project uses: **0.28.1** (legacy style)

### Stripe Package:
- **7.8.0**: Working version in project
- Generally stable across versions

## 🔧 **Installation Commands That Work**

```bash
# Individual packages (if requirements.txt fails)
pip install resend==2.10.0
pip install openai==0.28.1
pip install stripe==7.8.0
pip install Flask==2.3.3 Flask-CORS==4.0.0
pip install requests==2.31.0 beautifulsoup4==4.12.2
pip install reportlab==4.0.4 python-dotenv==1.0.0

# Or get latest resend
pip install resend  # Gets latest version automatically
```

## 🚨 **Lesson Learned**
Always verify package versions exist before specifying them in requirements.txt. Use:
```bash
pip index versions resend  # Check available versions
```

---
**Note**: Keep this file updated with any other version conflicts discovered during development.
