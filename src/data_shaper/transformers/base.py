"""Base class for data transformers."""

from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class BaseTransformer(ABC):
    """Abstract base class for all data transformers."""

    @abstractmethod
    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Transform a DataFrame based on configuration.

        Args:
            df: Input DataFrame
            config: Transformation configuration parameters

        Returns:
            Transformed DataFrame

        Raises:
            TransformationError: If transformation fails
        """
        pass

    @classmethod
    def get_type(cls) -> str:
        """
        Return the transformer type identifier.

        By default, removes 'Transformer' suffix and converts to lowercase.
        Override this method to customize the type identifier.

        Returns:
            String identifier for this transformer type
        """
        name = cls.__name__
        if name.endswith("Transformer"):
            name = name[:-11]  # Remove "Transformer" suffix
        return name.lower()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
