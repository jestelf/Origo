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


def test_report_contains_metrics():
    monitor = PerformanceMonitor()
    monitor.start_frame()
    monitor.start_subsystem("update")
    time.sleep(0.01)
    monitor.end_subsystem("update")
    monitor.end_frame()
    report = monitor.report()
    assert "FPS:" in report
    assert "CPU:" in report
    assert "Memory:" in report
    assert "update:" in report
