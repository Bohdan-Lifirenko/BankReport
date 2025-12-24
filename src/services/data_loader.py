import logging
import os
from typing import Optional

import pandas as pd

# Configure logger for this module
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        self.companies_info_df: Optional[pd.DataFrame] = None
        self._is_loaded: bool = False
        logger.info("DataLoader instance created")

    def load_data(self, companies_info_path: str) -> None:
        """
        Load CSV data files into memory with proper dtype handling.
        """
        try:
            self._load_companies_info_data(companies_info_path)

            self._is_loaded = True
            logger.info("Data loading completed successfully")

        except FileNotFoundError as e:
            logger.exception("File not found error during data loading")
            raise
        except ValueError as e:
            logger.exception("Data validation error during data loading")
            raise
        except Exception as e:
            logger.exception("Unexpected error during data loading")
            raise

    def _load_companies_info_data(self, companies_info_path: str) -> None:
        if not os.path.exists(companies_info_path):
            logger.error(f"Companies info file not found: {companies_info_path}")
            raise FileNotFoundError(f"Companies info file not found: {companies_info_path}")

        # Load firms.csv
        logger.info(f"Loading firms data from: {companies_info_path}")
        self.firms_df = pd.read_csv(
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
        missing_cols = set(required_firms_cols) - set(self.firms_df.columns)
        if missing_cols:
            logger.error(f"Missing required columns in firms.csv: {missing_cols}")
            raise ValueError(f"Missing required columns in firms.csv: {missing_cols}")

        logger.debug("Stripping whitespace from firms data columns")
        # Strip whitespace for consistent lookups
        self.firms_df['tax_id'] = self.firms_df['tax_id'].str.strip()
        self.firms_df['name'] = self.firms_df['name'].str.strip()
        self.firms_df['kved'] = self.firms_df['kved'].str.strip()
        self.firms_df['opf_code'] = self.firms_df['opf_code'].str.strip()
        self.firms_df['katottg'] = self.firms_df['katottg'].str.strip()
        self.firms_df['region_code'] = self.firms_df['region_code'].str.strip()
        self.firms_df['local_code'] = self.firms_df['local_code'].str.strip()

        logger.info(f"Successfully loaded {len(self.firms_df)} companies")



    def is_loaded(self) -> bool:
        """
        Check if data has been loaded.

        Returns:
            True if data is loaded, False otherwise
        """
        is_loaded = self._is_loaded and self.firms_df is not None
        logger.debug(f"Data loaded status: {is_loaded}")
        return is_loaded

    def get_company_data(self, company_id: str) -> Optional[pd.Series]:
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(company_id)
        result = self.firms_df[self.firms_df['tax_id'] == tax_id]

        if result.empty:
            return None

        return result.iloc[0]

