"""Registry for transformer plugins."""

import importlib
import inspect
from pathlib import Path
from typing import Dict, Type

from data_shaper.utils.exceptions import RegistryError
from data_shaper.utils.logger import get_logger
from data_shaper.transformers.base import BaseTransformer

logger = get_logger(__name__)


class TransformersRegistry:
    """Registry for managing transformer plugins."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._transformers: Dict[str, Type[BaseTransformer]] = {}

    def register(self, transformer_class: Type[BaseTransformer]) -> None:
        """
        Register a transformer class.

        Args:
            transformer_class: Transformer class to register

        Raises:
            RegistryError: If transformer type already registered
        """
        if not issubclass(transformer_class, BaseTransformer):
            raise RegistryError(
                f"{transformer_class} must inherit from BaseTransformer"
            )

        transformer_type = transformer_class.get_type()

        if transformer_type in self._transformers:
            logger.warning(
                f"Transformer type '{transformer_type}' already registered, overwriting"
            )

        self._transformers[transformer_type] = transformer_class
        logger.debug(
            f"Registered transformer: {transformer_type} -> {transformer_class.__name__}"
        )

    def get(self, transformer_type: str) -> BaseTransformer:
        """
        Get a transformer instance by type.

        Args:
            transformer_type: Type identifier for the transformer

        Returns:
            Instance of the requested transformer

        Raises:
            RegistryError: If transformer type not found
        """
        if transformer_type not in self._transformers:
            available = ", ".join(self._transformers.keys())
            raise RegistryError(
                f"Transformer type '{transformer_type}' not found. Available: {available}"
            )

        return self._transformers[transformer_type]()

    def list_types(self) -> list[str]:
        """
        List all registered transformer types.

        Returns:
            List of registered transformer type identifiers
        """
        return list(self._transformers.keys())

    def auto_discover(self) -> None:
        """
        Auto-discover and register all transformer classes in the transformers module.

        Scans all Python files in the transformers directory and registers
        any classes that inherit from BaseTransformer.
        """
        transformers_dir = Path(__file__).parent

        for py_file in transformers_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name in [
                "base.py",
                "registry.py",
            ]:
                continue

            module_name = f"data_shaper.transformers.{py_file.stem}"

            try:
                module = importlib.import_module(module_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseTransformer)
                        and obj is not BaseTransformer
                        and obj.__module__ == module_name
                    ):
                        self.register(obj)

            except Exception as e:
                logger.warning(f"Failed to load transformer module {module_name}: {e}")


# Global registry instance
transformers_registry = TransformersRegistry()
transformers_registry.auto_discover()
