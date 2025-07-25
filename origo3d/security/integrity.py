import hashlib
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


def compute_sha256(path: Path) -> str:
    """Return SHA256 checksum of the given file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_client_integrity(expected_files: Dict[Path, str]) -> bool:
    """Verify that specified files match provided SHA256 hashes."""
    for file_path, expected_hash in expected_files.items():
        p = Path(file_path)
        if not p.is_file():
            logger.warning("missing file: %s", p)
            return False
        actual_hash = compute_sha256(p)
        if actual_hash != expected_hash:
            logger.warning("hash mismatch for %s", p)
            return False
    return True
