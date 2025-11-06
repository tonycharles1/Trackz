# 📋 Quick Command Reference

## Run Streamlit App Locally

### Correct Command:
```powershell
python -m streamlit run app_streamlit.py
```

**NOT:** `streamlit run app_streamlit.py` (may not work if streamlit not in PATH)  
**USE:** `python -m streamlit run app_streamlit.py` ✅

---

## Alternative Commands

### Using Python Module (Recommended):
```powershell
python -m streamlit run app_streamlit.py
```

### If streamlit is in PATH:
```powershell
streamlit run app_streamlit.py
```

### Run on Different Port:
```powershell
python -m streamlit run app_streamlit.py --server.port 8502
```

### Run Without Opening Browser:
```powershell
python -m streamlit run app_streamlit.py --server.headless true
```

---

## Quick Start

### Easiest Way:
1. **Double-click:** `start_local.bat`
2. Browser opens automatically

### Manual Way:
```powershell
python -m streamlit run app_streamlit.py
```

---

## Other Useful Commands

### Install Dependencies:
```powershell
pip install -r requirements.txt
```

### Check Streamlit Version:
```powershell
python -m streamlit --version
```

### Test Credentials:
```powershell
python test_jwt_signature.py
```

### Generate secrets.toml:
```powershell
python create_secrets_toml.py
```

---

## Your App File

**File name:** `app_streamlit.py`  
**Command:** `python -m streamlit run app_streamlit.py`

---

**That's the correct command!** 🚀

