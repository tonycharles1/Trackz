# How to Start Your Streamlit App

## Quick Start

1. **Open PowerShell** in your project folder:
   ```
   C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System
   ```

2. **Run Streamlit:**
   ```powershell
   streamlit run app_streamlit.py
   ```

3. **Open your browser:**
   - Streamlit will automatically open: http://localhost:8501
   - Or manually go to: http://localhost:8501

## If You See "localhost refused to connect"

### Problem 1: Streamlit isn't running
**Solution:** Make sure you ran `streamlit run app_streamlit.py` in PowerShell

### Problem 2: Port 8501 is already in use
**Solution:** Use a different port:
```powershell
streamlit run app_streamlit.py --server.port 8502
```

### Problem 3: Database connection error on startup
**Solution:** The app will still start, but you'll see an error message. Follow these steps:

1. **Fix credentials** (see steps below)
2. **Refresh the browser** (F5 or click refresh button)

## Fix Database Connection First

Before starting Streamlit, it's recommended to fix the credentials:

### Step 1: Test Your Credentials
```powershell
python test_jwt_signature.py
```

This will tell you if your credentials are valid.

### Step 2: If Credentials Are Invalid

1. **Download new credentials:**
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316
   - Click on: `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Go to "Keys" tab → "Add Key" → "Create new key" → Select "JSON"
   - Download the file

2. **Replace credentials.json:**
   - Rename downloaded file to `credentials.json`
   - Place in project root folder

3. **Regenerate secrets.toml:**
   ```powershell
   python create_secrets_toml.py
   ```

4. **Share Google Sheet:**
   - Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
   - Share with: `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Set permission to "Editor"

### Step 3: Start Streamlit Again
```powershell
streamlit run app_streamlit.py
```

## Troubleshooting

### Check if Streamlit is installed:
```powershell
pip install streamlit
```

### Check if all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### View Streamlit logs:
The terminal where you ran `streamlit run` will show error messages. Look for:
- Database connection errors
- Import errors
- Missing file errors

## Default Login

Once the app is running:
- **Username:** admin
- **Password:** admin123

(Change this after first login!)

## Stopping Streamlit

Press `Ctrl+C` in the PowerShell window where Streamlit is running.

