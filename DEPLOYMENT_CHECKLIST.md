# ✅ Deployment Checklist

## Step 1: Verify App is Deployed ✅

1. Go to: https://share.streamlit.io
2. Check your app status
3. Should show: **"Running"** (green)
4. If still showing errors, wait 1-2 minutes for auto-redeploy

---

## Step 2: Verify Secrets are Configured 🔐

1. In Streamlit Cloud, click your app
2. Click **"Settings"** → **"Secrets"**
3. Verify you have:

```toml
[GOOGLE_SHEETS]
type = "service_account"
project_id = "asset-database-477316"
private_key_id = "your-private-key-id"
private_key = """-----BEGIN PRIVATE KEY-----
your-key-here
-----END PRIVATE KEY-----"""
client_email = "asset-database@asset-database-477316.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

GOOGLE_SHEET_ID = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
```

**If secrets are missing:**
- Copy content from your local `.streamlit/secrets.toml` file
- Paste into Streamlit Cloud Secrets
- Save and redeploy

---

## Step 3: Verify Google Sheet Sharing 📊

1. Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
2. Click **"Share"** button
3. Verify this email is listed:
   - `asset-database@asset-database-477316.iam.gserviceaccount.com`
   - Permission: **Editor**
4. If not shared, add it now

---

## Step 4: Test the App 🌐

1. Open your Streamlit Cloud app URL
2. You should see the **Login page**
3. Try to login:
   - Check if there are existing users
   - If not, use **Register** to create first admin account

---

## Step 5: Check for Errors 🔍

### If you see "Database Connection Failed":
- Check secrets are configured correctly
- Verify Google Sheet is shared with service account
- Check Streamlit Cloud logs for specific error

### If CSS doesn't show:
- Should be fixed now (we simplified CSS injection)
- Try refreshing the page

### If barcode printing doesn't work:
- This is expected (python-barcode is optional)
- The app will show a message if barcode is attempted

---

## Step 6: First Login 👤

### Option A: Register New User
1. Click **"Register"** tab
2. Create admin account:
   - Username: (your choice)
   - Email: (your email)
   - Password: (strong password)
   - Role: **admin**
3. Click Register
4. Login with your new account

### Option B: Use Default Admin (if exists)
- Username: `admin`
- Password: `admin123`
- **Important:** Change password after first login!

---

## Step 7: Verify Features ✅

Test these features to make sure everything works:

- [ ] Dashboard loads and shows metrics
- [ ] Can add new asset
- [ ] Can view assets list
- [ ] Can add locations, categories, brands
- [ ] Can view reports
- [ ] Can export to Excel
- [ ] CSS styling is visible
- [ ] Navigation works between pages

---

## Troubleshooting

### App won't start:
- Check Streamlit Cloud logs
- Verify secrets are correct
- Make sure Google Sheet is shared

### Database connection error:
- Verify secrets.toml format in Streamlit Cloud
- Check private_key uses triple quotes
- Verify service account email matches

### Other errors:
- Check Streamlit Cloud → Manage App → Logs
- Share error message for help

---

## Success Indicators ✅

Your app is successfully deployed when:
- ✅ App shows "Running" status
- ✅ Login page appears
- ✅ Can register/login
- ✅ Dashboard loads
- ✅ Can add/view assets
- ✅ No database connection errors

---

## Next Steps After Deployment

1. **Share the app URL** with your team
2. **Create admin accounts** for team members
3. **Set up master data** (Locations, Categories, etc.)
4. **Start adding assets**
5. **Test all features** thoroughly

---

**Your app should be live now!** 🎉

