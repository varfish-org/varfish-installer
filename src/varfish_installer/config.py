from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TlsCertificateMode(str, Enum):
    """Select the TLS certificate mode."""

    #: Use self-signed certificates (default).
    SELF_SIGNED = "self-signed"
    #: Use Let's Encrypt to obtain a certificate.
    LETSENCRYPT = "letsencrypt"
    #: Provide certificate and key file.
    PROVIDED = "provided"


class DownloadSubset(str, Enum):
    """Select the subset to download."""

    #: Full data.
    FULL = "full"
    #: Reduced to exonic regions.
    REDUCED_EXOMES = "reduced-exomes"
    #: Reduced for development.
    DEVELOPMENT = "reduced-dev"


class BaseConfig(BaseModel):
    """Base configuration."""

    #: Increase verbosity.
    verbose: bool = False
    #: Decrease verbosity.
    quiet: bool = False
    #: Execute in dry run mode.
    dry_run: bool = False


class InstallConfig(BaseConfig):
    """Configuration for the install/update command."""

    #: Whether to manage the ``docker-compose.override.yml`` file.
    manage_docker_compose_override: bool = True
    #: Whether to manage the ``.env`` file.
    manage_env: bool = True

    #: DNS name(s) of the varfish-web server.
    varfish_web_dns_names: list[str] = ["{catchall:.+}"]

    #: The TLS certificate mode.
    traefik_tls_mode: TlsCertificateMode = TlsCertificateMode.SELF_SIGNED
    #: The path to the provided TLS certificate (chain) file.
    traefik_tls_cert_file: Optional[str] = None
    #: The path to the provided TLS key file.
    traefik_tls_key_file: Optional[str] = None


class GenomeRelease(str, Enum):
    """Select the genome release."""

    #: GRCh37.
    GRCH37 = "GRCh37"
    #: GRCh38.
    GRCH38 = "GRCh38"


class DownloadDataset(str, Enum):
    """Select the dataset to download."""

    #: Annonars CADD RocksDB; release-specific.
    ANNONARS_CADD = "annonars-cadd"
    #: Annonars Conservation RocksDB; release-specific.
    ANNONARS_CONS = "annonars-cons"
    #: Annonars dbNSFP RocksDB; release-specific.
    ANNONARS_DBNSFP = "annonars-dbnsfp"
    #: Annonars dbSCNV RocksDB; release-specific.
    ANNONARS_DBSCNV = "annonars-dbscnv"
    #: Annonars functional regions RocksDB; release-specific.
    ANNONARS_FUNCTIONAL = "annonars-functional"
    #: Annonars gnomAD exomes RocksDB; release-specific.
    ANNONARS_GNOMAD_EXOMES = "annonars-gnomad-exomes"
    #: Annonars gnomAD genomes RocksDB; release-specific.
    ANNONARS_GNOMAD_GENOMES = "annonars-gnomad-genomes"
    #: Annonars mtDNA RocksDB; release-specific.
    ANNONARS_MTDNA = "annonars-mtdna"
    #: Annonars exomes SVs RocksDB; release-specific.
    ANNONARS_SV_EXOMES = "annonars-sv-exomes"
    #: Annonars genomes SVs RocksDB; release-specific.
    ANNONARS_SV_GENOMES = "annonars-sv-genomes"
    #: Annonars HelixMTDB RocksDB; release-specific.
    ANNONARS_HELIXMTDB = "annonars-helixmtdb"
    #: Annonars regions files; release-specific.
    ANNONARS_REGIONS = "annonars-regions"
    #: Annonars genes RocksDB; not release-specific.
    ANNONARS_GENES = "annonars-genes"
    #: Annonars ClinVar RocksDB; release-specific; from GitHub.
    ANNONARS_CLINVAR = "annonars-clinvar"

    #: Mehari frequencies RocksDB; release-specific.
    MEHARI_FREQS = "mehari-freqs"
    #: Mehari genes cross-link file; not release-specific.
    MEHARI_GENES_XLINK = "mehari-genes-xlink"
    #: Mehari transcripts; release-specific; from GitHub.
    MEHARI_TRANSCRIPTS = "mehari-transcripts"

    #: Genome browser tracks.
    GENOME_BROWSER_TRACKS = "genome-browser-tracks"

    #: VarFish Server Worker Data
    VARFISH_SERVER_WORKER_DATA = "varfish-server-worker-data"

    #: Viguno HPO data.
    VIGUNO_HPO = "viguno-hpo"

    #: CADA-Prio Data; from GitHub.
    CADA_PRIO = "cada-prio"


class DownloadConfig(BaseConfig):
    """Configuration for the download command."""

    #: S3 endpoint URL.
    s3_endpoint_url: str = "https://ceph-s3-public.cubi.bihealth.org"

    #: Base directory for config, volumes, and secrets.
    base_dir: str = ".prod"
    #: Infix for static data download.
    static_infix: str = "varfish-static"
    #: Subset to download.
    subset: DownloadSubset = DownloadSubset.FULL

    #: Disable verification of SSL certificates.
    disable_ssl_verification: bool = False

    #: The datasets to download, empty list for all.
    datasets: list[DownloadDataset] = []
