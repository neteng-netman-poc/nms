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
