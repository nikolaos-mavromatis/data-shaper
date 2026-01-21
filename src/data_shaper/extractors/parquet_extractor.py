"""Parquet data extractor."""

from typing import Any, Dict
import pandas as pd

from data_shaper.utils.exceptions import ExtractionError
from data_shaper.utils.logger import get_logger
from data_shaper.extractors.base import BaseExtractor

logger = get_logger(__name__)


class ParquetExtractor(BaseExtractor):
    """Extract data from Parquet files."""

    def extract(self, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data from a Parquet file.

        Supported options:
            - columns: List of columns to read (default: None, reads all)
            - filters: Row filter predicates (default: None)
            - use_threads: Use multiple threads for reading (default: True)

        Args:
            config: Extraction configuration

        Returns:
            DataFrame with Parquet data

        Raises:
            ExtractionError: If Parquet file cannot be read
        """
        try:
            logger.info(f"Extracting Parquet from: {config['source']}")

            df = pd.read_parquet(
                config["source"],
                columns=config["options"].get("columns"),
                filters=config["options"].get("filters"),
                use_threads=config["options"].get("use_threads", True),
            )

            logger.info(
                f"Extracted {len(df)} rows, {len(df.columns)} columns from Parquet"
            )
            return df

        except FileNotFoundError:
            raise ExtractionError(f"Parquet file not found: {config['source']}")
        except Exception as e:
            raise ExtractionError(
                f"Failed to extract Parquet from {config['source']}: {e}"
            )
