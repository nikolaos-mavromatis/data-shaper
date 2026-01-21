"""Custom exceptions for the data pipeline."""


class PipelineError(Exception):
    """Base exception for pipeline errors."""

    pass


class ConfigurationError(PipelineError):
    """Raised when configuration is invalid."""

    pass
