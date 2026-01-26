"""Filtering and aggregation transformers."""

from typing import Any, Dict

import pandas as pd

from data_shaper.utils.exceptions import TransformationError
from data_shaper.utils.logger import get_logger
from data_shaper.transformers.base import BaseTransformer

logger = get_logger(__name__)


class FilterRowsTransformer(BaseTransformer):
    """Filter rows based on conditions."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter rows using pandas query syntax.

        Config options:
            - condition: Query string (e.g., "age > 18 and city == 'NYC'")

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Filtered DataFrame
        """
        try:
            condition = config.get("condition")

            if not condition:
                raise TransformationError("Filter condition is required")

            initial_count = len(df)
            df_filtered = df.query(condition)
            filtered_count = initial_count - len(df_filtered)

            logger.info(
                f"Filtered out {filtered_count} rows using condition: {condition}"
            )
            return df_filtered

        except Exception as e:
            raise TransformationError(f"Failed to filter rows: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "filter_rows"


class AggregateTransformer(BaseTransformer):
    """Group by and aggregate data."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Group by columns and apply aggregations.

        Config options:
            - group_by: List of columns to group by
            - aggregations: Dictionary mapping column names to aggregation functions
                           (e.g., {'amount': 'sum', 'count': 'count', 'price': ['min', 'max']})

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Aggregated DataFrame
        """
        try:
            group_by = config.get("group_by", [])
            aggregations = config.get("aggregations", {})

            if not group_by:
                raise TransformationError("group_by columns are required")

            if not aggregations:
                raise TransformationError("Aggregation functions are required")

            df_aggregated = df.groupby(group_by).agg(aggregations).reset_index()

            # Flatten column names if multi-level
            if isinstance(df_aggregated.columns, pd.MultiIndex):
                df_aggregated.columns = [
                    "_".join(col).strip("_") if col[1] else col[0]
                    for col in df_aggregated.columns.values
                ]

            logger.info(f"Aggregated data by {group_by}")
            return df_aggregated

        except Exception as e:
            raise TransformationError(f"Failed to aggregate: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "aggregate"


class SortTransformer(BaseTransformer):
    """Sort DataFrame by columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Sort DataFrame.

        Config options:
            - columns: List of columns to sort by
            - ascending: Boolean or list of booleans for sort order (default: True)

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Sorted DataFrame
        """
        try:
            columns = config.get("columns", [])
            ascending = config.get("ascending", True)

            if not columns:
                raise TransformationError("Sort columns are required")

            df_sorted = df.sort_values(by=columns, ascending=ascending).reset_index(
                drop=True
            )

            logger.info(f"Sorted data by {columns}")
            return df_sorted

        except Exception as e:
            raise TransformationError(f"Failed to sort: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "sort"


class SampleTransformer(BaseTransformer):
    """Sample rows from DataFrame."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Sample rows from DataFrame.

        Config options:
            - n: Number of rows to sample (mutually exclusive with frac)
            - frac: Fraction of rows to sample (mutually exclusive with n)
            - random_state: Random seed for reproducibility (default: None)

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Sampled DataFrame
        """
        try:
            n = config.get("n")
            frac = config.get("frac")
            random_state = config.get("random_state")

            if n is None and frac is None:
                raise TransformationError("Either 'n' or 'frac' must be specified")

            df_sampled = df.sample(n=n, frac=frac, random_state=random_state)

            logger.info(f"Sampled {len(df_sampled)} rows")
            return df_sampled

        except Exception as e:
            raise TransformationError(f"Failed to sample: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "sample"
