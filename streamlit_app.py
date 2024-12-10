import streamlit as st
import requests
import pandas as pd
from pandas import ExcelFile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder

def send_emails(
    grouped_data,
    email_method,
    company_name,
    smtp_server=None,
    smtp_port=None,
    smtp_username=None,
    smtp_password=None,
    api_base_url=None,
    api_token=None,
    mailbox_number=None,
    email_subject=None,
    email_body=None,
    email_col=None,
    contact_col_merged=None,
    vendor_name_col_merged=None,
    product_col=None,
    quantity_col=None,
    due_date_col=None,
    contact_col=None,
    vendor_name_col=None
):
    for vendor_email, group in grouped_data:
        # Prepare email content
        message = MIMEMultipart()
        message['From'] = smtp_username if email_method == "SMTP" else company_name
        message['To'] = vendor_email
        message['Subject'] = email_subject
        
        # Personalize the email body
        recipient_names = ', '.join(group[contact_col_merged].unique())
        personalized_body = email_body.replace("[Recipient]", recipient_names)
        personalized_body = personalized_body.replace("[VendorName]", str(group[vendor_name_col_merged].iloc[0]))
        rows_text = group[[product_col, quantity_col, due_date_col]].to_string(index=False)
        full_email_body = f"{personalized_body}\n\n{rows_text}"
        
        if email_method == "SMTP":
            # Attach the body to the email
            message.attach(MIMEText(full_email_body, 'plain'))
            # Send the email via SMTP
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(message)
                server.quit()
                st.success(f"Email sent to vendor {vendor_email} via SMTP")
            except Exception as e:
                st.error(f"Failed to send email to vendor {vendor_email} via SMTP: {e}")
        elif email_method == "API":
            # Send the email via API
            try:
                # Prepare API payload
                payload = {
                    "mailbox_number": mailbox_number,
                    "email_to": vendor_email,
                    "subject": message['Subject'],
                    "body": full_email_body,
                }

                headers = {
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json"
                }

                response = requests.post(f"{api_base_url}/send_email", json=payload, headers=headers)

                if response.status_code == 200:
                    st.success(f"Email sent to vendor {vendor_email} via API")
                else:
                    st.error(f"Failed to send email to vendor {vendor_email} via API. Status Code: {response.status_code}. Response: {response.text}")
            except Exception as e:
                st.error(f"Failed to send email to vendor {vendor_email} via API: {e}")

