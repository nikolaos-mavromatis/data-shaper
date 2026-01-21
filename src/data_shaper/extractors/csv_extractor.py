"""CSV data extractor."""

from typing import Any, Dict
import pandas as pd

from data_shaper.utils.exceptions import ExtractionError
from data_shaper.utils.logger import get_logger
from data_shaper.extractors.base import BaseExtractor

logger = get_logger(__name__)


class CSVExtractor(BaseExtractor):
    """Extract data from CSV files."""

    def extract(self, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data from a CSV file.

        Supported options:
            - delimiter: Field delimiter (default: ',')
            - encoding: File encoding (default: 'utf-8')
            - header: Row number to use as column names (default: 0)
            - skiprows: Rows to skip at the start (default: None)
            - usecols: Columns to read (default: None)
            - dtype: Data type for columns (default: None)

        Args:
            config: Extraction configuration

        Returns:
            DataFrame with CSV data

        Raises:
            ExtractionError: If CSV file cannot be read
        """
        try:
            logger.info(f"Extracting CSV from: {config['source']}")

            df = pd.read_csv(
                config["source"],
                delimiter=config["options"].get("delimiter", ","),
                encoding=config["options"].get("encoding", "utf-8"),
                header=config["options"].get("header", 0),
                skiprows=config["options"].get("skiprows"),
                usecols=config["options"].get("usecols"),
                dtype=config["options"].get("dtype"),
            )

            logger.info(f"Extracted {len(df)} rows, {len(df.columns)} columns from CSV")
            return df

        except FileNotFoundError:
            raise ExtractionError(f"CSV file not found: {config['source']}")
        except pd.errors.EmptyDataError:
            raise ExtractionError(f"CSV file is empty: {config['source']}")
        except Exception as e:
            raise ExtractionError(f"Failed to extract CSV from {config['source']}: {e}")
