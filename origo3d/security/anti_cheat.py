"""Basic anti-cheat utilities."""

import logging
from pathlib import Path
from typing import Dict

from .integrity import verify_client_integrity
from ..networking.traffic_analyzer import TrafficAnalyzer

logger = logging.getLogger(__name__)
DEFAULT_PACKET_THRESHOLD = 5


def detect_cheat(expected_files: Dict[Path, str], analyzer: TrafficAnalyzer) -> bool:
    """Return True if cheating is suspected."""
    integrity_ok = verify_client_integrity(expected_files)
    if not integrity_ok:
        logger.info("Client integrity check failed")
        return True
    if analyzer.get_suspicious_count() > DEFAULT_PACKET_THRESHOLD:
        logger.info("Suspicious network activity detected")
        return True
    return False
