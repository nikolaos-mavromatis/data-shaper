"""Main entry point for the data pipeline CLI."""

import argparse
import sys
from data_shaper.pipeline.orchestrator import PipelineOrchestrator
from data_shaper.config.loader import ConfigLoader
from data_shaper.utils.logger import setup_logger
from data_shaper.extractors.registry import extractors_registry
from data_shaper.transformers.registry import transformers_registry
from data_shaper.exporters.registry import exporters_registry

logger = setup_logger("data-pipeline")


def run_pipeline(args: argparse.Namespace) -> int:
    config_loader = ConfigLoader(args.config_path)
    orchestrator = PipelineOrchestrator(
        extractors_registry=extractors_registry,
        transformers_registry=transformers_registry,
        exporters_registry=exporters_registry,
    )
    config = config_loader.load_config()
    orchestrator.run_pipeline(config)
    return 0


def list_plugins(args: argparse.Namespace) -> int:
    """
    List available extractors and transformers.

    Args:
        args: Command line arguments

    Returns:
        Exit code (always 0)
    """
    try:
        from rich.console import Console
        from rich.table import Table

        RICH_AVAILABLE = True
    except ImportError:
        RICH_AVAILABLE = False

    extractors = extractors_registry.list_types()
    transformers = transformers_registry.list_types()
    exporters = exporters_registry.list_types()

    if RICH_AVAILABLE:
        console = Console()

        # Extractors table
        console.print()
        table = Table(
            title="Available Extractors", show_header=True, header_style="bold cyan"
        )
        table.add_column("Type", style="green")

        for extractor_type in sorted(extractors):
            table.add_row(extractor_type)

        table.caption = f"Total: {len(extractors)} extractors"
        console.print(table)

        # Transformers table
        console.print()
        table = Table(
            title="Available Transformers", show_header=True, header_style="bold cyan"
        )
        table.add_column("Type", style="green")
        table.add_column("Category", style="yellow")

        # Categorize transformers
        # TODO: Automate category assignment
        categories = {
            "remove_nulls": "Cleaning",
            "deduplicate": "Cleaning",
            "fix_types": "Cleaning",
            "fill_nulls": "Cleaning",
            "rename_columns": "Schema",
            "select_columns": "Schema",
            "drop_columns": "Schema",
            "reorder_columns": "Schema",
            "filter_rows": "Filtering",
            "aggregate": "Filtering",
            "sort": "Filtering",
            "sample": "Filtering",
            "add_calculated_column": "Enrichment",
            "join_datasets": "Enrichment",
            "pivot": "Enrichment",
            "unpivot": "Enrichment",
        }

        for transformer_type in sorted(transformers):
            category = categories.get(transformer_type, "Other")
            table.add_row(transformer_type, category)

        table.caption = f"Total: {len(transformers)} transformers"
        console.print(table)
        console.print()

        # Exporters table
        console.print()
        table = Table(
            title="Available Exporters", show_header=True, header_style="bold cyan"
        )
        table.add_column("Type", style="green")

        for exporter_type in sorted(exporters):
            table.add_row(exporter_type)

        table.caption = f"Total: {len(exporters)} exporters"
        console.print(table)
    else:
        # Fallback to simple output
        print("\n=== Available Extractors ===")
        for extractor_type in sorted(extractors):
            print(f"  - {extractor_type}")

        print("\n=== Available Transformers ===")
        for transformer_type in sorted(transformers):
            print(f"  - {transformer_type}")

        print()

    return 0


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
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run data pipeline")

    run_parser.add_argument(
        "--config-path",
        required=True,
        help="Path to YAML file containing dataset configurations",
    )

    # List plugins command
    list_parser = subparsers.add_parser("list-plugins", help="List available plugins")

    args = parser.parse_args()

    # Update log level
    if args.log_level:
        logger.setLevel(args.log_level)

    if args.command == "run":
        return run_pipeline(args)
    elif args.command == "list-plugins":
        return list_plugins(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
