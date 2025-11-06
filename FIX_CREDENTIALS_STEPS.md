# 🔧 Fix Credentials - Step by Step Guide

## Current Problem
Your Google Sheets credentials are invalid (Invalid JWT Signature error). This means you need to download a new service account key.

---

## Step 1: Download New Credentials from Google Cloud Console

### 1.1 Open Google Cloud Console
Click this link: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316

### 1.2 Find the Service Account
- Look for: `asset-database@asset-database-477316.iam.gserviceaccount.com`
- Click on it

### 1.3 Create a New Key
1. Click the **"Keys"** tab (at the top)
2. Click **"Add Key"** button
3. Select **"Create new key"**
4. Choose **"JSON"** format
5. Click **"Create"**
6. The file will download automatically (usually to your Downloads folder)

---

## Step 2: Replace credentials.json

### 2.1 Find the Downloaded File
- Check your **Downloads folder**
- The file will be named something like: `asset-database-477316-xxxxxxxxxxxx.json`

### 2.2 Copy to Project Folder
1. Open your project folder:
   ```
   C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System
   ```

2. **Copy** the downloaded JSON file to this folder

### 2.3 Rename the File
1. Right-click on the downloaded file
2. Select **"Rename"**
3. Change the name to exactly: `credentials.json`
4. **Important:** Make sure it's NOT `credentials.json.txt` - it must end with `.json` only
5. If a file named `credentials.json` already exists, choose **"Replace"** when prompted

---

## Step 3: Regenerate secrets.toml

### 3.1 Open PowerShell
1. Right-click in your project folder
2. Select **"Open in Terminal"** or **"Open PowerShell window here"**

### 3.2 Run the Conversion Script
Type this command and press Enter:
```powershell
python create_secrets_toml.py
```

You should see:
```
[SUCCESS] Successfully created .streamlit/secrets.toml
```

---

## Step 4: Verify Credentials Work

### 4.1 Test the Connection
Run this command:
```powershell
python test_jwt_signature.py
```

### 4.2 Check for Success
You should see:
- ✅ `[SUCCESS] JWT signature is VALID!`
- ✅ `[SUCCESS] Connected to Google Sheets successfully!`

If you still see errors, go back to Step 1 and make sure you downloaded a **NEW** key.

---

## Step 5: Share Google Sheet with Service Account

### 5.1 Open the Google Sheet
Click this link: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit

### 5.2 Share with Service Account
1. Click the **"Share"** button (top right)
2. In the "Add people and groups" box, paste this email:
   ```
   asset-database@asset-database-477316.iam.gserviceaccount.com
   ```
3. Set permission to **"Editor"**
4. **Uncheck** "Notify people" (service accounts don't need email notifications)
5. Click **"Share"**

### 5.3 Verify Sharing
- The service account email should appear in the sharing list
- Permission should show as "Editor"

---

## Step 6: Start Streamlit App

### 6.1 Run Streamlit
In PowerShell, type:
```powershell
streamlit run app_streamlit.py
```

### 6.2 Open Browser
- Streamlit will automatically open: http://localhost:8501
- Or manually go to: http://localhost:8501

### 6.3 Login
- **Username:** `admin`
- **Password:** `admin123`

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] New credentials.json file exists in project folder
- [ ] credentials.json is NOT named credentials.json.txt
- [ ] `python create_secrets_toml.py` ran successfully
- [ ] `python test_jwt_signature.py` shows SUCCESS messages
- [ ] Google Sheet is shared with service account email
- [ ] Streamlit app starts without database errors
- [ ] Can login and see the dashboard

---

## 🆘 Troubleshooting

### Problem: "File not found" when running scripts
**Solution:** Make sure you're in the project folder in PowerShell. Type:
```powershell
cd "C:\Users\tonyc\OneDrive - TZ\PUBLISHED REPORTS\Development\Asset Management System"
```

### Problem: Still getting "Invalid JWT Signature"
**Solution:** 
1. Make sure you downloaded a **NEW** key (not using an old one)
2. Delete the old `credentials.json` first, then add the new one
3. Run `python create_secrets_toml.py` again

### Problem: "Module not found" errors
**Solution:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### Problem: Streamlit won't start
**Solution:**
1. Check if port 8501 is in use (try port 8502):
   ```powershell
   streamlit run app_streamlit.py --server.port 8502
   ```
2. Make sure Streamlit is installed:
   ```powershell
   pip install streamlit
   ```

---

## 📝 Quick Command Reference

```powershell
# Test credentials
python test_jwt_signature.py

# Regenerate secrets.toml
python create_secrets_toml.py

# Start Streamlit
streamlit run app_streamlit.py

# Start on different port (if 8501 is busy)
streamlit run app_streamlit.py --server.port 8502
```

---

## Need Help?

If you're still having issues:
1. Check the error message in Streamlit (it will show specific guidance)
2. Run `python test_jwt_signature.py` to see detailed diagnostics
3. Make sure all files are in the correct locations

