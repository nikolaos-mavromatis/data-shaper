"""Data cleaning transformers."""

from typing import Any, Dict, List

import pandas as pd

from data_shaper.utils.exceptions import TransformationError
from data_shaper.utils.logger import get_logger
from data_shaper.transformers.base import BaseTransformer

logger = get_logger(__name__)


class RemoveNullsTransformer(BaseTransformer):
    """Remove rows with null values in specified columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Remove rows containing null values.

        Config options:
            - columns: List of columns to check for nulls (default: all columns)
            - how: 'any' or 'all' (default: 'any')

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with null rows removed
        """
        try:
            columns = config.get("columns")
            how = config.get("how", "any")

            initial_count = len(df)
            df_cleaned = df.dropna(subset=columns, how=how)
            removed_count = initial_count - len(df_cleaned)

            logger.info(f"Removed {removed_count} rows with null values")
            return df_cleaned

        except Exception as e:
            raise TransformationError(f"Failed to remove nulls: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "remove_nulls"


class DeduplicateTransformer(BaseTransformer):
    """Remove duplicate rows."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Remove duplicate rows.

        Config options:
            - columns: Columns to consider for duplicates (default: all columns)
            - keep: 'first', 'last', or False (default: 'first')

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with duplicates removed
        """
        try:
            columns = config.get("columns")
            keep = config.get("keep", "first")

            initial_count = len(df)
            df_deduped = df.drop_duplicates(subset=columns, keep=keep)
            removed_count = initial_count - len(df_deduped)

            logger.info(f"Removed {removed_count} duplicate rows")
            return df_deduped

        except Exception as e:
            raise TransformationError(f"Failed to deduplicate: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "deduplicate"


class FixTypesTransformer(BaseTransformer):
    """Fix/convert column data types."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert column data types.

        Config options:
            - dtypes: Dictionary mapping column names to target types
                     (e.g., {'col1': 'int64', 'col2': 'float', 'col3': 'datetime64'})

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with converted types
        """
        try:
            dtypes = config.get("dtypes", {})

            for column, dtype in dtypes.items():
                if column not in df.columns:
                    logger.warning(
                        f"Column '{column}' not found, skipping type conversion"
                    )
                    continue

                if dtype == "datetime64":
                    df[column] = pd.to_datetime(df[column])
                else:
                    df[column] = df[column].astype(dtype)

                logger.debug(f"Converted column '{column}' to type '{dtype}'")

            return df

        except Exception as e:
            raise TransformationError(f"Failed to fix types: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "fix_types"


class FillNullsTransformer(BaseTransformer):
    """Fill null values with specified values."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Fill null values.

        Config options:
            - fill_values: Dictionary mapping column names to fill values
            - method: Fill method ('ffill', 'bfill') if fill_values not provided

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with nulls filled
        """
        try:
            fill_values = config.get("fill_values")
            method = config.get("method")

            if fill_values:
                df_filled = df.fillna(fill_values)
                logger.info(f"Filled nulls with specified values")
            elif method:
                df_filled = df.fillna(method=method)
                logger.info(f"Filled nulls using method: {method}")
            else:
                raise TransformationError(
                    "Either 'fill_values' or 'method' must be specified"
                )

            return df_filled

        except Exception as e:
            raise TransformationError(f"Failed to fill nulls: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "fill_nulls"
