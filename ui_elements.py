import streamlit as st
import pandas as pd

def upload_files():
    uploaded_file = st.file_uploader('Upload Excel File', type=['xlsx'])
    vendor_file = st.file_uploader('Upload Vendor Information Excel File', type=['xlsx'], key='vendor_file')
    return uploaded_file, vendor_file

def select_excel_sheets(main_file, vendor_file):
    main_sheets = pd.ExcelFile(main_file).sheet_names
    vendor_sheets = pd.ExcelFile(vendor_file).sheet_names
    main_sheet = st.selectbox("Select sheet from main data file", main_sheets)
    st.session_state["main_sheet"] = main_sheet
    vendor_sheet = st.selectbox("Select sheet from vendor info file", vendor_sheets)
    st.session_state["vendor_sheet"] = vendor_sheet
    return main_sheet, vendor_sheet

def column_mapping_section(df_columns, vendor_columns):
    with st.expander("Field Mapping Options"):
        st.subheader("Field Mapping")
        col1, col2 = st.columns(2)
        main_field = col1.selectbox("Select main file key for mapping 'Supplier No'", df_columns)
        st.session_state["main_field"] = main_field
        vendor_field = col2.selectbox("Select vendor file key for mapping 'Supplier No'", vendor_columns)
        st.session_state["vendor_field"] = vendor_field
        col3, col4 = st.columns(2)
        vendor_name_col = col3.selectbox("Select vendor name column", vendor_columns)
        st.session_state["vendor_name_col"] = vendor_name_col
        email_col_merged = col4.selectbox("Select email column from merged data", df_columns)
        st.session_state["email_col_merged"] = email_col_merged
        col5, col6 = st.columns(2)
        delivery_date_col = col5.selectbox("Select delivery date column", df_columns)
        st.session_state["delivery_date_col"] = delivery_date_col
        product_col = col6.selectbox("Select product column", df_columns)
        st.session_state["product_col"] = product_col
        quantity_col = st.selectbox("Select quantity column", df_columns)
        st.session_state["quantity_col"] = quantity_col
        future_delivery_option = st.radio("Select future delivery option", ["Next Week", "Next Month", "No Delivery Date"])
        st.session_state["future_delivery_option"] = future_delivery_option
        unconfirmed_po_col = st.selectbox("Select unconfirmed PO column (boolean)", df_columns)
        st.session_state["unconfirmed_po_col"] = unconfirmed_po_col
        if main_field and vendor_field and vendor_name_col and email_col_merged and delivery_date_col and product_col and quantity_col and unconfirmed_po_col:
             mapping_main = {main_field: "Supplier No", unconfirmed_po_col: "Unconfirmed PO"}
             mapping_vendor = {vendor_field: "Supplier No", vendor_name_col: "Vendor Name"}
             return {
                 "main": mapping_main,
                 "vendor": mapping_vendor,
                 "merge_key": "Supplier No",
                 "vendor_name_col_merged": "Vendor Name",
                 "email_col_merged": email_col_merged,
                 "due_date_col": delivery_date_col,
                 "product_col": product_col,
                 "quantity_col": quantity_col,
                 "unconfirmed_po": "Unconfirmed PO"
             }
    return None

def email_settings_section():
    st.subheader("Email Settings")
    method = st.selectbox("Select email sending method", ['SMTP', 'API'])
    st.session_state["email_method"] = method
    if method == 'SMTP':
         server = st.text_input("SMTP Server", value="smtp.example.com")
         port = st.number_input("SMTP Port", value=587)
         username = st.text_input("SMTP Username")
         password = st.text_input("SMTP Password", type="password")
         settings = {"method": method, "server": server, "port": port, "username": username, "password": password}
    else:
         base_url = st.text_input("API Base URL", value="https://api.example.com")
         mailbox = st.text_input("Mailbox Number", value="123456")
         token = st.text_input("API Token", type="password")
         settings = {"method": method, "api_base_url": base_url, "mailbox_number": mailbox, "api_token": token}
    st.session_state['email_settings'] = settings

def email_content_section():
    st.subheader("Email Content")
    subject = st.text_input("Email Subject", value="Back Order Follow-up")
    body = st.text_area("Email Body", value="Dear [Recipient],\n\nWe would like to follow up on the following back orders for [VendorName]:\n\n")
    signature = st.text_input("Email Signature", value="Your default signature")
    st.session_state['email_content'] = {"subject": subject, "body": body, "signature": signature}

def filter_unconfirmed_section():
    st.subheader("Table Filter")
    filter_option = st.radio("Filter table by unconfirmed Purchase Order", ["Show All", "Unconfirmed Only"])
    st.session_state["filter_unconfirmed"] = filter_option
