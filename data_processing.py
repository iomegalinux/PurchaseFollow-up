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
    merged_df = pd.merge(df1, df2, on=merge_key, how='left', suffixes=('', '_vendor'))
    return merged_df

def filter_late_orders(df, due_date_col):
    df[due_date_col] = pd.to_datetime(df[due_date_col], errors='coerce')
    today = pd.Timestamp.now().normalize()
    filtered_df = df[df[due_date_col] < today]
    return filtered_df
