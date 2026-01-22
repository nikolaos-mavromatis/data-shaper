"""Logging configuration for the data pipeline with rich formatting."""

import logging
import sys
from typing import Optional

try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.theme import Theme

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Custom theme for rich output
CUSTOM_THEME = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "debug": "dim cyan",
    }
)


def setup_logger(
    name: str, level: Optional[str] = None, use_rich: bool = True
) -> logging.Logger:
    """
    Set up a logger with rich console output.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_rich: Use rich formatting if available (default: True)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        if use_rich and RICH_AVAILABLE:
            # Use Rich handler for beautiful output
            console = Console(theme=CUSTOM_THEME)
            handler = RichHandler(
                console=console,
                show_time=True,
                show_path=True,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True,
            )
            formatter = logging.Formatter(
                "%(message)s",
                datefmt="[%Y-%m-%d %H:%M:%S]",
            )
        else:
            # Fallback to standard handler
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(log_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


def log_success(logger: logging.Logger, message: str) -> None:
    """Log a success message with rich formatting."""
    if RICH_AVAILABLE:
        logger.info(f"\n[success]✓[/success] {message}")
    else:
        logger.info(f"\n✓ {message}")


def log_error(logger: logging.Logger, message: str) -> None:
    """Log an error message with rich formatting."""
    if RICH_AVAILABLE:
        logger.error(f"\n[error]✗[/error] {message}")
    else:
        logger.error(f"\n✗ {message}")


def log_section(logger: logging.Logger, title: str) -> None:
    """Log a section header with rich formatting."""
    if RICH_AVAILABLE:
        logger.info(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
        logger.info(f"[bold cyan]{title}[/bold cyan]")
        logger.info(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
    else:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"{title}")
        logger.info(f"{'=' * 60}\n")
