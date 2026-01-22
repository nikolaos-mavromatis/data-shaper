"""Pipeline orchestration engine."""

from typing import Any, Dict, Optional

import pandas as pd
from data_shaper.extractors.registry import ExtractorsRegistry
from data_shaper.transformers.registry import TransformersRegistry
from data_shaper.exporters.registry import ExportersRegistry
from data_shaper.utils.exceptions import PipelineError
from data_shaper.utils.logger import get_logger, log_section, log_success


logger = get_logger(__name__)


class PipelineOrchestrator:
    """Orchestrate data extraction and transformation pipelines."""

    def __init__(
        self,
        extractors_registry: ExtractorsRegistry,
        transformers_registry: TransformersRegistry,
        exporters_registry: ExportersRegistry,
    ) -> None:
        """Initialize the pipeline orchestrator."""
        self.extractors = extractors_registry
        self.transformers = transformers_registry
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
        logger.info(f"Launched pipeline for dataset '{config['name']}'...")

        log_section(logger, "Data Extraction")
        self.df = self._extract_data(config)
        if config.get("transformations"):
            log_section(logger, "Data Transformation")
            self.df = self._apply_transformations(config)
        log_section(logger, "Data Exportation")
        self._export_data(config)

        log_success(logger, "Pipeline completed successfully.")

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

    def _apply_transformations(self, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply transformation steps to DataFrame.

        Args:
            config: Dataset configuration with transformations

        Returns:
            Transformed DataFrame
        """
        for i, step in enumerate(config["transformations"]):
            try:
                logger.debug(
                    f"Applying transformation {i + 1}/{len(config['transformations'])}: "
                    f"{step['type']}"
                )

                transformer = self.transformers.get(step["type"])
                df = transformer.transform(self.df, step["params"])
            except Exception as e:
                raise PipelineError(
                    f"Transformation '{step['type']}' failed for dataset '{config['name']}': {e}"
                )
        return df

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
