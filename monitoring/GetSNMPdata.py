import asyncio
import csv
import json
from pathlib import Path
from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine, CommunityData, UdpTransportTarget, ContextData,
    ObjectType, ObjectIdentity, get_cmd
)

TABLE_OIDS = {
    "ifHCInOctets", "ifHCOutOctets", "ifInErrors", "ifInDiscards",
    "ifOperStatus", "ifAdminStatus"
}

IF_NAME_OID = ".1.3.6.1.2.1.31.1.1.1.1"
IF_DESCR_OID = ".1.3.6.1.2.1.2.2.1.2"
MAX_IF_INDEX = 30
SEM = asyncio.Semaphore(10)  # max 10 concurrent SNMP gets


async def _get_oid(oid: str, target: str, version: str, community: str):
    async with SEM:
        try:
            error_indication, error_status, _, var_binds = await asyncio.wait_for(
                get_cmd(
                    SnmpEngine(),
                    CommunityData(community, mpModel=0 if version == "v1" else 1),
                    await UdpTransportTarget.create((target, 161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
                ),
                timeout=5
            )
        except asyncio.TimeoutError:
            return None

        if error_indication or error_status:
            return None
        val = str(var_binds[0][1])
        if "No Such" in val or "noSuch" in val.lower():
            return None
        return val


async def _discover_interfaces(target: str, version: str, community: str) -> dict:
    """Probe ifName 1..MAX_IF_INDEX in parallel, return {index: name} for non-empty names."""
    tasks = [
        _get_oid(f"{IF_NAME_OID}.{i}", target, version, community)
        for i in range(1, MAX_IF_INDEX + 1)
    ]
    results = await asyncio.gather(*tasks)
    return {
        str(i): val
        for i, val in enumerate(results, start=1)
        if val is not None and val.strip() != ""
    }


async def fetch_device_snmp_data(router_config: dict, oids: dict) -> dict:
    target_ip = router_config["routerip"]
    version = router_config["version"]
    community = router_config["community"]

    scalar_oids = {k: v for k, v in oids.items() if k not in TABLE_OIDS}
    table_oids = {k: v for k, v in oids.items() if k in TABLE_OIDS}

    # Step 1: scalars + discover interfaces (all parallel)
    scalar_keys = list(scalar_oids.keys())
    all_tasks = [
        _get_oid(scalar_oids[k], target_ip, version, community)
        for k in scalar_keys
    ]
    all_tasks.append(_discover_interfaces(target_ip, version, community))

    first_results = await asyncio.gather(*all_tasks)

    scalars = {scalar_keys[i]: (first_results[i] or "") for i in range(len(scalar_keys))}
    if_names = first_results[-1]

    # Step 2: all table OIDs for all interfaces (parallel with semaphore)
    table_keys = list(table_oids.keys())
    get_tasks = []
    task_map = []

    for idx in if_names:
        for key in table_keys:
            get_tasks.append(
                _get_oid(f"{table_oids[key]}.{idx}", target_ip, version, community)
            )
            task_map.append((idx, key))

    table_results = await asyncio.gather(*get_tasks)

    interfaces = {key: {} for key in table_keys}
    for i, (idx, key) in enumerate(task_map):
        interfaces[key][if_names[idx]] = table_results[i] or "N/A"

    return {
        "routername": router_config["routername"],
        "routerip": router_config["routerip"],
        "scalar": scalars,
        "interfaces": interfaces
    }


async def get_all_snmp_data(configs_file: str, oids_file: str) -> list:
    oids = {}
    with open(oids_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("name") and row.get("oid"):
                oids[row["name"]] = row["oid"]

    routers = []
    with open(configs_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            routers.append(row)

    return await asyncio.gather(*[
        fetch_device_snmp_data(router, oids) for router in routers
    ])


def main():
    base_dir = Path(__file__).parent
    configs_path = base_dir / "monitoring_configs.csv"
    oids_path = base_dir / "monitoring_oids.csv"

    results = asyncio.run(get_all_snmp_data(str(configs_path), str(oids_path)))
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()