"""Implementation of the ``install`` command."""

import pathlib
from typing import Optional

from loguru import logger

from varfish_installer.cli import app
from varfish_installer.config import InstallConfig, TlsCertificateMode

#: Default configuration to use in CLI.
DEFAULT_CONFIG = InstallConfig()


@app.command()
def install(
    dst_path: pathlib.Path,
    manage_docker_compose_override: bool = DEFAULT_CONFIG.manage_docker_compose_override,
    manage_env: bool = DEFAULT_CONFIG.manage_env,
    varfish_web_dns_names: list[str] = DEFAULT_CONFIG.varfish_web_dns_names,
    traefik_tls_mode: TlsCertificateMode = DEFAULT_CONFIG.traefik_tls_mode,
    traefik_tls_cert_file: Optional[str] = DEFAULT_CONFIG.traefik_tls_cert_file,
    traefik_tls_key_file: Optional[str] = DEFAULT_CONFIG.traefik_tls_key_file,
):
    """Create VarFish installation at the given path."""
    config = InstallConfig(
        manage_docker_compose_override=manage_docker_compose_override,
        manage_env=manage_env,
        varfish_web_dns_names=varfish_web_dns_names,
        traefik_tls_mode=traefik_tls_mode,
        traefik_tls_cert_file=traefik_tls_cert_file,
        traefik_tls_key_file=traefik_tls_key_file,
    )
    logger.debug(f"Installing VarFish at {dst_path} with config {config}")
    logger.debug(
        f"git clone https://github.com/varfish-org/varfish-docker-compose-ng.git {dst_path}"
    )
