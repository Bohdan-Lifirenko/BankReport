from typing import Optional

import pandas as pd

from src.services import DataLoader


class FinancialService:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def get_company_data(self, company_id: str) -> Optional[pd.Series]:

        return self.data_loader.get_company_data(company_id)
