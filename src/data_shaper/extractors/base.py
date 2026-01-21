"""Base class for data extractors."""

from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class BaseExtractor(ABC):
    """Abstract base class for all data extractors."""

    @abstractmethod
    def extract(self, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data from a source and return as DataFrame.

        Args:
            config: Extraction configuration containing source and options

        Returns:
            DataFrame containing extracted data

        Raises:
            ExtractionError: If extraction fails
        """
        pass

    @classmethod
    def get_type(cls) -> str:
        """
        Return the extractor type identifier.

        By default, removes 'Extractor' suffix and converts to lowercase.
        Override this method to customize the type identifier.

        Returns:
            String identifier for this extractor type
        """
        name = cls.__name__
        if name.endswith("Extractor"):
            name = name[:-9]  # Remove "Extractor" suffix
        return name.lower()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
