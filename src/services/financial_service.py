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

        tax_id = str(company_id)
        result = self.companies_info_df[self.companies_info_df['tax_id'] == tax_id]

        if result.empty:
            return None

        return result.iloc[0]

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
