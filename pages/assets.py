"""Assets page for Streamlit"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
try:
    import barcode
    from barcode.writer import ImageWriter
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False

def show(db, role):
    """Display assets page"""
    st.markdown('<h1 class="main-header">Assets</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage and track all your assets</p>', unsafe_allow_html=True)
    
    # Add Asset button
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search by Asset Code or Item Name", placeholder="Type to search...")
    with col2:
        if st.button("➕ Add Asset", use_container_width=True):
            st.session_state.show_add_asset = True
    
    # Get assets
    assets = db.get_all('Assets')
    
    # Filter assets
    if search_term:
        assets = [a for a in assets if search_term.lower() in a.get('Asset Code', '').lower() or 
                 search_term.lower() in a.get('Item Name', '').lower()]
    
    # Show add asset form
    if st.session_state.get('show_add_asset', False):
        with st.expander("➕ Add New Asset", expanded=True):
            add_asset_form(db)
    
    # Display assets table
    if assets:
        # Barcode printing section
        st.markdown("---")
        st.markdown("### 🏷️ Print Barcodes")
        
        # Create selection checkboxes
        selected_assets = []
        cols = st.columns(min(4, len(assets)))
        for idx, asset in enumerate(assets):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                asset_code = asset.get('Asset Code', '')
                item_name = asset.get('Item Name', '')
                if st.checkbox(
                    f"{asset_code}",
                    key=f"select_{asset_code}",
                    help=f"{item_name}"
                ):
                    selected_assets.append(asset)
        
        # Print button
        if selected_assets:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🖨️ Print Selected Barcodes", type="primary", use_container_width=True):
                    pdf_buffer = generate_barcode_pdf(selected_assets)
                    if pdf_buffer:
                        st.download_button(
                            label="📥 Download Barcode PDF",
                            data=pdf_buffer,
                            file_name=f"barcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
        
        st.markdown("---")
        
        df = pd.DataFrame(assets)
        # Select relevant columns for display
        display_cols = ['Asset Code', 'Item Name', 'Asset Category', 'Location', 'Amount', 'Asset Status']
        available_cols = [col for col in display_cols if col in df.columns]
        st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        
        # Action buttons for each asset
        st.markdown("### Asset Actions")
        for asset in assets:
            with st.expander(f"🔧 {asset.get('Asset Code', '')} - {asset.get('Item Name', '')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{asset.get('Asset Code')}"):
                        st.session_state[f"edit_{asset.get('Asset Code')}"] = True
                with col2:
                    if st.button(f"🖨️ Print Barcode", key=f"print_{asset.get('Asset Code')}"):
                        pdf_buffer = generate_barcode_pdf([asset])
                        if pdf_buffer:
                            st.download_button(
                                label="📥 Download Barcode",
                                data=pdf_buffer,
                                file_name=f"barcode_{asset.get('Asset Code', '')}.pdf",
                                mime="application/pdf",
                                key=f"dl_{asset.get('Asset Code')}"
                            )
                with col3:
                    if role == 'admin':
                        if st.button(f"🗑️ Delete", key=f"delete_{asset.get('Asset Code')}"):
                            if db.delete('Assets', 'Asset Code', asset.get('Asset Code')):
                                st.success("Asset deleted successfully")
                                st.rerun()
    else:
        st.info("No assets found. Click 'Add Asset' to create your first asset.")

def add_asset_form(db):
    """Add asset form"""
    # Store file uploaders in session state (outside form)
    if 'asset_image_file' not in st.session_state:
        st.session_state.asset_image_file = None
    if 'asset_document_file' not in st.session_state:
        st.session_state.asset_document_file = None
    
    # File uploaders outside form
    col1, col2 = st.columns(2)
    with col1:
        image_file = st.file_uploader("Image Attachment", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="asset_image_upload")
        if image_file:
            st.session_state.asset_image_file = image_file
    with col2:
        document_file = st.file_uploader("Document Attachment", type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'], key="asset_doc_upload")
        if document_file:
            st.session_state.asset_document_file = document_file
    
    # Form with all input fields
    with st.form("add_asset_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("Item Name *", key="asset_item_name")
            categories = db.get_all('Categories')
            category_names = [c.get('Category Name', '') for c in categories]
            asset_category = st.selectbox("Asset Category *", [""] + category_names, key="asset_category_select")
            subcategories = db.get_all('Subcategories')
            subcategory_names = [s.get('Subcategory Name', '') for s in subcategories]
            asset_subcategory = st.selectbox("Asset Subcategory", [""] + subcategory_names, key="asset_subcategory_select")
            brands = db.get_all('Brands')
            brand_names = [b.get('Brand Name', '') for b in brands]
            brand = st.selectbox("Brand", [""] + brand_names, key="asset_brand_select")
            asset_description = st.text_area("Asset Description", key="asset_description_text")
        
        with col2:
            amount = st.number_input("Amount", min_value=0.0, step=0.01, key="asset_amount_input")
            locations = db.get_all('Locations')
            location_names = [l.get('Location Name', '') for l in locations]
            location = st.selectbox("Location", [""] + location_names, key="asset_location_select")
            date_of_purchase = st.date_input("Date of Purchase", key="asset_date_input")
            warranty = st.text_input("Warranty", key="asset_warranty_input")
            department = st.text_input("Department", key="asset_department_input")
            ownership = st.text_input("Ownership", key="asset_ownership_input")
            status_options = ["", "Active", "Inactive", "Under Maintenance", "Disposed", "Sold", "Lost"]
            asset_status = st.selectbox("Asset Status", status_options, key="asset_status_select")
        
        # Submit button MUST be inside the form
        submitted = st.form_submit_button("💾 Save Asset", use_container_width=True)
        
        if submitted:
            if item_name and asset_category:
                # Generate asset code
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                asset_code = f"AST-{timestamp}"
                
                # Handle file uploads from session state
                image_filename = ''
                if st.session_state.asset_image_file:
                    image_filename = f"{asset_code}_{st.session_state.asset_image_file.name}"
                
                document_filename = ''
                if st.session_state.asset_document_file:
                    document_filename = f"{asset_code}_{st.session_state.asset_document_file.name}"
                
                asset_data = {
                    'Asset Code': asset_code,
                    'Item Name': item_name,
                    'Asset Category': asset_category,
                    'Asset SubCategory': asset_subcategory or '',
                    'Brand': brand or '',
                    'Asset Description': asset_description or '',
                    'Amount': str(amount) if amount else '',
                    'Location': location or '',
                    'Date of Purchase': date_of_purchase.strftime('%Y-%m-%d') if date_of_purchase else '',
                    'Warranty': warranty or '',
                    'Department': department or '',
                    'Ownership': ownership or '',
                    'Asset Status': asset_status or '',
                    'Image Attachment': image_filename,
                    'Document Attachment': document_filename
                }
                
                if db.insert('Assets', asset_data):
                    st.success("Asset added successfully!")
                    st.session_state.show_add_asset = False
                    st.rerun()
                else:
                    st.error("Failed to add asset")
            else:
                st.error("Please fill in required fields (Item Name and Category)")

def generate_barcode_pdf(assets):
    """Generate PDF with barcodes for selected assets"""
    if not BARCODE_AVAILABLE:
        st.error("Barcode library not available. Please install: pip install python-barcode")
        return None
    
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("Asset Barcodes", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Create barcode images and add to PDF
        for asset in assets:
            asset_code = asset.get('Asset Code', '')
            item_name = asset.get('Item Name', '')
            location = asset.get('Location', '')
            
            if not asset_code:
                continue
            
            # Generate barcode
            try:
                code128 = barcode.get_barcode_class('code128')
                barcode_instance = code128(asset_code, writer=ImageWriter())
                barcode_buffer = BytesIO()
                barcode_instance.write(barcode_buffer)
                barcode_buffer.seek(0)
                
                # Create barcode image
                barcode_img = Image(barcode_buffer, width=3*inch, height=0.8*inch)
                
                # Asset information
                info_text = f"<b>{item_name}</b><br/>Code: {asset_code}"
                if location:
                    info_text += f"<br/>Location: {location}"
                info_para = Paragraph(info_text, styles['Normal'])
                
                # Add to story
                story.append(info_para)
                story.append(Spacer(1, 0.1*inch))
                story.append(barcode_img)
                story.append(Spacer(1, 0.3*inch))
                
            except Exception as e:
                # If barcode generation fails, add text instead
                error_text = f"<b>{item_name}</b><br/>Code: {asset_code}<br/><i>Barcode generation failed: {str(e)}</i>"
                error_para = Paragraph(error_text, styles['Normal'])
                story.append(error_para)
                story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

