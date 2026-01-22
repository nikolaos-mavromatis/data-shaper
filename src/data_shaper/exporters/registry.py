"""Registry for exporter plugins."""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Type

from data_shaper.utils.exceptions import RegistryError
from data_shaper.utils.logger import get_logger
from data_shaper.exporters.base import BaseExporter

logger = get_logger(__name__)


class ExportersRegistry:
    """Registry for managing exporter plugins."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._exporters: Dict[str, Type[BaseExporter]] = {}

    def register(self, exporter_class: Type[BaseExporter]) -> None:
        """
        Register an exporter class.
        Args:
            exporter_class: Exporter class to register

        Raises:
            RegistryError: If exporter type already registered
        """
        if not issubclass(exporter_class, BaseExporter):
            raise RegistryError(f"{exporter_class} must inherit from BaseExporter")

        exporter_type = exporter_class.get_type()

        if exporter_type in self._exporters:
            logger.warning(
                f"Exporter type '{exporter_type}' already registered, overwriting"
            )

        self._exporters[exporter_type] = exporter_class
        logger.debug(
            f"Registered exporter: {exporter_type} -> {exporter_class.__name__}"
        )

    def get(self, exporter_type: str) -> BaseExporter:
        """
        Get an exporter instance by type.

        Args:
            exporter_type: Type identifier for the exporter

        Returns:
            Instance of the requested exporter

        Raises:
            RegistryError: If exporter type not found
        """
        if exporter_type not in self._exporters:
            available = ", ".join(self._exporters.keys())
            raise RegistryError(
                f"Exporter type '{exporter_type}' not found. Available: {available}"
            )

        return self._exporters[exporter_type]()

    def list_types(self) -> list[str]:
        """
        List all registered exporter types.
        Returns:
            List of registered exporter type identifiers
        """
        return list(self._exporters.keys())

    def auto_discover(self) -> None:
        """
        Auto-discover and register all exporter classes in the exporters module.
        Scans all Python files in the exporters directory and registers
        any classes that inherit from BaseExporter.
        """
        exporters_dir = Path(__file__).parent

        for py_file in exporters_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name in [
                "base.py",
                "registry.py",
            ]:
                continue

            module_name = f"data_shaper.exporters.{py_file.stem}"

            try:
                module = importlib.import_module(module_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseExporter)
                        and obj is not BaseExporter
                        and obj.__module__ == module_name
                    ):
                        self.register(obj)

            except Exception as e:
                logger.warning(f"Failed to load exporter module {module_name}: {e}")


# Global registry instance
exporters_registry = ExportersRegistry()
exporters_registry.auto_discover()
