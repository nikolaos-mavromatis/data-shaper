"""Custom exceptions for the data pipeline."""


class PipelineError(Exception):
    """Base exception for pipeline errors."""

    pass


class ConfigurationError(PipelineError):
    """Raised when configuration is invalid."""

    pass


class ExtractionError(PipelineError):
    """Raised when data extraction fails."""

    pass


class RegistryError(PipelineError):
    """Raised when plugin registration fails."""

    pass


class TransformationError(PipelineError):
    """Raised when data transformation fails."""

    pass


class ExportError(PipelineError):
    """Raised when data export fails."""

    pass
