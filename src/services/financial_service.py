from typing import Optional, List, Dict

import pandas as pd

from src.services import DataLoader


class FinancialService:
    def __init__(self, companies_info_path: str, fin_records_path: str):
        self.companies_info_df = DataLoader.load_companies_info_data(companies_info_path)
        self.fin_records_df = DataLoader.load_fin_records_data(fin_records_path)

    # Financial indicator codes
    CODE_REVENUE = 2000
    CODE_ASSETS = 1300
    CODE_EQUITY = 1495

    def get_company_data(self, company_id: str) -> Optional[pd.Series]:
        if self.company_exists(company_id):
            return self.companies_info_df[self.companies_info_df['tax_id'] == company_id].iloc[0]
        return None

    def get_revenue_data(self, tax_id: str) -> Optional[pd.DataFrame]:

        revenue_df = self._get_financial_data_by_code(
            tax_id,
            self.CODE_REVENUE
        )[['my_date', 'value']].copy()
        if revenue_df.empty:
            return None

        return revenue_df

    def get_balance_data(self, tax_id: str, date: str) -> Dict:
        assets_df = self._get_financial_data_by_code(tax_id, self.CODE_ASSETS)
        equity_df = self._get_financial_data_by_code(tax_id, self.CODE_EQUITY)

        assets_row = assets_df[assets_df['my_date'] == date]
        equity_row = equity_df[equity_df['my_date'] == date]

        assets_value = float(assets_row.iloc[0]['value']) if not assets_row.empty else None
        equity_value = float(equity_row.iloc[0]['value']) if not equity_row.empty else None

        # Calculate liabilities
        liabilities = None
        if assets_value is not None and equity_value is not None:
            liabilities = self._calculate_liabilities(assets_value, equity_value)

        return {
            'assets': assets_value,
            'equity': equity_value,
            'liabilities': liabilities,
            'date': date
        }

    def get_available_dates(self, tax_id: str) -> List[str]:
        """
        Get all available financial reporting dates for a company.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            List of date strings in YYYY-MM-DD format, sorted descending
        """
        tax_id = str(tax_id).strip()
        company_data = self.fin_records_df[self.fin_records_df['tax_id'] == tax_id]

        if company_data.empty:
            return []

        # Get unique dates, convert to string format, and sort descending
        dates = company_data['my_date'].dropna().unique()
        date_strings = [pd.Timestamp(d).strftime('%Y-%m-%d') for d in dates]
        return sorted(date_strings, reverse=True)

    def company_exists(self, tax_id: str) -> bool:
        tax_id = str(tax_id).strip()

        return not self.companies_info_df[self.companies_info_df['tax_id'] == tax_id].empty

    def _get_financial_data_by_code(self, tax_id: str, code: int) -> pd.DataFrame:
        tax_id = str(tax_id).strip()

        return self.fin_records_df[
            (self.fin_records_df['tax_id'] == tax_id) &
            (self.fin_records_df['code'] == code)
            ].copy()

    def _calculate_liabilities(self, assets: float, equity: float) -> float:
        """
        Calculate liabilities from assets and equity.

        Liabilities = Assets - Equity

        Args:
            assets: Total assets value
            equity: Total equity value

        Returns:
            Calculated liabilities value
        """
        return assets - equity
