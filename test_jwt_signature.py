"""
Test script to validate JWT signature in Google Sheets credentials
This helps diagnose "Invalid JWT Signature" errors
"""

import json
import os
from pathlib import Path
from google.oauth2.service_account import Credentials
import gspread

def test_credentials_json():
    """Test credentials.json file"""
    print("=" * 60)
    print("TESTING credentials.json FILE")
    print("=" * 60)
    
    creds_path = Path('credentials.json')
    
    if not creds_path.exists():
        print("\n[ERROR] credentials.json file NOT FOUND!")
        print("Please download it from Google Cloud Console.")
        return False
    
    try:
        with open(creds_path, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
        
        print(f"\n[OK] File exists and is valid JSON")
        print(f"[OK] Service Account: {creds_data.get('client_email')}")
        
        # Try to create credentials object
        try:
            credentials = Credentials.from_service_account_file(
                str(creds_path),
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive']
            )
            print("[OK] Credentials object created successfully")
            
            # Try to get a token (this will test JWT signature)
            try:
                credentials.refresh(None)
                print("[SUCCESS] JWT signature is VALID! Token refresh successful.")
                return True
            except Exception as e:
                error_msg = str(e)
                if "Invalid JWT Signature" in error_msg or "invalid_grant" in error_msg:
                    print("\n[ERROR] Invalid JWT Signature!")
                    print("The private key in credentials.json is invalid or revoked.")
                    print("\nSOLUTION: Download a NEW key from Google Cloud Console:")
                    print("1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=asset-database-477316")
                    print("2. Click on: asset-database@asset-database-477316.iam.gserviceaccount.com")
                    print("3. Go to 'Keys' tab → 'Add Key' → 'Create new key' → Select 'JSON'")
                    print("4. Download and replace credentials.json")
                else:
                    print(f"\n[ERROR] Token refresh failed: {error_msg}")
                return False
                
        except Exception as e:
            print(f"\n[ERROR] Failed to create credentials object: {e}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON format: {e}")
        print("The file may be corrupted. Please download a fresh copy.")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False

def test_secrets_toml():
    """Test secrets.toml file (for Streamlit)"""
    print("\n" + "=" * 60)
    print("TESTING secrets.toml FILE")
    print("=" * 60)
    
    secrets_path = Path('.streamlit/secrets.toml')
    
    if not secrets_path.exists():
        print("\n[WARNING] secrets.toml file NOT FOUND!")
        print("This is OK if you're using credentials.json instead.")
        return None
    
    try:
        # Try tomli (standard library-compatible TOML parser)
        try:
            import tomli as toml_parser
            with open(secrets_path, 'rb') as f:
                secrets_data = toml_parser.load(f)
        except ImportError:
            # Fallback: try Python 3.11+ built-in tomllib
            try:
                import tomllib as toml_parser
                with open(secrets_path, 'rb') as f:
                    secrets_data = toml_parser.load(f)
            except ImportError:
                raise ImportError("No TOML parser available. Install with: pip install tomli")
        
        if 'GOOGLE_SHEETS' not in secrets_data:
            print("\n[ERROR] GOOGLE_SHEETS section not found in secrets.toml")
            return False
        
        print(f"\n[OK] secrets.toml file exists and is valid TOML")
        print(f"[OK] Service Account: {secrets_data['GOOGLE_SHEETS'].get('client_email')}")
        
        # Build credentials dict
        creds_dict = {
            "type": secrets_data["GOOGLE_SHEETS"]["type"],
            "project_id": secrets_data["GOOGLE_SHEETS"]["project_id"],
            "private_key_id": secrets_data["GOOGLE_SHEETS"]["private_key_id"],
            "private_key": secrets_data["GOOGLE_SHEETS"]["private_key"],
            "client_email": secrets_data["GOOGLE_SHEETS"]["client_email"],
            "client_id": secrets_data["GOOGLE_SHEETS"]["client_id"],
            "auth_uri": secrets_data["GOOGLE_SHEETS"]["auth_uri"],
            "token_uri": secrets_data["GOOGLE_SHEETS"]["token_uri"],
            "auth_provider_x509_cert_url": secrets_data["GOOGLE_SHEETS"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": secrets_data["GOOGLE_SHEETS"]["client_x509_cert_url"]
        }
        
        # Try to create credentials object
        try:
            credentials = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive']
            )
            print("[OK] Credentials object created successfully")
            
            # Try to get a token (this will test JWT signature)
            try:
                credentials.refresh(None)
                print("[SUCCESS] JWT signature is VALID! Token refresh successful.")
                return True
            except Exception as e:
                error_msg = str(e)
                if "Invalid JWT Signature" in error_msg or "invalid_grant" in error_msg:
                    print("\n[ERROR] Invalid JWT Signature!")
                    print("The private key in secrets.toml is invalid or revoked.")
                    print("\nSOLUTION:")
                    print("1. Download a NEW credentials.json from Google Cloud Console")
                    print("2. Run: python create_secrets_toml.py")
                    print("   This will regenerate secrets.toml with the correct format")
                else:
                    print(f"\n[ERROR] Token refresh failed: {error_msg}")
                return False
                
        except Exception as e:
            print(f"\n[ERROR] Failed to create credentials object: {e}")
            print("\nPossible causes:")
            print("- Private key format is incorrect in secrets.toml")
            print("- Missing triple quotes around private_key")
            print("- Private key is corrupted")
            return False
            
    except ImportError:
        print("\n[WARNING] tomli library not installed. Cannot test secrets.toml.")
        print("Install with: pip install tomli")
        return None
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_google_sheets_connection():
    """Test actual connection to Google Sheets"""
    print("\n" + "=" * 60)
    print("TESTING GOOGLE SHEETS CONNECTION")
    print("=" * 60)
    
    # Try credentials.json first
    if Path('credentials.json').exists():
        try:
            credentials = Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive']
            )
            
            client = gspread.authorize(credentials)
            sheet_id = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
            sheet = client.open_by_key(sheet_id)
            
            print(f"\n[SUCCESS] Connected to Google Sheets successfully!")
            print(f"[OK] Sheet title: {sheet.title}")
            print(f"[OK] Sheet ID: {sheet_id}")
            
            # List worksheets
            worksheets = sheet.worksheets()
            print(f"\n[OK] Found {len(worksheets)} worksheet(s):")
            for ws in worksheets:
                print(f"  - {ws.title}")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n[ERROR] Connection failed: {error_msg}")
            
            if "Invalid JWT Signature" in error_msg or "invalid_grant" in error_msg:
                print("\n[ERROR] Invalid JWT Signature - Credentials are invalid!")
            elif "PERMISSION_DENIED" in error_msg or "access" in error_msg.lower():
                print("\n[ERROR] Permission denied - Sheet may not be shared with service account!")
                print(f"Share with: asset-database@asset-database-477316.iam.gserviceaccount.com")
            
            return False
    else:
        print("\n[WARNING] credentials.json not found. Cannot test connection.")
        return None

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("JWT SIGNATURE VALIDATION TEST")
    print("=" * 60)
    print("\nThis script tests your Google Sheets credentials to diagnose")
    print("'Invalid JWT Signature' errors.\n")
    
    # Test credentials.json
    json_result = test_credentials_json()
    
    # Test secrets.toml
    toml_result = test_secrets_toml()
    
    # Test actual connection
    connection_result = test_google_sheets_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if json_result:
        print("\n[SUCCESS] credentials.json is valid and working!")
    elif json_result is False:
        print("\n[ERROR] credentials.json has issues - see errors above")
    
    if toml_result:
        print("\n[SUCCESS] secrets.toml is valid and working!")
    elif toml_result is False:
        print("\n[ERROR] secrets.toml has issues - see errors above")
    
    if connection_result:
        print("\n[SUCCESS] Google Sheets connection successful!")
    elif connection_result is False:
        print("\n[ERROR] Google Sheets connection failed - see errors above")
    
    print("\n" + "=" * 60)

