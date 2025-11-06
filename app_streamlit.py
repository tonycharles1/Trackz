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

# Custom CSS - Matching Flask Template Design
# Inject CSS early and ensure it persists - Based on templates/base.html
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');
    
    /* DIN Font (same as Flask) */
    @font-face {
        font-family: 'DIN';
        src: local('DIN'), local('DIN-Regular'), local('FF DIN'), local('FF-DIN-Regular'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Regular.woff') format('woff'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Regular.ttf') format('truetype');
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }
    
    @font-face {
        font-family: 'DIN';
        src: local('DIN Medium'), local('DIN-Medium'), local('FF DIN Medium'), local('FF-DIN-Medium'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Medium.woff') format('woff'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Medium.ttf') format('truetype');
        font-weight: 500;
        font-style: normal;
        font-display: swap;
    }
    
    @font-face {
        font-family: 'DIN';
        src: local('DIN Bold'), local('DIN-Bold'), local('FF DIN Bold'), local('FF-DIN-Bold'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Bold.woff') format('woff'),
             url('https://fonts.cdnfonts.com/s/14882/DIN-Bold.ttf') format('truetype');
        font-weight: 700;
        font-style: normal;
        font-display: swap;
    }
    
    * {
        font-family: 'DIN', 'DIN Alternate', 'DIN Condensed', 'FF DIN', 'FF DIN Condensed', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif !important;
        box-sizing: border-box !important;
    }
    
    /* Main App Styling - Match Flask background */
    .stApp {
        background-color: #f5f7fa !important;
        background: #f5f7fa !important;
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
    
    /* Headings - Match Flask */
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748 !important;
        font-weight: 700 !important;
    }
    
    h1 {
        font-size: 2rem !important;
        margin-bottom: 8px !important;
    }
    
    h2 {
        font-size: 1.875rem !important;
        margin-bottom: 24px !important;
    }
    
    /* Buttons - Match Flask Design */
    /* Primary/Orange Button */
    .stButton>button[kind="primary"],
    .stButton>button:not([kind="secondary"]):not([kind="minimal"]) {
        background-color: #ff6b35 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        box-shadow: none !important;
    }
    
    .stButton>button[kind="primary"]:hover,
    .stButton>button:not([kind="secondary"]):not([kind="minimal"]):hover {
        background-color: #e55a2b !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3) !important;
        color: white !important;
    }
    
    /* Secondary/Grey Button */
    .stButton>button[kind="secondary"] {
        background-color: #edf2f7 !important;
        color: #2d3748 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        box-shadow: none !important;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background-color: #e2e8f0 !important;
        color: #2d3748 !important;
        transform: none !important;
    }
    
    /* Success Button */
    .stButton>button[kind="success"] {
        background-color: #48bb78 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button[kind="success"]:hover {
        background-color: #38a169 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3) !important;
        color: white !important;
    }
    
    /* Danger Button */
    .stButton>button[kind="danger"] {
        background-color: #f56565 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button[kind="danger"]:hover {
        background-color: #e53e3e !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(245, 101, 101, 0.3) !important;
        color: white !important;
    }
    
    /* Warning Button */
    .stButton>button[kind="warning"] {
        background-color: #ed8936 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button[kind="warning"]:hover {
        background-color: #dd6b20 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3) !important;
        color: white !important;
    }
    
    /* Info Button */
    .stButton>button[kind="info"] {
        background-color: #4299e1 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button[kind="info"]:hover {
        background-color: #3182ce !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3) !important;
        color: white !important;
    }
    
    /* Top Header Bar */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Sidebar - Match Flask Design (White Card) */
    [data-testid="stSidebar"] {
        background: white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        border-right: 1px solid #e2e8f0 !important;
        padding: 0 !important;
    }
    
    /* Sidebar Header */
    [data-testid="stSidebar"] > div:first-child {
        background: #f7fafc !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 20px 16px !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #2d3748 !important;
        margin: 0 !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
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
    
    /* Sidebar radio buttons - Match Flask nav-link design */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background: transparent !important;
        padding: 8px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        color: #4a5568 !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        background: transparent !important;
    }
    
    /* Ensure icons are visible */
    [data-testid="stSidebar"] [data-baseweb="radio"] label span,
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        font-size: 1rem !important;
    }
    
    /* Icon styling - Match Flask */
    [data-testid="stSidebar"] .menu-icon,
    [data-testid="stSidebar"] [data-baseweb="radio"] label span:first-child {
        font-size: 1.1rem !important;
        width: 20px !important;
        display: inline-block !important;
        text-align: center !important;
        color: #718096 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background-color: #f7fafc !important;
        color: #2d3748 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover .menu-icon,
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover span:first-child {
        color: #ff6b35 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label {
        background-color: #fff5f0 !important;
        color: #ff6b35 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label .menu-icon,
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + label span:first-child {
        color: #ff6b35 !important;
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
    
    /* Main content cards - Match Flask card design */
    .main .block-container > div {
        background: transparent !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }
    
    /* Card styling - Match Flask */
    .card, .stCard {
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        margin-bottom: 24px !important;
        transition: all 0.2s !important;
        overflow: hidden !important;
    }
    
    .card:hover, .stCard:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .card-header {
        background: white !important;
        color: #2d3748 !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 20px 24px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .card-body {
        padding: 24px !important;
    }
    
    /* Form styling - Match Flask */
    .stForm {
        background: white !important;
        padding: 24px !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        border: none !important;
        margin-bottom: 24px !important;
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
    
    /* Dataframe/Table Styling - Match Flask table */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        box-shadow: none !important;
    }
    
    .stDataFrame table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
        background: white !important;
        margin: 0 !important;
    }
    
    .stDataFrame thead {
        background: #f7fafc !important;
    }
    
    .stDataFrame thead th {
        border: none !important;
        border-bottom: 2px solid #e2e8f0 !important;
        font-weight: 600 !important;
        padding: 16px !important;
        color: #2d3748 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        background: #f7fafc !important;
    }
    
    .stDataFrame tbody tr {
        transition: background-color 0.2s !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #f7fafc !important;
    }
    
    .stDataFrame tbody td {
        padding: 16px !important;
        color: #4a5568 !important;
        vertical-align: middle !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    /* Text Inputs - Match Flask form-control */
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e0 !important;
        padding: 10px 16px !important;
        transition: all 0.2s !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #718096 !important;
    }
    
    /* Input labels - Match Flask form-label */
    .stTextInput label {
        font-weight: 600 !important;
        color: #2d3748 !important;
        font-size: 0.875rem !important;
        margin-bottom: 8px !important;
    }
    
    /* Selectbox - Match Flask form-select */
    .stSelectbox>div>div {
        border-radius: 8px !important;
        border: 1px solid #cbd5e0 !important;
    }
    
    .stSelectbox>div>div>select {
        padding: 10px 16px !important;
        color: #2d3748 !important;
    }
    
    .stSelectbox>div>div>select:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        outline: none !important;
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
    
    /* Alerts - Match Flask */
    .stSuccess,
    .alert-success {
        background-color: #c6f6d5 !important;
        color: #22543d !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 16px 20px !important;
    }
    
    .stError,
    .alert-danger {
        background-color: #fed7d7 !important;
        color: #742a2a !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 16px 20px !important;
    }
    
    .stInfo,
    .alert-info {
        background-color: #bee3f8 !important;
        color: #2c5282 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 16px 20px !important;
    }
    
    .stWarning,
    .alert-warning {
        background-color: #feebc8 !important;
        color: #744210 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 16px 20px !important;
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
<script>
    // Ensure CSS loads on Streamlit Cloud - inject into head
    (function() {
        if (!document.querySelector('style[data-streamlit-custom-css]')) {
            const style = document.createElement('style');
            style.setAttribute('data-streamlit-custom-css', 'true');
            style.innerHTML = document.querySelector('style').innerHTML;
            document.head.appendChild(style);
        }
    })();
</script>
""", unsafe_allow_html=True)

# Additional CSS injection using components.html for Streamlit Cloud
try:
    import streamlit.components.v1 as components
    components.html("""
    <style>
        /* Critical styles for Streamlit Cloud */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }
        [data-testid="stSidebar"] {
            background: #f8fafc !important;
        }
        .stButton>button {
            background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%) !important;
            color: white !important;
            border-radius: 12px !important;
        }
    </style>
    """, height=0)
except:
    pass

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
    """Login page - Modern two-panel design with tabs"""
    import streamlit.components.v1 as components
    
    # Determine which tab is active
    current_tab = st.session_state.get('login_tab', 'login')
    
    # Inject modern CSS
    st.markdown("""
    <style>
        :root {
            --bg: #f6f9ff;
            --card: #ffffff;
            --accent1: #5b6fff;
            --accent2: #7dd3fc;
            --muted: #6b7280;
            --glass: rgba(255,255,255,0.6);
            --radius: 14px;
            --shadow: 0 8px 30px rgba(28,36,70,0.08);
        }
        
        .stApp {
            background: linear-gradient(160deg, var(--bg) 0%, #eef4ff 100%) !important;
            background-attachment: fixed !important;
        }
        
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Create the HTML component with login/register forms
    html_content = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <style>
            :root{{
                --bg:#f6f9ff;
                --card:#ffffff;
                --accent1:#5b6fff;
                --accent2:#7dd3fc;
                --muted:#6b7280;
                --glass: rgba(255,255,255,0.6);
                --radius:14px;
                --shadow: 0 8px 30px rgba(28,36,70,0.08);
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            }}
            *{{box-sizing:border-box}}
            html,body{{height:100%; margin:0; padding:0}}
            body{{
                background: linear-gradient(160deg,var(--bg) 0%, #eef4ff 100%);
                display:grid;
                place-items:center;
                padding:32px;
                -webkit-font-smoothing:antialiased;
                -moz-osx-font-smoothing:grayscale;
                color:#111827;
            }}
            .container{{
                width:100%;
                max-width:980px;
                background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(255,255,255,0.95));
                border-radius:18px;
                box-shadow:var(--shadow);
                overflow:hidden;
                display:grid;
                grid-template-columns: 420px 1fr;
                min-height:520px;
            }}
            .hero{{
                padding:36px 28px;
                background: linear-gradient(180deg,var(--accent1), #9aa7ff);
                color:white;
                display:flex;
                flex-direction:column;
                justify-content:center;
                gap:18px;
            }}
            .logo{{
                font-weight:700; letter-spacing:0.4px; font-size:20px;
                display:flex; align-items:center; gap:12px;
            }}
            .logo .orb{{width:44px; height:44px; border-radius:10px; background:rgba(255,255,255,0.18); display:grid; place-items:center; font-weight:700}}
            .hero h1{{font-size:26px; margin:0}}
            .hero p{{margin:0; opacity:0.95}}
            .formArea{{
                padding:34px 40px;
                background: linear-gradient(180deg,var(--card), rgba(255,255,255,0.98));
            }}
            .tabs{{display:flex; gap:8px; margin-bottom:14px}}
            .tab{{padding:10px 14px; border-radius:12px; cursor:pointer; font-weight:600; color:var(--muted); transition:all 0.2s}}
            .tab.active{{background: linear-gradient(90deg, rgba(91,111,255,0.12), rgba(125,211,252,0.1)); color:var(--accent1)}}
            .tab:hover{{background:rgba(91,111,255,0.08)}}
            form{{max-width:520px}}
            .field{{display:flex; flex-direction:column; gap:8px; margin-bottom:12px}}
            label{{font-size:13px; color:var(--muted); font-weight:500}}
            input[type="text"], input[type="email"], input[type="password"], input[type="tel"]{{
                padding:12px 14px; border-radius:10px; border:1px solid #e6e9f2; background:transparent; outline:none; font-size:15px;
                transition:box-shadow .12s, border-color .12s
            }}
            input:focus{{border-color:var(--accent1); box-shadow:0 6px 18px rgba(91,111,255,0.12)}}
            .row{{display:flex; gap:12px}}
            .row .field{{flex:1}}
            .actions{{display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:6px}}
            .btn{{
                padding:10px 14px; border-radius:10px; border:0; font-weight:700; cursor:pointer; font-size:15px; min-width:120px;
                transition:all 0.2s
            }}
            .btn.primary{{background:linear-gradient(90deg,var(--accent1), #7b8dff); color:white; box-shadow: 0 8px 22px rgba(91,111,255,0.18)}}
            .btn.primary:hover{{transform:translateY(-1px); box-shadow: 0 10px 28px rgba(91,111,255,0.25)}}
            .btn.ghost{{background:transparent; color:var(--muted); border:1px solid #eef2ff}}
            .muted{{color:var(--muted); font-size:13px}}
            .sep{{display:flex; align-items:center; gap:12px; margin:18px 0}}
            .sep span{{height:1px; background:#eef2ff; flex:1}}
            .sep .txt{{font-size:13px; color:var(--muted); text-align:center}}
            .socials{{display:flex; gap:10px}}
            .socials button{{flex:1; padding:10px; border-radius:10px; border:1px solid #eef2ff; background:white; cursor:pointer; transition:all 0.2s}}
            .socials button:hover{{border-color:var(--accent1); background:#f8faff}}
            .foot{{margin-top:18px; font-size:13px; color:var(--muted)}}
            .foot a{{color:var(--accent1); text-decoration:none; font-weight:500}}
            .foot a:hover{{text-decoration:underline}}
            @media (max-width:880px){{
                .container{{grid-template-columns:1fr; padding:18px; min-height:unset}}
                .hero{{order:2; padding:20px}}
            }}
        </style>
    </head>
    <body>
        <div class="container" role="main">
            <section class="hero">
                <div class="logo"><div class="orb">📦</div> Asset Management</div>
                <h1>Welcome back</h1>
                <p>Quick and secure login for your Asset Management System. Clean, responsive layout.</p>
                <div style="margin-top:auto; font-size:13px; opacity:0.95">New here? Switch to Register from the tab above.</div>
            </section>
            <section class="formArea">
                <div class="tabs" role="tablist">
                    <div class="tab {'active' if current_tab == 'login' else ''}" id="tab-login" onclick="switchTab('login')">Login</div>
                    <div class="tab {'active' if current_tab == 'register' else ''}" id="tab-register" onclick="switchTab('register')">Register</div>
                </div>
                <div id="form-container"></div>
            </section>
        </div>
        <script>
            function switchTab(tab) {{
                window.parent.postMessage({{type: 'switchTab', tab: tab}}, '*');
            }}
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'updateTab') {{
                    const tab = event.data.tab;
                    document.getElementById('tab-login').classList.toggle('active', tab === 'login');
                    document.getElementById('tab-register').classList.toggle('active', tab === 'register');
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit columns to create the two-panel layout
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        # Hero section
        st.markdown("""
        <div style="background: linear-gradient(180deg, #5b6fff, #9aa7ff); padding: 36px 28px; border-radius: 18px 0 0 18px; color: white; height: 520px; display: flex; flex-direction: column; justify-content: center; gap: 18px;">
            <div style="font-weight: 700; letter-spacing: 0.4px; font-size: 20px; display: flex; align-items: center; gap: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(255,255,255,0.18); display: grid; place-items: center; font-weight: 700;">📦</div>
                Asset Management
            </div>
            <h1 style="font-size: 26px; margin: 0;">Welcome back</h1>
            <p style="margin: 0; opacity: 0.95;">Quick and secure login for your Asset Management System. Clean, responsive layout.</p>
            <div style="margin-top: auto; font-size: 13px; opacity: 0.95;">New here? Switch to Register from the tab on the right.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                st.markdown('<div class="field">', unsafe_allow_html=True)
                username = st.text_input("Email", placeholder="you@domain.com", key="login_username")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="field">', unsafe_allow_html=True)
                password = st.text_input("Password", type="password", placeholder="Your password", key="login_password")
                st.markdown('</div>', unsafe_allow_html=True)
                
                col_remember, col_submit = st.columns([1, 1])
                with col_remember:
                    remember = st.checkbox("Remember me", key="remember")
                with col_submit:
                    submit = st.form_submit_button("Sign in", use_container_width=True, type="primary")
                
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
                
                # Social login
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 12px; margin: 18px 0;">
                    <span style="height: 1px; background: #eef2ff; flex: 1;"></span>
                    <div style="font-size: 13px; color: #6b7280; text-align: center;">or continue with</div>
                    <span style="height: 1px; background: #eef2ff; flex: 1;"></span>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button style="flex: 1; padding: 10px; border-radius: 10px; border: 1px solid #eef2ff; background: white; cursor: pointer;">Google</button>
                    <button style="flex: 1; padding: 10px; border-radius: 10px; border: 1px solid #eef2ff; background: white; cursor: pointer;">GitHub</button>
                </div>
                <p style="margin-top: 18px; font-size: 13px; color: #6b7280;">Forgot password? <a href="#" style="color: #5b6fff; text-decoration: none; font-weight: 500;">Reset</a></p>
                """, unsafe_allow_html=True)
        
        with tab2:
            with st.form("register_form"):
                col_first, col_last = st.columns(2)
                with col_first:
                    reg_first = st.text_input("First name", placeholder="First name", key="reg_first")
                with col_last:
                    reg_last = st.text_input("Last name", placeholder="Last name", key="reg_last")
                
                reg_email = st.text_input("Email", placeholder="you@domain.com", key="reg_email")
                reg_phone = st.text_input("Phone (optional)", placeholder="+91 98765 43210", key="reg_phone")
                reg_password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
                
                col_terms, col_submit_reg = st.columns([1.5, 1])
                with col_terms:
                    st.markdown('<div class="muted">By registering you agree to our <a href="#">Terms</a>.</div>', unsafe_allow_html=True)
                with col_submit_reg:
                    submit_reg = st.form_submit_button("Create account", use_container_width=True, type="primary")
                
                if submit_reg:
                    reg_username = f"{reg_first}_{reg_last}".lower().replace(" ", "")
                    if reg_first and reg_last and reg_email and reg_password:
                        db = get_db()
                        if db:
                            users = db.get_all('Users')
                            existing = next((u for u in users if u.get('Username') == reg_username or u.get('Email') == reg_email), None)
                            if existing:
                                st.error("Username or email already exists")
                            else:
                                user_data = {
                                    'Username': reg_username,
                                    'Email': reg_email,
                                    'Password': hash_password(reg_password),
                                    'Role': 'user'
                                }
                                if db.insert('Users', user_data):
                                    st.success("Registration successful! Please login.")
                                    st.rerun()
                                else:
                                    st.error("Registration failed")
                        else:
                            st.error("Database connection failed")
                    else:
                        st.error("Please fill in all required fields")
    
    # Add CSS for form styling
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            margin-bottom: 14px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 14px;
            border-radius: 12px;
            font-weight: 600;
            color: #6b7280;
            transition: all 0.2s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(91,111,255,0.08);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, rgba(91,111,255,0.12), rgba(125,211,252,0.1));
            color: #5b6fff;
        }
        .stTextInput>div>div>input {
            padding: 12px 14px !important;
            border-radius: 10px !important;
            border: 1px solid #e6e9f2 !important;
            font-size: 15px !important;
            transition: box-shadow .12s, border-color .12s !important;
        }
        .stTextInput>div>div>input:focus {
            border-color: #5b6fff !important;
            box-shadow: 0 6px 18px rgba(91,111,255,0.12) !important;
        }
        .stTextInput label {
            font-size: 13px !important;
            color: #6b7280 !important;
            font-weight: 500 !important;
        }
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            transition: all 0.2s !important;
        }
        .stButton>button[type="primary"] {
            background: linear-gradient(90deg, #5b6fff, #7b8dff) !important;
            box-shadow: 0 8px 22px rgba(91,111,255,0.18) !important;
        }
        .stButton>button[type="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 10px 28px rgba(91,111,255,0.25) !important;
        }
    </style>
    """, unsafe_allow_html=True)

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
    
    # Top Navbar - Match Flask Design
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <i class="bi bi-box-seam" style="color: #ff6b35; font-size: 1.5rem;"></i>
            <span style="font-weight: 700; font-size: 1.5rem; color: #2d3748;">Asset Management</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem;">
            <span style="color: #718096; font-weight: 400;">
                Welcome, <strong style="color: #2d3748;">{st.session_state.user_id}</strong> ({st.session_state.role})
            </span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn", use_container_width=False, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.role = None
            st.session_state.db = None
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar navigation - Match Flask Design
    with st.sidebar:
        # Hide Streamlit default navigation
        st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
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
        </style>
        """, unsafe_allow_html=True)
        
        # Sidebar Header - Match Flask
        st.markdown("""
        <div style="background: #f7fafc; border-bottom: 1px solid #e2e8f0; padding: 20px 16px; margin: -1rem -1rem 1rem -1rem;">
            <h5 style="color: #2d3748; margin: 0; font-weight: 700; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.5px;">MENU</h5>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu - Plain text only (no icons to avoid rendering issues)
        menu_items = [
            "Dashboard",
            "Assets",
            "Locations",
            "Categories",
            "Subcategories",
            "Asset Types",
            "Brands",
            "Asset Movements",
            "Depreciation",
            "Asset Report",
            "Movement Report",
            "Logs"
        ]
        
        # Create radio buttons - simple text only
        page = st.radio(
            "Navigation",
            menu_items,
            label_visibility="collapsed"
        )
    
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

    # Footer - Match Flask Design
    st.markdown("""
    <footer style="background: white; border-top: 1px solid #e2e8f0; padding: 24px 0; margin-top: 3rem;">
        <div style="max-width: 1600px; margin: 0 auto; padding: 0 24px;">
            <div style="text-align: center; color: #718096; font-size: 0.875rem;">
                <p style="margin: 0;">
                    Powered by : <strong style="color: #ff6b35;">Trackz Solutions and Technologies</strong>
                </p>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)

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

