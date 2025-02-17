import pandas as pd
import streamlit as st

def load_excel_file(uploaded_file, sheet_name):
    try:
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def map_columns(df, mappings):
    df = df.rename(columns=mappings)
    return df

def merge_dataframes(df1, df2, merge_key):
    if merge_key not in df1.columns:
        import streamlit as st
        st.error(f"Merge key '{merge_key}' not found in main dataframe columns: {df1.columns.tolist()}")
        return None
    if merge_key not in df2.columns:
        import streamlit as st
        st.error(f"Merge key '{merge_key}' not found in vendor dataframe columns: {df2.columns.tolist()}")
        return None
    df1[merge_key] = df1[merge_key].astype(str)
    df2[merge_key] = df2[merge_key].astype(str)
    merged_df = pd.merge(df1, df2, on=merge_key, how='left', suffixes=('', '_vendor'))
    return merged_df

def filter_late_orders(df, due_date_col):
    df[due_date_col] = pd.to_datetime(df[due_date_col], errors='coerce')
    today = pd.Timestamp.now().normalize()
    filtered_df = df[df[due_date_col] < today]
    return filtered_df
