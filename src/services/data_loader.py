import os
import pandas as pd
from pandas import DataFrame


class DataLoader:

    @staticmethod
    def load_companies_info_data(companies_info_path: str) -> DataFrame:
        if not os.path.exists(companies_info_path):
            raise FileNotFoundError(f"Companies info file not found: {companies_info_path}")

        companies_info_df = pd.read_csv(
            companies_info_path,
            dtype={
                'tax_id': str,
                'name': str,
                'kved': str,
                'opf_code': str,
                'katottg': str,
                'region_code': str,
                'local_code': str
            }
        )

        # Validate firms columns
        required_firms_cols = ['tax_id', 'name', 'kved', 'opf_code',
                               'katottg', 'region_code', 'local_code']
        missing_cols = set(required_firms_cols) - set(companies_info_df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns in firms.csv: {missing_cols}")

        # Strip whitespace for consistent lookups
        companies_info_df['tax_id'] = companies_info_df['tax_id'].str.strip()
        companies_info_df['name'] = companies_info_df['name'].str.strip()
        companies_info_df['kved'] = companies_info_df['kved'].str.strip()
        companies_info_df['opf_code'] = companies_info_df['opf_code'].str.strip()
        companies_info_df['katottg'] = companies_info_df['katottg'].str.strip()
        companies_info_df['region_code'] = companies_info_df['region_code'].str.strip()
        companies_info_df['local_code'] = companies_info_df['local_code'].str.strip()

        return companies_info_df

    @staticmethod
    def load_fin_records_data(fin_records: str) -> DataFrame:
        if not os.path.exists(fin_records):
            raise FileNotFoundError(f"Financial values file not found: {fin_records}")

        fin_records_df = pd.read_csv(
            fin_records,
            dtype={
                'tax_id': str,
                'code': int,
                'value': float,
                'c_doc_sub': str
            },
            parse_dates=['my_date']  # Parse date column automatically
        )

        # Validate fin_values columns
        required_fin_cols = ['tax_id', 'my_date', 'code', 'value', 'c_doc_sub']
        missing_cols = set(required_fin_cols) - set(fin_records_df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns in fin_values.csv: {missing_cols}")

        # Strip whitespace from tax_id for consistent lookups
        fin_records_df['tax_id'] = fin_records_df['tax_id'].str.strip()

        # Sort by date for better performance
        fin_records_df = fin_records_df.sort_values(['tax_id', 'my_date'])

        return fin_records_df


