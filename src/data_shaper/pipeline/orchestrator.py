"""Pipeline orchestration engine."""

from typing import Any, Dict, Optional

import pandas as pd
from data_shaper.extractors.registry import ExtractorsRegistry
from data_shaper.utils.exceptions import PipelineError
from data_shaper.utils.logger import get_logger


logger = get_logger(__name__)


class PipelineOrchestrator:
    """Orchestrate data extraction and transformation pipelines."""

    def __init__(self, extractors_registry: ExtractorsRegistry) -> None:
        """Initialize the pipeline orchestrator."""
        self.extractors = extractors_registry

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

        df = self._extract_data(config)

        return df

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
