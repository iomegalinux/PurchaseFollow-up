### Using the Application



 1. **Email Settings:**

    - Navigate to the **Email Settings** tab.

    - **SMTP Server:** Enter your SMTP server address (e.g., `smtp.gmail.com` for Gmail).

    - **SMTP Port:** Enter the port number (commonly `587` for TLS).

    - **SMTP Username:** Your email address used to send emails.

    - **SMTP Password:** The password for your email account.

    - **Your Company Name:** The name of your company to be included in the email signature.



 2. **Back Order Follow-up:**

    - Navigate to the **Back Order Follow-up** tab.

    - **Upload CSV:** Click the upload button and select your back order CSV file.

    - **View Data:** After uploading, the data will be displayed in an interactive grid.

    - **Select Orders:** Use the checkboxes to select the orders you want to follow up on.

    - **Send Follow-up Emails:** Click the **Follow-up** button to send emails to the selected vendors.



 ### CSV File Structure



 The application expects the uploaded CSV file to have the following columns:



 - **vendor_no:** A unique identifier for the vendor (e.g., `V12345`).

 - **email:** The vendor's email address (e.g., `vendor@example.com`).

 - **product:** The name of the back-ordered product (e.g., `Widget A`).

 - **quantity:** The quantity of the product back-ordered (e.g., `100`).

 - **due_date:** The expected fulfillment date in `YYYY-MM-DD` format (e.g., `2024-01-15`).



 **Example CSV:**



 | vendor_no | email               | product  | quantity | due_date   |

 |-----------|---------------------|----------|----------|------------|

 | V12345    | vendor1@example.com | Widget A | 100      | 2024-01-10 |

 | V67890    | vendor2@example.com | Widget B | 50       | 2024-01-15 |



 ### Email Settings Details



 To configure the email settings correctly, ensure the following:



 - **SMTP Server:** This is the address of your email provider's SMTP server. Common SMTP servers include:

   - Gmail: `smtp.gmail.com`

   - Outlook: `smtp.office365.com`

   - Yahoo: `smtp.mail.yahoo.com`



 - **SMTP Port:**

   - **TLS:** Use port `587`.

   - **SSL:** Use port `465`.



 - **SMTP Username:** This should be your full email address (e.g., `your_email@example.com`).



 - **SMTP Password:** For security reasons, consider using an [App Password](https://support.google.com/accounts/answer/185833) if you're using Gmail or similar services that offer app-specif 
 passwords.



 - **Your Company Name:** This will appear in the email signature to personalize the communication.



 **Important:** Ensure that your email account allows SMTP access. You may need to adjust security settings or enable access for less secure apps depending on your email provider.



 ## Best Practices



 - **Environment Variables:** For enhanced security, store sensitive information like SMTP credentials in environment variables instead of hardcoding them.



 - **Virtual Environments:** Always use a virtual environment to manage your project's dependencies and avoid conflicts.



 - **Dependency Management:** Regularly update your dependencies and use tools like `pip freeze` to maintain a `requirements.txt` file.



 ## Troubleshooting



 - **CSV Upload Issues:**

   - Ensure your CSV file has all the required columns: `vendor_no`, `email`, `product`, `quantity`, `due_date`.

   - Verify that the `due_date` is in the correct `YYYY-MM-DD` format.



 - **Email Sending Failures:**

   - Double-check your SMTP settings for accuracy.

   - Ensure that your network allows outbound SMTP connections.

   - Verify that your email account has the necessary permissions to send emails via SMTP.



 - **Application Errors:**

   - Check the terminal for any error messages when running the Streamlit app.

   - Use `flake8` to lint your code and identify any syntax issues:

     ```

     flake8 backorder_followup.py

     ```



 ## Contributing



 Contributions are welcome! Please fork the repository and submit a pull request with your improvements.



 ## License



 This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.