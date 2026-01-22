"""Base class for data exporters."""

from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class BaseExporter(ABC):
    """Abstract base class for all data exporters."""

    @abstractmethod
    def export(self, data: pd.DataFrame, config: Dict[str, Any]) -> None:
        """
        Export data to a destination.

        Args:
            data: DataFrame to export
            config: Export configuration containing destination and options

        Raises:
            ExportError: If export fails
        """
        pass

    @classmethod
    def get_type(cls) -> str:
        """
        Return the exporter type identifier.

        By default, removes 'Exporter' suffix and converts to lowercase.
        Override this method to customize the type identifier.

        Returns:
            String identifier for this exporter type
        """
        name = cls.__name__
        if name.endswith("Exporter"):
            name = name[:-8]  # Remove "Exporter" suffix
        return name.lower()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
