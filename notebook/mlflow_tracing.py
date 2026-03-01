"""MLflow tracing helpers for notebook and async agent workloads."""

from __future__ import annotations

import logging
import sys
import warnings

import mlflow

_SCHEMA_WARNING_TEXT = "Value 'True' is not supported in schema, ignoring v=True"
_CONTEXT_WARNING_TEXT = "was created in a different Context"
_FILTERS_INSTALLED = False
_STDERR_PATCHED = False


class _FilteredStderr:
    """Drop noisy lines while forwarding all other stderr output."""

    def __init__(self, wrapped, blocked_texts: tuple[str, ...]):
        self._wrapped = wrapped
        self._blocked_texts = blocked_texts
        self._buffer = ""

    def write(self, text: str) -> int:
        if not text:
            return 0

        self._buffer += text
        written = len(text)

        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            full_line = f"{line}\n"
            if any(blocked in full_line for blocked in self._blocked_texts):
                continue
            self._wrapped.write(full_line)
        return written

    def flush(self) -> None:
        if self._buffer:
            if not any(blocked in self._buffer for blocked in self._blocked_texts):
                self._wrapped.write(self._buffer)
            self._buffer = ""
        self._wrapped.flush()

    def __getattr__(self, name):
        return getattr(self._wrapped, name)


class _DropMlflowContextWarning(logging.Filter):
    """Suppress known benign context warnings from MLflow async autologging."""

    def filter(self, record: logging.LogRecord) -> bool:
        return _CONTEXT_WARNING_TEXT not in record.getMessage()


class _DropSchemaWarning(logging.Filter):
    """Suppress noisy schema compatibility messages from tool schema conversion."""

    def filter(self, record: logging.LogRecord) -> bool:
        return _SCHEMA_WARNING_TEXT not in record.getMessage()


def _install_noise_filters() -> None:
    global _FILTERS_INSTALLED, _STDERR_PATCHED
    if _FILTERS_INSTALLED:
        return

    warnings.filterwarnings("ignore", message=_SCHEMA_WARNING_TEXT)

    autolog_logger = logging.getLogger("mlflow.utils.autologging_utils")
    if not any(isinstance(f, _DropMlflowContextWarning) for f in autolog_logger.filters):
        autolog_logger.addFilter(_DropMlflowContextWarning())

    schema_filter = _DropSchemaWarning()
    for logger_name in ("google", "google.genai", "langchain_google_genai"):
        schema_logger = logging.getLogger(logger_name)
        if not any(isinstance(f, _DropSchemaWarning) for f in schema_logger.filters):
            schema_logger.addFilter(schema_filter)

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if not any(isinstance(f, _DropSchemaWarning) for f in handler.filters):
            handler.addFilter(schema_filter)

    # Some providers write schema warnings directly to stderr (not logging/warnings).
    if not _STDERR_PATCHED:
        sys.stderr = _FilteredStderr(sys.stderr, (_SCHEMA_WARNING_TEXT,))
        _STDERR_PATCHED = True

    _FILTERS_INSTALLED = True


def enable_mlflow_tracing(
    *,
    run_tracer_inline: bool = True,
    log_traces: bool = True,
    silence_known_noise: bool = True,
) -> None:
    """Enable MLflow LangChain autologging with optional warning suppression."""

    if silence_known_noise:
        _install_noise_filters()

    mlflow.langchain.autolog(run_tracer_inline=run_tracer_inline, log_traces=log_traces)


def disable_mlflow_tracing() -> None:
    """Disable MLflow LangChain autologging."""

    mlflow.langchain.autolog(disable=True)
