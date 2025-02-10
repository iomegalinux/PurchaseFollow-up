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
    vendor_sheet = st.selectbox("Select sheet from vendor info file", vendor_sheets)
    return main_sheet, vendor_sheet

def column_mapping_section(df_columns, vendor_columns):
    st.subheader("Field Mapping")
    main_field = st.selectbox("Select main file key for mapping 'Supplier No'", df_columns)
    vendor_field = st.selectbox("Select vendor file key for mapping 'Supplier No'", vendor_columns)
    email_col_merged = st.selectbox("Select email column from merged data", df_columns)
    delivery_date_col = st.selectbox("Select delivery date column", df_columns)
    if main_field and vendor_field and email_col_merged and delivery_date_col:
         mapping_main = {main_field: "Supplier No"}
         mapping_vendor = {vendor_field: "Supplier No"}
         return {
             "main": mapping_main,
             "vendor": mapping_vendor,
             "merge_key": "Supplier No",
             "email_col_merged": email_col_merged,
             "due_date_col": delivery_date_col
         }
    return None

def email_settings_section():
    st.subheader("Email Settings")
    method = st.selectbox("Select email sending method", ['SMTP', 'API'])
    if method == 'SMTP':
         server = st.text_input("SMTP Server", value="smtp.example.com")
         port = st.number_input("SMTP Port", value=587)
         username = st.text_input("SMTP Username")
         password = st.text_input("SMTP Password", type="password")
         settings = {"method": method, "server": server, "port": port, "username": username, "password": password}
    else:
         api_key = st.text_input("API Key")
         api_url = st.text_input("API URL")
         settings = {"method": method, "api_key": api_key, "api_url": api_url}
    st.session_state['email_settings'] = settings

def email_content_section():
    st.subheader("Email Content")
    subject = st.text_input("Email Subject", value="Back Order Follow-up")
    body = st.text_area("Email Body", value="Dear [Recipient],\n\nWe would like to follow up on the following back orders for [VendorName]:\n\n")
    st.session_state['email_content'] = {"subject": subject, "body": body}
