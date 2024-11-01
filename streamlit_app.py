import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder

def send_emails(
    grouped_data,
    smtp_server,
    smtp_port,
    smtp_username,
    smtp_password,
    company_name,
    email_subject,
    email_body,
    email_col,
    product_col,
    quantity_col,
    due_date_col,
    contact_col,
    vendor_name_col
):
    for vendor, group in grouped_data:
        # Prepare email content
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = ', '.join(group[email_col].unique())
        message['Subject'] = email_subject
        
        # Personalize the email body
        recipient_names = ', '.join(group[contact_col].unique())
        personalized_body = email_body.replace("[Recipient]", recipient_names)
        personalized_body = personalized_body.replace("[VendorName]", str(group[vendor_name_col].iloc[0]))
        rows_text = group[[product_col, quantity_col, due_date_col]].to_string(index=False)
        full_email_body = f"{personalized_body}\n\n{rows_text}"
        
        message.attach(MIMEText(full_email_body, 'plain'))
        
        # Send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
            server.quit()
            st.success(f"Emails sent to vendor {vendor}")
        except Exception as e:
            st.error(f"Failed to send email to vendor {vendor}: {e}")

def main():
    st.set_page_config(layout="wide")
    st.title('Back Order Follow-up')
    
    tab1, tab2 = st.tabs(["Data Input", "Email Settings"])
    
    with tab2:
        st.header("Email Configuration")
        smtp_server = st.text_input("SMTP Server", value="smtp.example.com")
        smtp_port = st.number_input("SMTP Port", value=587, step=1)
        smtp_username = st.text_input("SMTP Username", value="your_email@example.com")
        smtp_password = st.text_input("SMTP Password", type="password")
        company_name = st.text_input("Your Company Name", value="Your Company")
        email_subject = st.text_input("Email Subject", value="Back Order Follow-up")
        email_body = st.text_area(
            "Email Body",
            value="Dear [Recipient],\n\nWe would like to follow up on the following back orders for [VendorName]:\n\n"
        )
    
    with tab1:
        uploaded_file = st.file_uploader('Upload Excel File', type=['xlsx'])
        vendor_file = st.file_uploader('Upload Vendor Information Excel File', type=['xlsx'], key='vendor_file')
        
        # Check if both files are uploaded
        if uploaded_file is not None and vendor_file is not None:
            try:
                # Read the main data file
                df = pd.read_excel(uploaded_file)
                # Read the vendor information file
                vendor_df = pd.read_excel(vendor_file)
            except Exception as e:
                st.error(f"Error processing the uploaded files: {e}")
                return
        else:
            st.warning("Please upload both the main data file and the vendor information file.")
            return

        st.subheader('Map Columns')

        columns = df.columns.tolist()
        email_col = st.selectbox('Select the Email Column', options=columns, index=columns.index('email') if 'email' in columns else 0)
        vendor_col = st.selectbox('Select the Vendor Number Column', options=columns, index=columns.index('vendor_no') if 'vendor_no' in columns else 0)
        product_col = st.selectbox('Select the Product Column', options=columns, index=columns.index('product') if 'product' in columns else 0)
        quantity_col = st.selectbox('Select the Quantity Column', options=columns, index=columns.index('quantity') if 'quantity' in columns else 0)
        due_date_col = st.selectbox('Select the Due Date Column', options=columns, index=columns.index('due_date') if 'due_date' in columns else 0)

        if not all([
            email_col,
            vendor_col,
            product_col,
            quantity_col,
            due_date_col
        ]):
            st.error("Please select all required columns in both 'Map Columns' sections.")
            return

                st.subheader('Map Vendor Information Columns')

                # Get the list of columns from the vendor DataFrame
                vendor_columns = vendor_df.columns.tolist()

                # Add select boxes for mapping vendor information columns
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

                # Ensure all vendor columns have been selected
                if not all([vendor_no_col_vendor, vendor_name_col, vendor_email_col, contact_col]):
                    st.error("Please select all required columns in the 'Map Vendor Information Columns' section.")
                    return

                # Merge the DataFrames on the vendor number
                merged_df = pd.merge(
                    df,
                    vendor_df,
                    left_on=vendor_col,         # Vendor number column from the main data
                    right_on=vendor_no_col_vendor,  # Vendor number column from the vendor info
                    how='left'
                )

                # Update the email column to use the vendor email from the merged DataFrame
                email_col = vendor_email_col

                # Create a display DataFrame with relevant columns
                display_df = merged_df[[vendor_col, product_col, quantity_col, due_date_col, vendor_name_col, email_col, contact_col]].copy()

                # Configure AgGrid for multi-selection
                gb = GridOptionsBuilder.from_dataframe(display_df)
                gb.configure_selection('multiple', use_checkbox=True)
                grid_options = gb.build()

                # Display the data in AgGrid
                grid_response = AgGrid(
                    display_df,
                    gridOptions=grid_options,
                    enable_enterprise_modules=False,
                    allow_unsafe_jscode=True,
                    update_mode='MODEL_CHANGED'
                )

                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)

                if st.button('Follow-up'):
                    if not selected_df.empty:
                        grouped = selected_df.groupby(vendor_col)
                        # Validate email settings
                        if not all([smtp_server, smtp_port, smtp_username, smtp_password, company_name]):
                            st.error("Please provide all email settings in the Email Settings tab.")
                        else:
                            send_emails(
                                grouped, smtp_server, smtp_port, smtp_username, smtp_password,
                                company_name, email_subject, email_body, email_col,
                                product_col, quantity_col, due_date_col, contact_col, vendor_name_col
                            )
                    else:
                        st.warning('Please select at least one row.')

if __name__ == '__main__':
    main()
