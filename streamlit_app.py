import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder

def send_emails(grouped_data, smtp_server, smtp_port, smtp_username, smtp_password, company_name, email_subject, email_body):
    for vendor, group in grouped_data:
        # Prepare email content
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = ', '.join(group['email'].unique())
        message['Subject'] = email_subject
        
        personalized_body = email_body.replace("[Recipient]", ', '.join(group['email'].unique()))
        rows_text = group.to_string(index=False)
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
        email_body = st.text_area("Email Body", value="Dear [Recipient],\n\nWe would like to follow up on the following back orders:\n\n")
    
    with tab1:
        uploaded_file = st.file_uploader('Upload CSV', type=['csv'])
        if uploaded_file is not None:
            try:
                stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
                df = pd.read_csv(stringio)
                st.subheader('Uploaded Data')
                
                # Ensure required columns are present
                required_columns = {'vendor_no', 'email', 'product', 'quantity', 'due_date'}
                if not required_columns.issubset(df.columns):
                    st.error(f"CSV is missing required columns: {required_columns - set(df.columns)}")
                    return
                
                # Configure AgGrid for multi-selection
                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_selection('multiple', use_checkbox=True)
                grid_options = gb.build()
                
                grid_response = AgGrid(
                    df,
                    gridOptions=grid_options,
                    enable_enterprise_modules=False,
                    allow_unsafe_jscode=True,
                    update_mode='MODEL_CHANGED'
                )
                
                selected = grid_response['selected_rows']
                selected_df = pd.DataFrame(selected)
                
                if st.button('Follow-up'):
                    if not selected_df.empty:
                        grouped = selected_df.groupby('vendor_no')
                        # Validate email settings
                        if not all([smtp_server, smtp_port, smtp_username, smtp_password, company_name]):
                            st.error("Please provide all email settings in the Email Settings tab.")
                        else:
                            send_emails(grouped, smtp_server, smtp_port, smtp_username, smtp_password, company_name, email_subject, email_body)
                    else:
                        st.warning('Please select at least one row.')
            except Exception as e:
                st.error(f"Error processing the uploaded file: {e}")

if __name__ == '__main__':
    main()
