import logging
from collections import deque

logger = logging.getLogger(__name__)


class TrafficAnalyzer:
    """Simple analyzer for network packets."""

    def __init__(self, max_history: int = 100) -> None:
        self.max_history = max_history
        self.packet_sizes = deque(maxlen=max_history)
        self.suspicious_packets = 0

    def analyze_packet(self, packet: bytes) -> None:
        """Analyze a single network packet."""
        size = len(packet)
        self.packet_sizes.append(size)
        if size > 64 * 1024:
            self.suspicious_packets += 1
            logger.debug("Suspicious packet size: %d", size)

    def get_suspicious_count(self) -> int:
        return self.suspicious_packets

    def reset(self) -> None:
        self.packet_sizes.clear()
        self.suspicious_packets = 0
