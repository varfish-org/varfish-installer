import syrupy
from moto import mock_aws

from varfish_installer.config import DownloadConfig, ManifestParser, DownloadInfoGenerator

#: Default configuration to use.
DEFAULT_CONFIG = DownloadConfig()


def test_manifest_parser(snapshot: syrupy.assertion.SnapshotAssertion):
    parser = ManifestParser(path="tests/config/manifest-gnomad-exomes.txt")
    result = parser.parse()
    assert result == snapshot


@mock_aws
def test_download_info_generator(
    create_bucket,
    snapshot: syrupy.assertion.SnapshotAssertion
):
    parser = ManifestParser(path="tests/config/manifest-gnomad-exomes.txt")
    manifest = parser.parse()
    config = DownloadConfig(datasets=[manifest])
    result = manifest
    assert result == snapshot
