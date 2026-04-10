#!/usr/bin/env python3
"""
prometheus_exporter.py

Polls SNMP data every 60 seconds via GetSNMPdata and exposes the results
as Prometheus metrics on port 8787.

All metrics carry 'routername' and 'routerip' labels.
Interface-level metrics additionally carry an 'interface' label.

Usage:
    python prometheus_exporter.py

Metrics endpoint:
    http://localhost:8787/metrics
"""

import asyncio
import time
from pathlib import Path

from prometheus_client import start_http_server, Gauge

from GetSNMPdata import get_all_snmp_data

PORT = 8787
POLL_INTERVAL = 60  # seconds

BASE_DIR = Path(__file__).parent
CONFIGS_PATH = str(BASE_DIR / "monitoring_configs.csv")
OIDS_PATH = str(BASE_DIR / "monitoring_oids.csv")

# ── Device-level labels ────────────────────────────────────────────────────────
DEV = ["routername", "routerip"]

# ── Scalar metrics ─────────────────────────────────────────────────────────────
snmp_uptime = Gauge(
    "snmp_uptime_ticks",
    "System uptime in timeticks (sysUpTime .1.3.6.1.2.1.1.3.0)",
    DEV,
)
snmp_cpu_load_5min = Gauge(
    "snmp_cpu_load_5min_percent",
    "5-minute CPU load % (Cisco ciscoProcessMIB .1.3.6.1.4.1.9.9.109...)",
    DEV,
)
snmp_memory_used = Gauge(
    "snmp_memory_pool_used_bytes",
    "Cisco memory pool used bytes (ciscoMemoryPoolUsed)",
    DEV,
)
snmp_memory_free = Gauge(
    "snmp_memory_pool_free_bytes",
    "Cisco memory pool free bytes (ciscoMemoryPoolFree)",
    DEV,
)

# ── Interface-level labels ─────────────────────────────────────────────────────
IFACE = ["routername", "routerip", "interface"]

# ── Interface metrics ──────────────────────────────────────────────────────────
snmp_iface_in_octets = Gauge(
    "snmp_interface_hc_in_octets_total",
    "HC inbound octets on interface (ifHCInOctets)",
    IFACE,
)
snmp_iface_out_octets = Gauge(
    "snmp_interface_hc_out_octets_total",
    "HC outbound octets on interface (ifHCOutOctets)",
    IFACE,
)
snmp_iface_in_errors = Gauge(
    "snmp_interface_in_errors_total",
    "Inbound errors on interface (ifInErrors)",
    IFACE,
)
snmp_iface_in_discards = Gauge(
    "snmp_interface_in_discards_total",
    "Inbound discards on interface (ifInDiscards)",
    IFACE,
)
snmp_iface_oper_status = Gauge(
    "snmp_interface_oper_status",
    "Interface operational status: 1=up 2=down (ifOperStatus)",
    IFACE,
)
snmp_iface_admin_status = Gauge(
    "snmp_interface_admin_status",
    "Interface admin status: 1=up 2=down (ifAdminStatus)",
    IFACE,
)

# ── SNMP key → Gauge mapping ───────────────────────────────────────────────────
IFACE_METRIC_MAP = {
    "ifHCInOctets":  snmp_iface_in_octets,
    "ifHCOutOctets": snmp_iface_out_octets,
    "ifInErrors":    snmp_iface_in_errors,
    "ifInDiscards":  snmp_iface_in_discards,
    "ifOperStatus":  snmp_iface_oper_status,
    "ifAdminStatus": snmp_iface_admin_status,
}

SCALAR_METRIC_MAP = [
    ("uptime",               snmp_uptime),
    ("cpuLoad5min",          snmp_cpu_load_5min),
    ("ciscoMemoryPoolUsed",  snmp_memory_used),
    ("ciscoMemoryPoolFree",  snmp_memory_free),
]


def _to_float(val: str | None) -> float | None:
    """Safely convert an SNMP string value to float; returns None on failure."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def update_metrics(devices: list) -> None:
    """Push collected SNMP data into Prometheus Gauge objects."""
    for device in devices:
        rname = device["routername"]
        rip   = device["routerip"]
        dev   = {"routername": rname, "routerip": rip}

        # Scalar metrics
        for snmp_key, gauge in SCALAR_METRIC_MAP:
            v = _to_float(device["scalar"].get(snmp_key))
            if v is not None:
                gauge.labels(**dev).set(v)

        # Interface metrics
        for snmp_key, gauge in IFACE_METRIC_MAP.items():
            for iface, raw in device["interfaces"].get(snmp_key, {}).items():
                v = _to_float(raw)
                if v is not None:
                    gauge.labels(routername=rname, routerip=rip, interface=iface).set(v)


# Single persistent event loop — reused across all polls so the module-level
# asyncio.Semaphore in GetSNMPdata stays bound to the same loop forever.
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


def poll_loop() -> None:
    """Collect SNMP data every POLL_INTERVAL seconds and update metrics."""
    while True:
        t0 = time.monotonic()
        print(f"[poll] Collecting SNMP data ...")
        try:
            devices = _loop.run_until_complete(get_all_snmp_data(CONFIGS_PATH, OIDS_PATH))
            update_metrics(devices)
            elapsed = time.monotonic() - t0
            print(f"[poll] Updated {len(devices)} device(s) in {elapsed:.1f}s")
        except Exception as exc:
            print(f"[poll] ERROR: {exc}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    start_http_server(PORT)
    print(f"[exporter] Metrics server listening on port {PORT}")
    print(f"[exporter] Scrape endpoint → http://localhost:{PORT}/metrics")
    print(f"[exporter] Poll interval   → {POLL_INTERVAL}s")
    poll_loop()