def main():
    st.set_page_config(layout="wide")
    st.title('Back Order Follow-up')
    
    tab1, tab2 = st.tabs(["Data Input", "Email Settings"])
    
    with tab1:
        st.header("Data Input")
        
        with st.expander('Upload Data Files'):
            uploaded_file = st.file_uploader('Upload Excel File', type=['xlsx'])
            vendor_file = st.file_uploader('Upload Vendor Information Excel File', type=['xlsx'], key='vendor_file')
        
        # Initialize email settings variables
        smtp_server = None
        smtp_port = None
        smtp_username = None
        smtp_password = None
        company_name = None
        email_subject = None
        email_body = None

        # Proceed only if both files are uploaded
        if uploaded_file is not None and vendor_file is not None:
            try:
                # Get sheet names from the uploaded Excel files
                main_excel_file = pd.ExcelFile(uploaded_file)
                main_sheet_names = main_excel_file.sheet_names

                vendor_excel_file = pd.ExcelFile(vendor_file)
                vendor_sheet_names = vendor_excel_file.sheet_names

                # Allow the user to select the sheet from each file
                with st.expander('Select Excel Sheets'):
                    main_sheet = st.selectbox(
                        "Select sheet from the main data file",
                        options=main_sheet_names,
                        key='main_sheet_selectbox'
                    )
                    vendor_sheet = st.selectbox(
                        "Select sheet from the vendor information file",
                        options=vendor_sheet_names,
                        key='vendor_sheet_selectbox'
                    )

                # Read the selected sheets into DataFrames
                df = pd.read_excel(
                    uploaded_file,
                    sheet_name=main_sheet,
                    header=0,
                    index_col=None
                )
                vendor_df = pd.read_excel(
                    vendor_file,
                    sheet_name=vendor_sheet,
                    header=0,
                    index_col=None
                )
            except Exception as e:
                st.error(f"Error processing the uploaded files: {e}")
                return

            with st.expander('BackOrder information Map Columns'):
                columns = df.columns.tolist()
                email_col = st.selectbox('Select the Email Column', options=columns, index=columns.index('email') if 'email' in columns else 0)
                vendor_col = st.selectbox('Select the Vendor Number Column', options=columns, index=columns.index('vendor_no') if 'vendor_no' in columns else 0)
                product_col = st.selectbox('Select the Product Column', options=columns, index=columns.index('product') if 'product' in columns else 0)
                quantity_col = st.selectbox('Select the Quantity Column', options=columns, index=columns.index('quantity') if 'quantity' in columns else 0)
                due_date_col = st.selectbox('Select the Due Date Column', options=columns, index=columns.index('due_date') if 'due_date' in columns else 0)

            if not all([email_col, vendor_col, product_col, quantity_col, due_date_col]):
                st.error("Please select all required columns in the 'Map Columns' section.")
                return

            with st.expander('Map Vendor Information Columns'):
                vendor_columns = vendor_df.columns.tolist()
                vendor_no_col_vendor = st.selectbox(
                    'Select the Vendor Number Column in Vendor Information File',
                    options=vendor_columns,
                    index=vendor_columns.index('vendor_no') if 'vendor_no' in vendor_columns else 0,
                    key='vendor_no_col_vendor'
                )
                vendor_name_col = st.selectbox(
                    'Select the Vendor Name Column',
                    options=vendor_columns,
                    index=vendor_columns.index('vendor_name') if 'vendor_name' in vendor_columns else 0
                )
                vendor_email_col = st.selectbox(
                    'Select the Vendor Email Column',
                    options=vendor_columns,
                    index=vendor_columns.index('email') if 'email' in vendor_columns else 0,
                    key='vendor_email_col'
                )
                contact_col = st.selectbox(
                    'Select the Contact Column',
                    options=vendor_columns,
                    index=vendor_columns.index('contact') if 'contact' in vendor_columns else 0
                )

            if not all([vendor_no_col_vendor, vendor_name_col, vendor_email_col, contact_col]):
                st.error("Please select all required columns in the 'Map Vendor Information Columns' section.")
                return

            # Convert key columns to string to ensure consistent data types
            df[vendor_col] = df[vendor_col].astype(str)
            vendor_df[vendor_no_col_vendor] = vendor_df[vendor_no_col_vendor].astype(str)

            # Merge the DataFrames on the vendor number
            # Convert vendor number columns to string to ensure consistent data types
            df[vendor_col] = df[vendor_col].astype(str)
            vendor_df[vendor_no_col_vendor] = vendor_df[vendor_no_col_vendor].astype(str)

            # Merge the DataFrames on the vendor number
            merged_df = pd.merge(
                df,
                vendor_df,
                left_on=vendor_col,
                right_on=vendor_no_col_vendor,
                how='left'
            )

            # Remove duplicates from the merged DataFrame
            merged_df = merged_df.drop_duplicates()

            # Use the original column names since we removed suffixes
            vendor_name_col_merged = vendor_name_col
            email_col_merged = vendor_email_col
            contact_col_merged = contact_col

            # Create a display DataFrame with all columns from the merged dataframe
            display_df = merged_df.copy()

            # Check for duplicate columns in display_df
            duplicated_columns = display_df.columns[display_df.columns.duplicated()].tolist()
            if duplicated_columns:
                # Identify the sources of the duplicate columns
                duplicate_details = []
                for col in duplicated_columns:
                    sources = []
                    if col in df.columns:
                        sources.append("Main Data")
                    if col in vendor_df.columns:
                        sources.append("Vendor Information")
                    duplicate_details.append(f"- '{col}' selected from: {', '.join(sources)}")
                
                st.error("You have selected duplicate columns, resulting in duplicate names in the display.")
                st.write("Duplicate columns and their sources:")
                for detail in duplicate_details:
                    st.write(detail)
                st.stop()

            # Configure AgGrid for multi-selection
            gb = GridOptionsBuilder.from_dataframe(display_df)
            gb.configure_selection('multiple', use_checkbox=True)
            grid_options = gb.build()

            # Display the data in AgGrid
            grid_response = AgGrid(
                display_df,
                gridOptions=grid_options,
                height=500,  # Set the desired height in pixels
                enable_enterprise_modules=False,
                allow_unsafe_jscode=True,
                update_mode='MODEL_CHANGED'
            )

            selected = grid_response['selected_rows']
            selected_df = pd.DataFrame(selected)

            if st.button('Follow-up'):
                if not selected_df.empty:
                    grouped = selected_df.groupby(email_col_merged)
                    if email_method == "SMTP":
                        # Validate SMTP email settings
                        if not all([smtp_server, smtp_port, smtp_username, smtp_password, company_name]):
                            st.error("Please provide all SMTP email settings in the Email Settings tab.")
                        else:
                            send_emails(
                                grouped_data=grouped,
                                email_method=email_method,
                                company_name=company_name,
                                smtp_server=smtp_server,
                                smtp_port=smtp_port,
                                smtp_username=smtp_username,
                                smtp_password=smtp_password,
                                api_base_url=None,
                                api_token=None,
                                mailbox_number=None,
                                email_subject=email_subject,
                                email_body=email_body,
                                email_col=email_col_merged,
                                contact_col_merged=contact_col_merged,
                                vendor_name_col_merged=vendor_name_col_merged,
                                product_col=product_col,
                                quantity_col=quantity_col,
                                due_date_col=due_date_col,
                                contact_col=contact_col,
                                vendor_name_col=vendor_name_col
                            )
                    elif email_method == "API":
                        # Validate API email settings
                        if not all([api_base_url, api_token, mailbox_number]):
                            st.error("Please provide all API email settings in the Email Settings tab.")
                        else:
                            send_emails(
                                grouped_data=grouped,
                                email_method=email_method,
                                company_name=None,
                                smtp_server=None,
                                smtp_port=None,
                                smtp_username=None,
                                smtp_password=None,
                                api_base_url=api_base_url,
                                api_token=api_token,
                                mailbox_number=mailbox_number,
                                email_subject=email_subject,
                                email_body=email_body,
                                email_col=email_col_merged,
                                contact_col_merged=contact_col_merged,
                                vendor_name_col_merged=vendor_name_col_merged,
                                product_col=product_col,
                                quantity_col=quantity_col,
                                due_date_col=due_date_col,
                                contact_col=contact_col,
                                vendor_name_col=vendor_name_col
                            )
                else:
                    st.warning('Please select at least one row.')
        else:
            st.warning("Please upload both the main data file and the vendor information file.")

    with tab2:
        st.header("Email Configuration")

        with st.expander('Email Settings'):
            email_method = st.radio("Select Email Method", options=["SMTP", "API"], index=0)
            
            if email_method == "SMTP":
                smtp_server = st.text_input("SMTP Server", value="smtp.example.com")
                if 'office365.com' in smtp_server:
                    st.warning("If you are using two-factor authentication with Office 365, please provide an application password in the SMTP password email settings.")
                smtp_port = st.number_input("SMTP Port", value=587, step=1)
                smtp_username = st.text_input("SMTP Username", value="your_email@example.com")
                smtp_password = st.text_input("SMTP Password", type="password")
                company_name = st.text_input("Your Company Name", value="Your Company")
            elif email_method == "API":
                api_base_url = st.text_input("API Base URL", value="https://api.example.com")
                api_token = st.text_input("API Token", type="password")
                mailbox_number = st.text_input("Mailbox Number", value="123456")

        with st.expander('Email Content'):
            email_subject = st.text_input("Email Subject", value="Back Order Follow-up")
            email_body = st.text_area(
                "Email Body",
                value="Dear [Recipient],\n\nWe would like to follow up on the following back orders for [VendorName]:\n\n"
            )

if __name__ == '__main__':
    main()
