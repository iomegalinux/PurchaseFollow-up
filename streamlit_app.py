import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from data_processing import (
    load_excel_file, map_columns,
    merge_dataframes, filter_late_orders
)
from email_sender import send_emails
from ui_elements import (
    upload_files, select_excel_sheets,
    column_mapping_section, email_settings_section,
    email_content_section
)

def display_data(df):
    grid_options = GridOptionsBuilder.from_dataframe(df)
    grid_options.configure_selection('multiple', use_checkbox=True)
    grid_options = grid_options.build()

    grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)
    selected_rows = grid_response.get('selected_rows')
    if selected_rows is None:
         return df
    if isinstance(selected_rows, list) and len(selected_rows) > 0:
         return pd.DataFrame(selected_rows)
    elif isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
         return selected_rows
    return df

def main():
    st.set_page_config(layout="wide")
    st.title('Back Order Follow-up')
    
    tab1, tab2 = st.tabs(["Data Input", "Email Settings"])
    
    with tab1:
        st.header("Data Input")
        with st.expander('Upload Data Files'):
            uploaded_file, vendor_file = upload_files()
        
        if uploaded_file and vendor_file:
            main_sheet, vendor_sheet = select_excel_sheets(uploaded_file, vendor_file)
            df = load_excel_file(uploaded_file, main_sheet)
            vendor_df = load_excel_file(vendor_file, vendor_sheet)

            if df is not None and vendor_df is not None:
                column_mappings = column_mapping_section(df.columns.tolist(), vendor_df.columns.tolist())
                if column_mappings:
                    df = map_columns(df, column_mappings['main'])
                    vendor_df = map_columns(vendor_df, column_mappings['vendor'])
                    merged_df = merge_dataframes(df, vendor_df, column_mappings['merge_key'])

                    show_late_only = st.checkbox('Show Late Only', value=False)
                    if show_late_only:
                        merged_df = filter_late_orders(merged_df, column_mappings['due_date_col'])
                    if merged_df is None:
                        st.error("Merging data failed. Please verify merge key exists in both files.")
                        return

                    email_settings = st.session_state.get('email_settings', {})
                    if (email_settings.get('method') == 'SMTP' and (not email_settings.get('username') or not email_settings.get('password') or not email_settings.get('server'))) or \
                       (email_settings.get('method') == 'API' and (not email_settings.get('api_base_url') or not email_settings.get('mailbox_number') or not email_settings.get('api_token'))):
                        st.warning("Please complete email configuration in the Email Settings tab before proceeding.")
                    else:
                        selected_df = display_data(merged_df)
                        if selected_df is not None and st.button('Follow-up'):
                            email_content = st.session_state.get('email_content', {})
                            columns_info = column_mappings
                            grouped = selected_df.groupby(column_mappings['email_col_merged'])
                            send_emails(grouped, email_settings['method'], email_settings, email_content, columns_info)
        else:
            st.warning("Please upload both the main data file and the vendor information file.")
    
    with tab2:
        st.header("Email Configuration")
        email_settings_section()
        email_content_section()

if __name__ == '__main__':
    main()
