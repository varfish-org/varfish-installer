import syrupy

from varfish_installer.config import DownloadConfig, ManifestParser, DownloadInfoGenerator

#: Default configuration to use.
DEFAULT_CONFIG = DownloadConfig()


def test_manifest_parser(snapshot: syrupy.assertion.SnapshotAssertion):
    parser = ManifestParser(path="tests/config/manifest-gnomad-exomes.txt")
    result = parser.parse()
    assert result == snapshot


def test_download_info_generator(snapshot: syrupy.assertion.SnapshotAssertion):
    parser = ManifestParser(path="tests/config/manifest-gnomad-exomes.txt")
    manifest = parser.parse()
    config = DownloadConfig(datasets=[manifest])
    result = manifest
    assert result == snapshot
