from dataclasses import dataclass


@dataclass
class Router:
    index: int
    hostname: str
    ipv4: str
    ipv6: str
    ospf_area: int
    loopback: str
    user: str
    password: str


@dataclass
class TextConf:
    conf: str
    secret: str
    ip: str


@dataclass
class GrafanaQuery:
    host: str
    ip: str
    error: bool


@dataclass
class IpChange:
    mgmt_ip: str
    user: str
    secret: str
    interface: str
    new_ip: str
    ip_mask: str


@dataclass
class OspfChange:
    mgmt_ip: str
    user: str
    secret: str
    ospf_id: int
    ospf_area: int
    ospf_network: str
    ospf_mask: str
