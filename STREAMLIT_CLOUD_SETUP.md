# 🚀 Streamlit Cloud Deployment Guide

## ✅ All Files Pushed to GitHub

Your complete Asset Management System has been pushed to:
**https://github.com/tonycharles1/Trackz**

## 📦 Included Files

### ✅ Streamlit Application
- `app_streamlit.py` - Main Streamlit app with embedded CSS
- `pages/` - All 13 page modules including:
  - `assets.py` - Asset management with **barcode generation**
  - `dashboard.py` - Dashboard with metrics
  - `asset_movements.py` - Movement tracking
  - `depreciation.py` - Depreciation calculations
  - And 9 more pages...

### ✅ Templates & CSS
- `templates/` - All 21 HTML templates including:
  - `base.html` - Base template with embedded CSS
  - `barcode_print.html` - Barcode printing template
  - `barcode_preview.html` - Barcode preview template
  - All other templates with embedded CSS

### ✅ Configuration Files
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml.example` - Example secrets file
- `requirements.txt` - All dependencies (Streamlit, barcode, etc.)
- `runtime.txt` - Python version (3.11)

### ✅ Supporting Files
- `google_sheets_db.py` - Database connection
- `config.py` - Configuration
- `setup_database.py` - Database setup script
- All helper scripts and documentation

## 🎨 CSS & Styling

**CSS is embedded in:**
1. `app_streamlit.py` - Custom Streamlit CSS (lines 29-79)
2. `templates/base.html` - Flask template CSS (embedded in HTML)

**No separate CSS files needed** - everything is included!

## 📊 Barcode Functionality

**Barcode features are in:**
- `pages/assets.py` - Barcode generation and PDF printing
- Uses `reportlab` for PDF generation
- Uses `python-barcode` (optional, graceful fallback if not available)

## 🌐 Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io**
2. Sign in with your GitHub account

### Step 2: Create New App
1. Click **"New app"**
2. Select repository: **`tonycharles1/Trackz`**
3. Branch: **`master`**
4. Main file: **`app_streamlit.py`**

### Step 3: Add Secrets
1. Click **"Advanced settings"**
2. Click **"Secrets"**
3. Add your Google Sheets credentials:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "your-private-key-id"
private_key = """-----BEGIN PRIVATE KEY-----
your-private-key-here
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/asset-database%40asset-database-477316.iam.gserviceaccount.com"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

### Step 4: Deploy
1. Click **"Deploy!"**
2. Wait for deployment (2-5 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

## ✅ Pre-Deployment Checklist

- [x] All Python files pushed
- [x] All pages pushed
- [x] All templates pushed (with embedded CSS)
- [x] Streamlit config pushed
- [x] Requirements.txt includes all dependencies
- [x] Runtime.txt specified
- [x] Barcode functionality included
- [x] CSS embedded in code

## 🔧 After Deployment

1. **Share Google Sheet** with service account email:
   - `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Give it **Editor** access

2. **Test the app:**
   - Register first user (becomes admin)
   - Test asset creation
   - Test barcode printing
   - Verify all pages load correctly

## 📝 Notes

- **CSS**: All CSS is embedded in `app_streamlit.py` and templates - no separate files needed
- **Barcode**: Works with `reportlab` (included in requirements.txt)
- **Secrets**: Never commit `.streamlit/secrets.toml` - add via Streamlit Cloud UI only
- **Uploads**: Upload folder is excluded from git (handled by Streamlit Cloud)

## 🎉 Ready to Deploy!

Your repository is complete and ready for Streamlit Cloud deployment!

**Repository:** https://github.com/tonycharles1/Trackz  
**Main File:** `app_streamlit.py`  
**Branch:** `master`

