from enum import Enum
import typing
from typing import Optional

from loguru import logger
from pydantic import BaseModel, ConfigDict


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


class DatasetCategory(str, Enum):
    """Category for a datasets."""

    #: Data for annonars.
    ANNONARS = "annonars"
    #: Data for Mehari.
    MEHARI = "mehari"
    #: Tracks for genome browser.
    TRACKS = "tracks"
    #: Data for viguno.
    VIGUNO = "viguno"
    #: Data for the VarFish server worker.
    WORKER = "worker"


class ManifestEntry(BaseModel):
    """Entry in the manifest file."""

    model_config = ConfigDict(frozen=True)

    #: Size of the file.
    size: int
    #: MD5 checksum of file.
    md5: str
    #: SHA256 checksum of file.
    sha256: str
    #: Name of the file.
    name: str


class Manifest(BaseModel):
    """Information from the manifest of a dataset."""

    model_config = ConfigDict(frozen=True)

    #: Raw manifest text content.
    raw_content: str
    #: Path that hashdeep was invoked from
    hashdeep_invocation_path: Optional[str]
    #: SHA256 checksum of raw content (minus last line).
    sha256_checksum: Optional[str]
    #: The manifest entries.
    entries: list[ManifestEntry]


class ManifestParser:
    """Helper class to parse hashdeep manifest files."""

    def __init__(self, *, path: Optional[str] = None, inputf: Optional[typing.TextIO] = None):
        #: Path to input file (mutually exclusive with inputf).
        self.path = path
        #: Input file (mutually exclusive with path).
        self.inputf = inputf

        if self.path and self.inputf:
            raise ValueError("Only one of path or inputf must be given.")
        elif not self.path and not self.inputf:
            raise ValueError("One of path or inputf must be given.")

    def parse(self) -> Manifest:
        """Parse a manifest file."""
        if self.path:
            with open(self.path, "rt") as inputf:
                return self._parse(inputf)
        else:
            assert self.inputf is not None, "checked in __init__"
            return self._parse(self.inputf)

    def _parse(self, inputf: typing.TextIO) -> Manifest:
        """Implementation of parsing manifest file."""
        raw_content = inputf.read()
        hashdeep_invocation_path = ""
        sha256_checksum = ""
        entries = []

        for lineno, line in enumerate(raw_content.splitlines()):
            if lineno == 0:
                if ":" not in line:
                    raise ValueError(f"First line must contain ':' but got: {line}")
                hashdeep_invocation_path = line.split(":")[1].strip()
            elif line.startswith("## EOF"):
                if "## EOF SHA256=" not in line:
                    raise ValueError(f"Expected '## EOF SHA256=' in line {lineno} but got: {line}")
                sha256_checksum = line.split("=")[-1]
            elif not line.startswith("##") and not line.startswith("%%%%"):
                parts = line.split(",")
                if len(parts) != 4:
                    raise ValueError(
                        f"Expected 4 parts in line {lineno} but got {len(parts)}: {line}"
                    )
                size, md5, sha256, name = parts
                entries.append(ManifestEntry(size=int(size), md5=md5, sha256=sha256, name=name))

        if not hashdeep_invocation_path:
            logger.warning("No SHA256 checksum found in manifest")
        if not sha256_checksum:
            logger.warning("No SHA256 checksum found in manifest")

        return Manifest(
            raw_content=raw_content,
            hashdeep_invocation_path=hashdeep_invocation_path,
            sha256_checksum=sha256_checksum,
            entries=entries,
        )


class DatasetInfo(BaseModel):
    """Store information about one dataset."""

    #: Dataset name.
    name: str
    #: Dataset category.
    category: DatasetCategory
    #: Optional dataset release.
    release: Optional[GenomeRelease]
    #: Raw version string.
    version_raw: str
    #: Parsed version where the key points at the dataset-specific
    #: input dataset name and the value is this dataset's version.
    version_parsed: dict[str, str]
    #: The manifest of the dataset.
    manifest: Optional[Manifest]


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
