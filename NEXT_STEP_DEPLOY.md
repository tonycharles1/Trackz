# 🚀 Next Step: Deploy Your Streamlit App

## Current Status ✅
- ✅ All files pushed to GitHub
- ✅ Credentials tested and working
- ✅ Repository ready for deployment

## Option 1: Test Locally First (Recommended)

### Step 1: Start Streamlit
```powershell
streamlit run app_streamlit.py
```

### Step 2: Verify Everything Works
- Open http://localhost:8501
- Login with: `admin` / `admin123`
- Test key features:
  - Dashboard loads
  - Can add assets
  - Can view reports

### Step 3: Fix Any Issues
If you find any problems, fix them locally before deploying.

---

## Option 2: Deploy to Streamlit Cloud (Next Step)

Once local testing is done, deploy to Streamlit Cloud:

### Step 1: Go to Streamlit Cloud
1. Visit: **https://share.streamlit.io**
2. Sign in with your **GitHub account** (same account as `tonycharles1`)

### Step 2: Create New App
1. Click **"New app"** button
2. Select repository: **`tonycharles1/Asset`**
3. Set branch: **`master`** (or `main` if you renamed it)
4. Set main file: **`app_streamlit.py`**
5. App URL: (leave default or customize)

### Step 3: Add Secrets
1. Click **"Advanced settings"**
2. Click **"Secrets"**
3. Paste your credentials in TOML format:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "YOUR_PRIVATE_KEY_ID_FROM_CREDENTIALS_JSON"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID_FROM_CREDENTIALS_JSON"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL_FROM_CREDENTIALS_JSON"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

**To get these values:**
- Open your `credentials.json` file
- Copy each value exactly as shown
- Make sure private_key uses triple quotes and includes BEGIN/END lines

**OR** use the helper script:
```powershell
python create_secrets_toml.py
```
Then copy the content from `.streamlit/secrets.toml` (but don't commit it!)

### Step 4: Deploy
1. Click **"Deploy"** button
2. Wait 2-5 minutes for build
3. Your app will be live at: `https://your-app-name.streamlit.app`

### Step 5: First Login
1. Open your deployed app URL
2. Register a new user (first user becomes admin)
3. Or login if default admin exists: `admin` / `admin123`

---

## Important Notes

### Branch Name
- Your current branch is `master`
- If Streamlit Cloud asks for `main`, you can either:
  - Rename branch: `git branch -M main` then `git push origin main`
  - Or just use `master` in Streamlit Cloud settings

### Security
- ✅ `credentials.json` is NOT in GitHub (properly ignored)
- ✅ `.streamlit/secrets.toml` is NOT in GitHub (properly ignored)
- ✅ Only `.streamlit/secrets.toml.example` is in GitHub (safe)

### Google Sheet Sharing
Make sure your Google Sheet is shared with:
- Email: `asset-database@asset-database-477316.iam.gserviceaccount.com`
- Permission: **Editor**

---

## Quick Commands Reference

```powershell
# Test locally
streamlit run app_streamlit.py

# Generate secrets.toml content (for copying to Streamlit Cloud)
python create_secrets_toml.py

# Test credentials
python test_jwt_signature.py

# Check git status
git status
```

---

## Troubleshooting

### "Repository not found" in Streamlit Cloud
- Make sure you're signed in with the correct GitHub account
- Check that the repository is public (or you've granted Streamlit Cloud access)

### "Branch not found"
- Check your branch name: `git branch`
- Use `master` or rename to `main`: `git branch -M main`

### "Invalid JWT Signature" after deployment
- Double-check secrets are copied correctly
- Verify private_key uses triple quotes
- Make sure all values are from your current credentials.json

---

## 🎯 Recommended Path

1. **Test locally first** (5 minutes)
   ```powershell
   streamlit run app_streamlit.py
   ```

2. **Deploy to Streamlit Cloud** (10 minutes)
   - Follow steps above
   - Copy secrets correctly
   - Wait for deployment

3. **Verify deployment** (5 minutes)
   - Test all features
   - Create admin account
   - Share with your team!

---

**Ready? Start with testing locally, then deploy!** 🚀

