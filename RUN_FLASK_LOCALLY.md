# 🚀 Run Flask App on Localhost

## Quick Start - Flask Application

### Easiest Method: Double-Click Batch File

1. **Double-click:** `run_flask.bat`
2. **Wait 5-10 seconds** for Flask to start
3. **Browser opens automatically** at http://localhost:5000

---

## Manual Method: PowerShell/Command Prompt

### Step 1: Open Terminal
1. **Right-click** in your project folder
2. Select **"Open in Terminal"** or **"Open PowerShell window here"**

### Step 2: Run Flask App
```powershell
python app.py
```

### Step 3: Open Browser
- Browser will open automatically at **http://localhost:5000**
- Or manually go to: **http://localhost:5000**

---

## First Time Setup

### 1. Install Dependencies
```powershell
pip install flask gspread google-auth google-auth-oauthlib google-auth-httplib2 python-dotenv reportlab Pillow openpyxl pandas
```

Or install from requirements.txt:
```powershell
pip install -r requirements.txt
```

### 2. Verify credentials.json
- Make sure `credentials.json` exists in project root
- Verify Google Sheet is shared with service account

### 3. Create .env file (if needed)
Create `.env` file in project root:
```
SECRET_KEY=your-secret-key-here
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec
```

---

## What You'll See

When Flask starts successfully:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

Then open: **http://localhost:5000**

---

## Login

- **First time:** Register a new admin account
- **Or use default:** `admin` / `admin123` (if exists)

---

## Troubleshooting

### "Module 'flask' not found"
**Solution:** Install Flask:
```powershell
pip install flask
```

### Port 5000 already in use
**Solution:** Change port in `app.py` or use:
```powershell
$env:PORT=5001; python app.py
```

### Database connection error
**Solution:**
- Check `credentials.json` exists
- Verify Google Sheet is shared
- Run: `python test_connection.py`

---

## Stop the App

Press `Ctrl+C` in the terminal where Flask is running.

---

## Quick Reference

**Start Flask:**
```powershell
python app.py
```

**URL:** http://localhost:5000

**Default Port:** 5000

---

**That's it! Your Flask app should be running on http://localhost:5000** 🎉

