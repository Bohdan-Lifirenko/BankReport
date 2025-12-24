# src/services/data_preparer.py
import logging
from typing import Any, Optional

import pandas as pd

from src.services import FinancialService

logger = logging.getLogger(__name__)


class DataPreparer:
    """
    Prepares data for frontend consumption.
    Handles NaN, None, and empty string values.
    """

    def __init__(self, financial_service: FinancialService):
        self.financial_service = financial_service
        logger.info("DataPreparer instance created")

    def get_prepared_company_data(self, company_id: str) -> Optional[dict[str, Any]]:
        """
        Get company data with cleaned/sanitized values for frontend.
        Replaces NaN, None, and empty strings with a default value.
        """
        company_data = self.financial_service.get_company_data(company_id).to_dict()

        if company_data is None:
            return None

        return self._clean_data(company_data)

    def _clean_data(self, data: dict[str, Any], default_value: str = "") -> dict[str, Any]:
        """
        Clean dictionary values by replacing missing values.

        Handles:
        - None
        - NaN (float('nan'))
        - Empty strings or whitespace-only strings
        """
        cleaned = {}
        for key, value in data.items():
            cleaned[key] = self._clean_value(value, default_value)
        return cleaned

    def _clean_value(self, value: Any, default_value: str = "") -> Any:
        """
        Clean a single value.
        Returns default_value if value is missing/empty.
        """
        # Check for None or NaN
        if pd.isna(value):
            return default_value

        # Check for empty or whitespace-only strings
        if isinstance(value, str) and not value.strip():
            return default_value

        return value
