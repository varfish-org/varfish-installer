import syrupy

from varfish_installer.config import DownloadConfig, ManifestParser

#: Default configuration to use.
DEFAULT_CONFIG = DownloadConfig()


def test_manifest_parser(snapshot: syrupy.assertion.SnapshotAssertion):
    parser = ManifestParser(path="tests/config/manifest-gnomad-exomes.txt")
    result = parser.parse()
    assert result == snapshot
