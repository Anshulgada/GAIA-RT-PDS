"""
Launcher for the pothole detector package.

This file is a small, backwards-compatible entrypoint that delegates to the
real implementation in the `src.pothole_detector` package.

Improvements:
- Provide a testable `main()` function.
- Configure minimal logging so errors are visible when invoked from the CLI.
- Return non-zero exit code on unexpected exceptions.
"""

from __future__ import annotations

import logging
import sys
from typing import NoReturn

from src.pothole_detector.cli import cli


logger = logging.getLogger(__name__)


def main() -> NoReturn:
    """Run the package CLI with minimal logging and controlled exit codes.

    This small wrapper improves debuggability when the package is invoked as a
    script and makes it easier to call from tests by importing `main` or the
    underlying `cli` function.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        cli()
    except SystemExit:
        # Let SystemExit pass through so CLI frameworks can control exit codes
        raise
    except Exception as exc:  # pragma: no cover - surface unexpected errors
        logger.exception("Unhandled exception while running CLI: %s", exc)
        # Exit with a non-zero status to indicate failure
        sys.exit(1)


if __name__ == "__main__":
    main()
