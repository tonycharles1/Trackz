"""
Streamlit Asset Management System
Converted from Flask application
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io

# Page configuration
st.set_page_config(
    page_title="Asset Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Premium interface design for Streamlit Cloud
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.75rem !important;
        font-weight: 800 !important;
        color: #1a202c !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .sub-header {
        color: #64748b !important;
        font-size: 1.1rem !important;
        margin-bottom: 2rem !important;
        font-weight: 400 !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Buttons - Modern Design */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(255, 107, 53, 0.39) !important;
        text-transform: none !important;
        letter-spacing: 0.02em !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 20px 0 rgba(255, 107, 53, 0.5) !important;
        background: linear-gradient(135deg, #f7931e 0%, #ff6b35 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Top Header Bar */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Sidebar - Clean Menu Design */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05) !important;
        padding-top: 1rem !important;
    }
    
    /* Hide Streamlit default sidebar elements */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="input"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Sidebar Menu Header */
    [data-testid="stSidebar"] h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar radio buttons - Menu items with icons */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background: transparent !important;
        gap: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        color: #475569 !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        background: transparent !important;
    }
    
    /* Ensure icons are visible */
    [data-testid="stSidebar"] [data-baseweb="radio"] label span,
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        font-size: 1rem !important;
    }
    
    /* Icon styling */
    [data-testid="stSidebar"] .menu-icon {
        font-size: 1.2rem !important;
        width: 20px !important;
        display: inline-block !important;
        text-align: center !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background-color: #e2e8f0 !important;
        color: #1e293b !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label {
        background-color: #ff6b35 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label .menu-icon {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label::before {
        content: '' !important;
    }
    
    /* Sidebar dividers */
    [data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid #e2e8f0 !important;
        margin: 1rem 0 !important;
    }
    
    /* Main content cards */
    .main .block-container > div {
        background: white !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Form styling */
    .stForm {
        background: white !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        border: none !important;
    }
    
    /* Metric Cards - Card Design */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        line-height: 1.2 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricContainer"] {
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stMetricContainer"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Dataframe/Table Styling */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
        background: white !important;
    }
    
    .stDataFrame table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
    }
    
    .stDataFrame thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em !important;
    }
    
    .stDataFrame tbody td {
        padding: 0.875rem 1rem !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #f8fafc !important;
    }
    
    /* Text Inputs */
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Forms */
    .stForm {
        background: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        padding: 0.5rem !important;
    }
    
    .stCheckbox label {
        font-weight: 500 !important;
        color: #1e293b !important;
    }
    
    /* Dividers */
    hr {
        border: none !important;
        border-top: 2px solid #e2e8f0 !important;
        margin: 2rem 0 !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Charts Container */
    [data-testid="stVerticalBlock"] {
        gap: 1.5rem !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        border-radius: 10px !important;
        border: 2px dashed #cbd5e1 !important;
        padding: 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: #ff6b35 !important;
        background-color: #fff7ed !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f7931e 0%, #ff6b35 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'db' not in st.session_state:
    st.session_state.db = None
if 'show_add_asset' not in st.session_state:
    st.session_state.show_add_asset = False

# Database connection class for Streamlit
class GoogleSheetsDB:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.connected = False
        self.error = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets using Streamlit secrets"""
        try:
            # Get credentials from Streamlit secrets
            # Use try-except to handle missing secrets gracefully
            try:
                secrets = st.secrets
            except Exception:
                secrets = {}
            
            if 'GOOGLE_SHEETS' in secrets:
                try:
                    creds_dict = {
                        "type": secrets["GOOGLE_SHEETS"]["type"],
                        "project_id": secrets["GOOGLE_SHEETS"]["project_id"],
                        "private_key_id": secrets["GOOGLE_SHEETS"]["private_key_id"],
                        "private_key": secrets["GOOGLE_SHEETS"]["private_key"],
                        "client_email": secrets["GOOGLE_SHEETS"]["client_email"],
                        "client_id": secrets["GOOGLE_SHEETS"]["client_id"],
                        "auth_uri": secrets["GOOGLE_SHEETS"]["auth_uri"],
                        "token_uri": secrets["GOOGLE_SHEETS"]["token_uri"],
                        "auth_provider_x509_cert_url": secrets["GOOGLE_SHEETS"]["auth_provider_x509_cert_url"],
                        "client_x509_cert_url": secrets["GOOGLE_SHEETS"]["client_x509_cert_url"]
                    }
                    
                    credentials = Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/spreadsheets',
                               'https://www.googleapis.com/auth/drive']
                    )
                except Exception as e:
                    st.warning(f"Error loading from secrets: {e}. Trying credentials.json file...")
                    # Fallback to file
                    if os.path.exists('credentials.json'):
                        credentials = Credentials.from_service_account_file(
                            'credentials.json',
                            scopes=['https://www.googleapis.com/auth/spreadsheets',
                                   'https://www.googleapis.com/auth/drive']
                        )
                    else:
                        raise Exception("No credentials found in secrets or credentials.json file")
            else:
                # Fallback to credentials.json file
                if os.path.exists('credentials.json'):
                    credentials = Credentials.from_service_account_file(
                        'credentials.json',
                        scopes=['https://www.googleapis.com/auth/spreadsheets',
                               'https://www.googleapis.com/auth/drive']
                    )
                else:
                    raise Exception("No credentials found. Please add secrets.toml or credentials.json file")
            
            self.client = gspread.authorize(credentials)
            # Get sheet ID from secrets or use default
            try:
                sheet_id = secrets.get("GOOGLE_SHEET_ID", "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec")
            except:
                sheet_id = "1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec"
            self.sheet = self.client.open_by_key(sheet_id)
            self._initialize_sheets()
            self.connected = True
            
        except Exception as e:
            error_msg = str(e)
            self.error = error_msg
            self.connected = False
            # Don't call st.stop() here - let the app continue to show error message
    
    def _initialize_sheets(self):
        """Initialize all required sheets if they don't exist"""
        sheet_names = ['Users', 'Locations', 'Categories', 'Subcategories', 
                      'AssetTypes', 'Brands', 'Assets', 'AssetMovements', 'ActivityLogs']
        
        for sheet_name in sheet_names:
            try:
                worksheet = self.sheet.worksheet(sheet_name)
                self._ensure_headers(sheet_name)
            except:
                worksheet = self.sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
                self._set_headers(sheet_name)
    
    def _set_headers(self, sheet_name: str):
        """Set headers for each sheet"""
        worksheet = self.sheet.worksheet(sheet_name)
        
        headers = {
            'Users': ['Username', 'Email', 'Password', 'Role'],
            'Locations': ['ID', 'Location Name'],
            'Categories': ['ID', 'Category Name'],
            'Subcategories': ['ID', 'Subcategory Name', 'Category ID'],
            'AssetTypes': ['Asset Code', 'Asset Type', 'Depreciation Value (%)'],
            'Brands': ['ID', 'Brand Name'],
            'Assets': ['Asset Code', 'Item Name', 'Asset Category', 'Asset SubCategory', 
                      'Brand', 'Asset Description', 'Amount', 'Location', 
                      'Date of Purchase', 'Warranty', 'Department', 'Ownership',
                      'Asset Status', 'Image Attachment', 'Document Attachment'],
            'AssetMovements': ['ID', 'Asset Code', 'From Location', 'To Location', 
                              'Movement Date', 'Moved By', 'Notes'],
            'ActivityLogs': ['ID', 'Date & Time', 'Type', 'User', 'Action', 'Entity Type', 
                           'Entity ID', 'Description', 'Details']
        }
        
        if sheet_name in headers:
            worksheet.append_row(headers[sheet_name])
    
    def _ensure_headers(self, sheet_name: str):
        """Ensure headers exist and are up-to-date"""
        # Simplified version - same logic as Flask version
        pass
    
    def get_all(self, sheet_name: str) -> List[Dict]:
        """Get all records from a sheet"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                return []
            
            headers = [str(h).strip() for h in all_values[0]]
            records = []
            
            for row in all_values[1:]:
                if not any(row):
                    continue
                
                record = {}
                for i, header in enumerate(headers):
                    value = row[i] if i < len(row) else ''
                    record[header] = value.strip() if value else ''
                
                if any(record.values()):
                    records.append(record)
            
            return records
        except Exception as e:
            st.error(f"Error getting records from {sheet_name}: {e}")
            return []
    
    def get_by_id(self, sheet_name: str, id_field: str, id_value: str) -> Optional[Dict]:
        """Get a record by ID"""
        records = self.get_all(sheet_name)
        for record in records:
            if str(record.get(id_field)) == str(id_value):
                return record
        return None
    
    def get_next_id(self, sheet_name: str) -> int:
        """Get next available ID"""
        records = self.get_all(sheet_name)
        if not records:
            return 1
        ids = []
        for record in records:
            try:
                ids.append(int(record.get('ID', 0)))
            except:
                pass
        return max(ids, default=0) + 1
    
    def insert(self, sheet_name: str, data: Dict) -> bool:
        """Insert a new record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            headers = worksheet.row_values(1)
            row = [data.get(header, '') for header in headers]
            worksheet.append_row(row)
            return True
        except Exception as e:
            st.error(f"Error inserting record: {e}")
            return False
    
    def update(self, sheet_name: str, id_field: str, id_value: str, data: Dict) -> bool:
        """Update a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = self.get_all(sheet_name)
            headers = worksheet.row_values(1)
            
            for i, record in enumerate(records, start=2):
                if str(record.get(id_field)) == str(id_value):
                    row = [data.get(header, record.get(header, '')) for header in headers]
                    worksheet.update(f"A{i}:{chr(64+len(headers))}{i}", [row])
                    return True
            return False
        except Exception as e:
            st.error(f"Error updating record: {e}")
            return False
    
    def delete(self, sheet_name: str, id_field: str, id_value: str) -> bool:
        """Delete a record"""
        try:
            worksheet = self.sheet.worksheet(sheet_name)
            records = self.get_all(sheet_name)
            
            for i, record in enumerate(records, start=2):
                if str(record.get(id_field)) == str(id_value):
                    worksheet.delete_rows(i)
                    return True
            return False
        except Exception as e:
            st.error(f"Error deleting record: {e}")
            return False

# Initialize database connection
@st.cache_resource
def get_db():
    """Get database connection (cached)"""
    try:
        db = GoogleSheetsDB()
        if not db.connected:
            return None
        return db
    except Exception as e:
        return None

# Authentication functions
def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, password_hash: str) -> bool:
    """Check if password matches hash"""
    return hash_password(password) == password_hash

def login_page():
    """Login page"""
    st.title("Asset Management System")
    st.markdown('<p class="sub-header">Please login to continue</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                db = get_db()
                if db:
                    users = db.get_all('Users')
                    user = next((u for u in users if u.get('Username') == username), None)
                    
                    if user and check_password(password, user.get('Password', '')):
                        st.session_state.authenticated = True
                        st.session_state.user_id = username
                        st.session_state.role = user.get('Role', 'user')
                        st.session_state.db = db
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Database connection failed")
    
    with tab2:
        with st.form("register_form"):
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            reg_role = st.selectbox("Role", ["user", "admin"], key="reg_role")
            submit_reg = st.form_submit_button("Register", use_container_width=True)
            
            if submit_reg:
                if reg_password != reg_confirm:
                    st.error("Passwords do not match")
                elif reg_username and reg_email and reg_password:
                    db = get_db()
                    if db:
                        users = db.get_all('Users')
                        existing = next((u for u in users if u.get('Username') == reg_username), None)
                        if existing:
                            st.error("Username already exists")
                        else:
                            user_data = {
                                'Username': reg_username,
                                'Email': reg_email,
                                'Password': hash_password(reg_password),
                                'Role': reg_role
                            }
                            if db.insert('Users', user_data):
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Registration failed")
                else:
                    st.error("Please fill in all fields")

# Main app
def main():
    """Main application"""
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Initialize database
    if st.session_state.db is None:
        st.session_state.db = get_db()
    
    if st.session_state.db is None or not st.session_state.db.connected:
        # Show helpful error message with connection details
        # Don't use st.stop() - it prevents health checks from passing on Streamlit Cloud
        st.error("## ⚠️ Database Connection Failed")
        
        # Try to get error details
        try:
            db_temp = GoogleSheetsDB()
            if db_temp.error:
                error_msg = db_temp.error
                
                if "Invalid JWT Signature" in error_msg or "invalid_grant" in error_msg:
                    st.error("""
                    **Invalid JWT Signature Error**
                    
                    Your service account credentials are invalid or have been revoked.
                    
                    **For Streamlit Cloud - How to Fix:**
                    
                    1. **Go to Streamlit Cloud Settings:**
                       - Open your app on Streamlit Cloud
                       - Click "Settings" (⚙️ icon)
                       - Click "Secrets"
                    
                    2. **Add/Update Secrets:**
                       - Make sure all Google Sheets credentials are in the secrets
                       - Format should match the example in `.streamlit/secrets.toml.example`
                    
                    3. **Share the Google Sheet:**
                       - Open: https://docs.google.com/spreadsheets/d/1q9jfezVWpFYAmvjo81Lk788kf9DNwqvSx7yxHWRGkec/edit
                       - Share with: `asset-database@asset-database-477316.iam.gserviceaccount.com`
                       - Set permission to "Editor"
                    
                    4. **Redeploy:**
                       - Click "Reboot app" in Streamlit Cloud
                       - Or push a new commit to trigger redeployment
                    """)
                else:
                    st.error(f"**Error:** {error_msg}")
                    
                    with st.expander("Troubleshooting Steps for Streamlit Cloud"):
                        st.markdown("""
                        1. **Check Secrets in Streamlit Cloud:**
                           - Go to your app settings → Secrets
                           - Verify all GOOGLE_SHEETS credentials are correct
                        
                        2. **Verify Sheet Sharing:**
                           - Share the Google Sheet with the service account email
                           - Permission must be "Editor"
                        
                        3. **Check Logs:**
                           - Go to Streamlit Cloud dashboard
                           - Click "Manage app" → "Logs"
                           - Look for detailed error messages
                        """)
        except Exception as e:
            st.error(f"**Error:** {str(e)}")
            with st.expander("Show Full Error Details"):
                import traceback
                st.code(traceback.format_exc())
        
        st.info("💡 **Tip:** Fix the connection issue above, then click 'R' to refresh or use the Streamlit menu to reboot the app.")
        st.warning("⚠️ **Note:** The app is running but database operations are disabled until connection is restored.")
        
        # Don't use st.stop() - it prevents health checks from passing
        # Instead, show a message and allow the app to continue
        st.markdown("---")
        st.markdown("### 🔧 Setup Instructions")
        st.markdown("""
        **To fix this issue on Streamlit Cloud:**
        
        1. Go to your app's **Settings** → **Secrets**
        2. Add your Google Sheets credentials in TOML format
        3. Make sure the Google Sheet is shared with the service account
        4. Click **"Reboot app"** to restart
        """)
        return  # Return early instead of st.stop()
    
    # Top Header Bar
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px;">📦</div>
            <h2 style="margin: 0; color: #1e293b; font-weight: 700; font-size: 1.5rem;">Asset Management</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 1rem; margin-bottom: 1rem;">
            <span style="color: #64748b; font-size: 0.9rem;">Welcome, <strong>{}</strong> ({})</span>
        </div>
        """.format(st.session_state.user_id, st.session_state.role), unsafe_allow_html=True)
        if st.button("Logout", use_container_width=False, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.role = None
            st.session_state.db = None
            st.rerun()
    
    # Sidebar navigation - Icon-based menu
    with st.sidebar:
        # Hide Streamlit default navigation
        st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Menu Header
        st.markdown("### MENU")
        st.markdown("---")
        
        # Navigation menu with icons (using emojis for better visibility)
        menu_items = [
            ("📊", "Dashboard"),
            ("📦", "Assets"),
            ("📍", "Locations"),
            ("🏷️", "Categories"),
            ("🏷️", "Subcategories"),
            ("📋", "Asset Types"),
            ("⭐", "Brands"),
            ("↔️", "Asset Movements"),
            ("🧮", "Depreciation"),
            ("📄", "Asset Report"),
            ("📈", "Movement Report"),
            ("📝", "Logs")
        ]
        
        # Create custom radio buttons with icons - ensure icons display
        page_options = []
        for icon, name in menu_items:
            # Use HTML to ensure icon displays properly
            page_options.append(f"{icon} {name}")
        
        page = st.radio(
            "Navigation",
            page_options,
            label_visibility="collapsed",
            format_func=lambda x: x
        )
        
        # Extract page name from selection (remove icon)
        if " " in page:
            page = page.split(" ", 1)[1]
        else:
            # Fallback: match by removing emoji
            for icon, name in menu_items:
                if name in page:
                    page = name
                    break
    
    # Route to appropriate page
    try:
        if page == "Dashboard":
            from pages import dashboard
            dashboard.show(st.session_state.db, st.session_state.role)
        elif page == "Assets":
            from pages import assets
            assets.show(st.session_state.db, st.session_state.role)
        elif page == "Locations":
            from pages import locations
            locations.show(st.session_state.db, st.session_state.role)
        elif page == "Categories":
            from pages import categories
            categories.show(st.session_state.db, st.session_state.role)
        elif page == "Subcategories":
            from pages import subcategories
            subcategories.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Types":
            from pages import asset_types
            asset_types.show(st.session_state.db, st.session_state.role)
        elif page == "Brands":
            from pages import brands
            brands.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Movements":
            from pages import asset_movements
            asset_movements.show(st.session_state.db, st.session_state.role)
        elif page == "Depreciation":
            from pages import depreciation
            depreciation.show(st.session_state.db, st.session_state.role)
        elif page == "Asset Report":
            from pages import asset_report
            asset_report.show(st.session_state.db, st.session_state.role)
        elif page == "Movement Report":
            from pages import movement_report
            movement_report.show(st.session_state.db, st.session_state.role)
        elif page == "Logs":
            from pages import logs
            logs.show(st.session_state.db, st.session_state.role)
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.exception(e)

# Streamlit automatically runs the script, so we call main() directly
# This ensures the app starts even if there are errors
# Wrapped in try-except to handle any startup errors gracefully
try:
    main()
except Exception as e:
    # Show error but don't crash - allows health check to pass
    st.error("## ⚠️ Application Error")
    st.error(f"An error occurred while starting the application: {str(e)}")
    with st.expander("Show Full Error Details"):
        import traceback
        st.code(traceback.format_exc())
    st.info("💡 **Tip:** Check the error details above and fix any configuration issues. The app will attempt to continue.")

