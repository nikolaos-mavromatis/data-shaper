"""Registry for extractor plugins."""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Type

from data_shaper.utils.exceptions import RegistryError
from data_shaper.utils.logger import get_logger
from data_shaper.extractors.base import BaseExtractor

logger = get_logger(__name__)


class ExtractorsRegistry:
    """Registry for managing extractor plugins."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._extractors: Dict[str, Type[BaseExtractor]] = {}

    def register(self, extractor_class: Type[BaseExtractor]) -> None:
        """
        Register an extractor class.

        Args:
            extractor_class: Extractor class to register

        Raises:
            RegistryError: If extractor type already registered
        """
        if not issubclass(extractor_class, BaseExtractor):
            raise RegistryError(f"{extractor_class} must inherit from BaseExtractor")

        extractor_type = extractor_class.get_type()

        if extractor_type in self._extractors:
            logger.warning(
                f"Extractor type '{extractor_type}' already registered, overwriting"
            )

        self._extractors[extractor_type] = extractor_class
        logger.debug(
            f"Registered extractor: {extractor_type} -> {extractor_class.__name__}"
        )

    def get(self, extractor_type: str) -> BaseExtractor:
        """
        Get an extractor instance by type.

        Args:
            extractor_type: Type identifier for the extractor

        Returns:
            Instance of the requested extractor

        Raises:
            RegistryError: If extractor type not found
        """
        if extractor_type not in self._extractors:
            available = ", ".join(self._extractors.keys())
            raise RegistryError(
                f"Extractor type '{extractor_type}' not found. Available: {available}"
            )

        return self._extractors[extractor_type]()

    def list_types(self) -> list[str]:
        """
        List all registered extractor types.

        Returns:
            List of registered extractor type identifiers
        """
        return list(self._extractors.keys())

    def auto_discover(self) -> None:
        """
        Auto-discover and register all extractor classes in the extractors module.

        Scans all Python files in the extractors directory and registers
        any classes that inherit from BaseExtractor.
        """
        extractors_dir = Path(__file__).parent

        for py_file in extractors_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name in [
                "base.py",
                "registry.py",
            ]:
                continue

            module_name = f"src.extractors.{py_file.stem}"

            try:
                module = importlib.import_module(module_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseExtractor)
                        and obj is not BaseExtractor
                        and obj.__module__ == module_name
                    ):
                        self.register(obj)

            except Exception as e:
                logger.warning(f"Failed to load extractor module {module_name}: {e}")


# Global registry instance
extractor_registry = ExtractorsRegistry()
