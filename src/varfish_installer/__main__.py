import sys

from loguru import logger

from varfish_installer import cmd_download  # noqa: F401
from varfish_installer import cmd_install  # noqa: F401
from varfish_installer.cli import app

if __name__ == "__main__":
    logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
    app()
