"""Implementation of the ``download`` command."""

import pathlib

from loguru import logger

from varfish_installer.cli import app
from varfish_installer.config import DownloadConfig, DownloadDataset, DownloadSubset

#: Default configuration to use.
DEFAULT_CONFIG = DownloadConfig()


@app.command()
def install(
    dst_path: pathlib.Path,
    base_dir: str = DEFAULT_CONFIG.base_dir,
    static_infix: str = DEFAULT_CONFIG.static_infix,
    subset: DownloadSubset = DEFAULT_CONFIG.subset,
    disable_ssl_verification: bool = DEFAULT_CONFIG.disable_ssl_verification,
    datasets: list[DownloadDataset] = DEFAULT_CONFIG.datasets,
):
    """Update data downloads at the given path."""
    config = DownloadConfig(
        base_dir=base_dir,
        static_infix=static_infix,
        subset=subset,
        disable_ssl_verification=disable_ssl_verification,
        datasets=datasets,
    )
    logger.debug(f"Downloading data to {dst_path} with config {config}")
