# Netman SNMP Prometheus Exporter

This module provides a scalable, async Python solution for polling SNMP data from network devices (e.g., routers) and exporting the runtime metrics directly to Prometheus.

The application automatically handles concurrency across multiple routers and generates highly structured Prometheus gauges labeled by `routername`, `routerip`, and `interface`.

## Directory Files

- `monitoring/GetSNMPdata.py` - Core engine for mapping high-level metrics and tabular OIDs to async SNMP queries via `pysnmp`.
- `monitoring/prometheus_exporter.py` - The main daemon that runs the SNMP fetch loop and safely exposes Prometheus telemetry on port `8787` for scraping.
- `monitoring/monitoring_configs.csv` - Target devices definition list.
- `monitoring/monitoring_oids.csv` - Metric map of OIDs to fetch per device.

## Prerequisites & Installation

Ensure you have **Python 3.10+** installed on your system (the exporter code uses type-hints like `str | None` and modern asyncio).

1. Clone or download the repository to your machine.
2. (Optional but recommended) Create and activate a python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required external Python packages:
   ```bash
   pip install pysnmp prometheus-client
   ```

## Configuration

Before starting, map out your network scope in the `CSV` files:

1. **`monitoring_configs.csv`**
   Add your routers here. You need the display name, IP address, SNMP community string, and version:
   ```csv
   routername,routerip,community,version
   R1,192.168.100.2,lab123,v2c
   ```

2. **`monitoring_oids.csv`**
   Add any extra scalar or interface OIDs you want to scrape here. The exporter automatically correlates interface tables (like `ifHCInOctets`) out of the box based on the OID definition names.

## Usage

Start the exporter by running `prometheus_exporter.py`. It will launch a listening HTTP web server on port `8787` and begin continuously fetching SNMP data in a 60-second loop.

```bash
# Navigate to the correct directory
cd monitoring

# Start the application
python3 prometheus_exporter.py
```

### Metrics Endpoint

The collected runtime telemetry is directly readable by pulling the `/metrics` endpoint:

```bash
curl http://localhost:8787/metrics
```

### Prometheus Integration

To officially collect these stats over time, add a scrape job to your central `prometheus.yml` server config file:

```yaml
scrape_configs:
  - job_name: 'custom_snmp_monitors'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['127.0.0.1:8787'] # Adjust to the exporter machine's IP if hosted elsewhere
```
