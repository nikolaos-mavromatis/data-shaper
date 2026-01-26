"""Data enrichment transformers."""

from typing import Any, Dict

import pandas as pd

from data_shaper.utils.exceptions import TransformationError
from data_shaper.utils.logger import get_logger
from data_shaper.transformers.base import BaseTransformer

logger = get_logger(__name__)


class AddCalculatedColumnTransformer(BaseTransformer):
    """Add calculated columns."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Add a calculated column.

        Config options:
            - name: Name of the new column
            - expression: Python expression to evaluate (can reference column names)
            - dtype: Optional data type for the new column

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            DataFrame with new calculated column
        """
        try:
            name = config.get("name")
            expression = config.get("expression")
            dtype = config.get("dtype")

            if not name:
                raise TransformationError("Column name is required")

            if not expression:
                raise TransformationError("Expression is required")

            # Evaluate expression using DataFrame.eval()
            df[name] = df.eval(expression)

            if dtype:
                df[name] = df[name].astype(dtype)

            logger.info(f"Added calculated column: {name}")
            return df

        except Exception as e:
            raise TransformationError(f"Failed to add calculated column: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "add_calculated_column"


class JoinDatasetsTransformer(BaseTransformer):
    """Join with another dataset."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Join with another DataFrame.

        Config options:
            - right_df: The DataFrame to join with (must be provided at runtime)
            - on: Column(s) to join on
            - how: Join type ('left', 'right', 'inner', 'outer') (default: 'left')
            - left_on: Column(s) in left DataFrame (alternative to 'on')
            - right_on: Column(s) in right DataFrame (alternative to 'on')
            - suffixes: Tuple of suffixes for overlapping columns (default: ('_left', '_right'))

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Joined DataFrame
        """
        try:
            right_df = config.get("right_df")
            on = config.get("on")
            how = config.get("how", "left")
            left_on = config.get("left_on")
            right_on = config.get("right_on")
            suffixes = config.get("suffixes", ("_left", "_right"))

            if right_df is None:
                raise TransformationError("right_df must be provided")

            if not isinstance(right_df, pd.DataFrame):
                raise TransformationError("right_df must be a DataFrame")

            if on:
                df_joined = df.merge(right_df, on=on, how=how, suffixes=suffixes)
            elif left_on and right_on:
                df_joined = df.merge(
                    right_df,
                    left_on=left_on,
                    right_on=right_on,
                    how=how,
                    suffixes=suffixes,
                )
            else:
                raise TransformationError(
                    "Either 'on' or both 'left_on' and 'right_on' required"
                )

            logger.info(f"Joined datasets with {how} join")
            return df_joined

        except Exception as e:
            raise TransformationError(f"Failed to join datasets: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "join_datasets"


class PivotTransformer(BaseTransformer):
    """Pivot DataFrame."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Pivot DataFrame.

        Config options:
            - index: Column(s) to use as index
            - columns: Column to pivot on
            - values: Column(s) with values to aggregate
            - aggfunc: Aggregation function (default: 'mean')

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Pivoted DataFrame
        """
        try:
            index = config.get("index")
            columns = config.get("columns")
            values = config.get("values")
            aggfunc = config.get("aggfunc", "mean")

            if not index or not columns or not values:
                raise TransformationError("index, columns, and values are required")

            df_pivoted = df.pivot_table(
                index=index, columns=columns, values=values, aggfunc=aggfunc
            ).reset_index()

            # Flatten column names
            df_pivoted.columns.name = None

            logger.info(f"Pivoted DataFrame")
            return df_pivoted

        except Exception as e:
            raise TransformationError(f"Failed to pivot: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "pivot"


class UnpivotTransformer(BaseTransformer):
    """Unpivot (melt) DataFrame."""

    def transform(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Unpivot DataFrame (melt from wide to long format).

        Config options:
            - id_vars: Columns to use as identifier variables
            - value_vars: Columns to unpivot (default: all non-id columns)
            - var_name: Name for the variable column (default: 'variable')
            - value_name: Name for the value column (default: 'value')

        Args:
            df: Input DataFrame
            config: Transformation configuration

        Returns:
            Unpivoted DataFrame
        """
        try:
            id_vars = config.get("id_vars", [])
            value_vars = config.get("value_vars")
            var_name = config.get("var_name", "variable")
            value_name = config.get("value_name", "value")

            df_unpivoted = df.melt(
                id_vars=id_vars,
                value_vars=value_vars,
                var_name=var_name,
                value_name=value_name,
            )

            logger.info(f"Unpivoted DataFrame")
            return df_unpivoted

        except Exception as e:
            raise TransformationError(f"Failed to unpivot: {e}")

    @classmethod
    def get_type(cls) -> str:
        return "unpivot"
