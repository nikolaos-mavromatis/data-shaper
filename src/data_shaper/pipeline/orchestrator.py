"""Pipeline orchestration engine."""

from typing import Any, Dict, Optional

import pandas as pd
from data_shaper.extractors.registry import ExtractorsRegistry
from data_shaper.exporters.registry import ExportersRegistry
from data_shaper.utils.exceptions import PipelineError
from data_shaper.utils.logger import get_logger


logger = get_logger(__name__)


class PipelineOrchestrator:
    """Orchestrate data extraction and transformation pipelines."""

    def __init__(
        self,
        extractors_registry: ExtractorsRegistry,
        exporters_registry: ExportersRegistry,
    ) -> None:
        """Initialize the pipeline orchestrator."""
        self.extractors = extractors_registry
        self.exporters = exporters_registry

    def run_pipeline(
        self,
        config: Dict[str, Any],
    ) -> pd.DataFrame:
        """
        Execute the complete pipeline for a dataset.

        Args:
            config: Dataset configurations
            export_path: Optional path to save output files

        Returns:
            Dictionary mapping dataset names to resulting DataFrames

        Raises:
            PipelineError: If pipeline execution fails
        """
        logger.info(f"Processing dataset...")

        self.df = self._extract_data(config)

        self._export_data(config)

        return self.df

    def _extract_data(self, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract data using configured extractor.

        Args:
            config: Dataset configuration

        Returns:
            Extracted DataFrame
        """
        try:
            extractor = self.extractors.get(config["extraction"]["type"])
            df = extractor.extract(config["extraction"])
            return df

        except Exception as e:
            raise PipelineError(
                f"Extraction failed for dataset '{config['name']}': {e}"
            )

    def _export_data(
        self,
        config: Dict[str, Any],
        export_path: Optional[str] = None,
    ) -> None:
        """
        Export data using configured exporter.

        Args:
            data: DataFrame to export
            config: Dataset configuration
            export_path: Optional path to save output files
        """
        try:
            exporter = self.exporters.get(config["exportation"]["type"])

            export_config = config["exportation"]
            if export_path:
                export_config["destination"] = export_path

            exporter.export(self.df, export_config)

        except Exception as e:
            raise PipelineError(
                f"Exportation failed for dataset '{config['name']}': {e}"
            )
