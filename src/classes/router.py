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

@dataclass
class GrafanaQuery:
    host: str
    ip: str
    error: bool


@dataclass
class IpV4Change:
    host: str
    interface: str
    new_ip: str
    ip_mask: str

@dataclass
class IpV6Change:
    host: str
    interface: str
    new_ip: str
    prefix_len: str


@dataclass
class OspfChange:
    host: str
    ospf_id: int
    ospf_area: int
    ospf_network: str
    ospf_mask: str
