"""Main entry point for the data pipeline CLI."""

import argparse
import sys
from data_shaper.pipeline.orchestrator import PipelineOrchestrator
from data_shaper.config.loader import ConfigLoader
from data_shaper.utils.logger import setup_logger
from data_shaper.extractors.registry import extractors_registry
from data_shaper.exporters.registry import exporters_registry

logger = setup_logger("data-pipeline")


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="Data preparation pipeline with extraction and transformation"
    )

    parser.add_argument(
        "--config-path",
        required=True,
        help="Path to YAML file containing dataset configurations",
    )

    parser.add_argument(
        "--export-path",
        required=False,
        help="Path to YAML file containing dataset configurations",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Update log level
    if args.log_level:
        logger.setLevel(args.log_level)

    config_loader = ConfigLoader(args.config_path)
    orchestrator = PipelineOrchestrator(
        extractors_registry=extractors_registry, exporters_registry=exporters_registry
    )

    try:
        logger.info(f"Loading configuration from {args.config_path}")
        config = config_loader.load_config()

        logger.info(f"Running pipeline for dataset: {config['name']}")
        result = orchestrator.run_pipeline(config)
        print(result.head())
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
