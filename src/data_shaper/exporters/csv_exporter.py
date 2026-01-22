"""CSV data exporter."""

from typing import Any, Dict
import pandas as pd

from data_shaper.utils.exceptions import ExportError
from data_shaper.utils.logger import get_logger
from data_shaper.exporters.base import BaseExporter

logger = get_logger(__name__)


class CSVExporter(BaseExporter):
    """Export data to CSV files."""

    def export(self, data: pd.DataFrame, config: Dict[str, Any]) -> None:
        """
        Export data to a CSV file.

        Supported options:
            - index: Export index (default: False)
            - delimiter: Field delimiter (default: ',')
            - encoding: File encoding (default: 'utf-8')

        Args:
            data: DataFrame to export
            config: Export configuration

        Raises:
            ExportError: If CSV file cannot be written
        """
        try:
            logger.info(f"Exporting CSV to: {config['destination']}")

            data.to_csv(
                config["destination"],
                index=config["options"].get("index", False),
                sep=config["options"].get("delimiter", ","),
                encoding=config["options"].get("encoding", "utf-8"),
            )

            logger.info(
                f"Exported {len(data)} rows, {len(data.columns)} columns to CSV"
            )

        except FileNotFoundError:
            raise ExportError(f"CSV file not found: {config['destination']}")
        except pd.errors.EmptyDataError:
            raise ExportError(f"CSV file is empty: {config['destination']}")
        except Exception as e:
            raise ExportError(f"Failed to export CSV to {config['destination']}: {e}")
