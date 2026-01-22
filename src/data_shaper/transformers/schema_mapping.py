"""Schema and column mapping transformers."""

from typing import Any, Dict, List

import pandas as pd

from ..utils.exceptions import TransformationError
from ..utils.logger import get_logger
from .base import BaseTransformer

logger = get_logger(__name__)


class RenameColumnsTransformer(BaseTransformer):
    """Rename columns based on mapping."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Rename columns.

        Config options:
            - mapping: Dictionary mapping old names to new names
                      (e.g., {'old_name': 'new_name'})

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with renamed columns
        """
        try:
            mapping = config.get("mapping", {})

            if not mapping:
                raise TransformationError("Column mapping is required")

            df_renamed = df.rename(columns=mapping)
            renamed_cols = [old for old in mapping.keys() if old in df.columns]

            logger.info(f"Renamed {len(renamed_cols)} columns")
            return df_renamed

        except Exception as e:
            raise TransformationError(f"Failed to rename columns: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "rename_columns"


class SelectColumnsTransformer(BaseTransformer):
    """Select specific columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Select specific columns from DataFrame.

        Config options:
            - columns: List of column names to keep

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with selected columns only
        """
        try:
            columns = config.get("columns", [])

            if not columns:
                raise TransformationError("Column list is required")

            # Filter to only existing columns
            existing_columns = [col for col in columns if col in df.columns]
            missing_columns = [col for col in columns if col not in df.columns]

            if missing_columns:
                logger.warning(f"Columns not found: {missing_columns}")

            df_selected = df[existing_columns]
            logger.info(f"Selected {len(existing_columns)} columns")
            return df_selected

        except Exception as e:
            raise TransformationError(f"Failed to select columns: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "select_columns"


class ReorderColumnsTransformer(BaseTransformer):
    """Reorder columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Reorder columns.

        Config options:
            - columns: List of column names in desired order
            - append_remaining: If True, append columns not in list at end (default: False)

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with reordered columns
        """
        try:
            columns = config.get("columns", [])
            append_remaining = config.get("append_remaining", False)

            if not columns:
                raise TransformationError("Column order list is required")

            # Filter to only existing columns
            existing_ordered = [col for col in columns if col in df.columns]

            if append_remaining:
                remaining = [col for col in df.columns if col not in existing_ordered]
                final_order = existing_ordered + remaining
            else:
                final_order = existing_ordered

            df_reordered = df[final_order]
            logger.info("Reordered columns")
            return df_reordered

        except Exception as e:
            raise TransformationError(f"Failed to reorder columns: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "reorder_columns"


class DropColumnsTransformer(BaseTransformer):
    """Drop specified columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Drop columns from DataFrame.

        Config options:
            - columns: List of column names to drop

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with columns dropped
        """
        try:
            columns = config.get("columns", [])

            if not columns:
                raise TransformationError("Column list is required")

            existing_columns = [col for col in columns if col in df.columns]
            df_dropped = df.drop(columns=existing_columns, errors="ignore")

            logger.info(f"Dropped {len(existing_columns)} columns")
            return df_dropped

        except Exception as e:
            raise TransformationError(f"Failed to drop columns: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "drop_columns"
