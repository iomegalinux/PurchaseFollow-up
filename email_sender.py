import streamlit as st
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_emails(
    grouped_data,
    email_method,
    email_settings,
    email_content,
    columns_info
):
    for vendor_email, group in grouped_data:
        subject, body = prepare_email_content(group, email_content, columns_info)
        
        if email_method == "SMTP":
            send_email_smtp(vendor_email, subject, body, email_settings)
        elif email_method == "API":
            send_email_api(vendor_email, subject, body, email_settings)
        else:
            st.error("Invalid email method selected.")

def prepare_email_content(group, email_content, columns_info):
    recipient_names = ', '.join(group[columns_info['contact_col_merged']].unique())
    vendor_name = str(group[columns_info['vendor_name_col_merged']].iloc[0])
    personalized_body = email_content['body'].replace("[Recipient]", recipient_names)
    personalized_body = personalized_body.replace("[VendorName]", vendor_name)
    rows_text = group[
        [columns_info['product_col'], columns_info['quantity_col'], columns_info['due_date_col']]
    ].to_string(index=False)
    full_body = f"{personalized_body}\n\n{rows_text}\n\n{email_content['signature']}"
    return email_content['subject'], full_body

def send_email_smtp(vendor_email, subject, body, email_settings):
    message = MIMEMultipart()
    message['From'] = email_settings['smtp_username']
    message['To'] = vendor_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port'])
        server.starttls()
        server.login(email_settings['smtp_username'], email_settings['smtp_password'])
        server.send_message(message)
        server.quit()
        st.success(f"Email sent to {vendor_email} via SMTP")
    except Exception as e:
        st.error(f"Failed to send email to {vendor_email}: {e}")

def send_email_api(vendor_email, subject, body, email_settings):
    url = f"{email_settings['api_base_url']}/channels/{email_settings['mailbox_number']}/messages"
    vendor_email = vendor_email.strip()
    archive_flag = vendor_email != "achat@gilbert-tech.com"
    payload = {
        "options": {"archive": archive_flag},
        "to": [vendor_email],
        "sender_name": "Achat",
        "subject": subject,
        "body": body,
        "should_add_default_signature": False,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {email_settings['api_token']}",
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 202:
            st.success(f"Email sent to {vendor_email} via Front API")
        else:
            st.error(f"Failed to send email to {vendor_email} via API. Status Code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        st.error(f"Failed to send email to {vendor_email} via API: {e}")