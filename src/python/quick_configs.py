from jinja2 import Template
from netmiko import ConnectHandler
import os

def config_ospf(process_id, area, network, wildcard_mask):
    with open('src/python/templates/ospf.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(process_id=process_id, area=area, network=network, wildcard_mask=wildcard_mask)

def config_ipv4_interface(name, ip_address, subnet_mask):
    with open('src/python/templates/ipv4.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(name=name, ip_address=ip_address, subnet_mask=subnet_mask)

def config_ipv6_interface(name, ipv6_address, prefix_length):
    with open('src/python/templates/ipv6.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(name=name, ipv6_address=ipv6_address, prefix_length=prefix_length)

def config_ipv4_route(destination, subnet_mask, next_hop):
    with open('src/python/templates/ipv4_route.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(destination=destination, subnet_mask=subnet_mask, next_hop=next_hop)

def config_ipv6_route(destination, prefix_length, next_hop):
    with open('src/python/templates/ipv6_route.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(destination=destination, prefix_length=prefix_length, next_hop=next_hop)

def config_bgp(as_number, neighbor_ip, remote_as):
    with open('src/python/templates/bgp.j2', 'r') as template_file:
        template = Template(template_file.read())
    return template.render(as_number=as_number, neighbor_ip=neighbor_ip, remote_as=remote_as)

def save_config_to_file(config, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as file:
        file.write(config)
    file.close()

def send_config_to_device(config, device_ip, username, password):
    
    device = {
        'device_type': 'cisco_ios',
        'host': device_ip,
        'username': username,
        'password': password,
        'secret': password
    }
    
    connection = ConnectHandler(**device)
    connection.send_config_set(config.splitlines())
    connection.send_command('write memory')
    connection.disconnect()
    
save_config_to_file(config_ipv4_interface("GigabitEthernet0/1", "192.168.1.1", "255.255.255.0"), "configs/gigabitethernet0_1.cfg")
