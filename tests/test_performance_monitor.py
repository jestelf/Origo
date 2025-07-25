"""Tests for the PerformanceMonitor tool."""

import time

from devtools.performance_monitor import PerformanceMonitor


def test_monitor_records_subsystem_time():
    monitor = PerformanceMonitor()
    monitor.start_frame()
    monitor.start_subsystem("update")
    time.sleep(0.01)
    monitor.end_subsystem("update")
    monitor.end_frame()
    assert "update" in monitor.subsystems
    assert monitor.fps > 0
