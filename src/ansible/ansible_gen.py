import csv
import yaml
import os
import subprocess
from netmiko import ConnectHandler


TASK_TEMPLATES = { 
    'ipv4': [ 
        { 
            'name': 'Generate ipv4 config from template', 
            'template': 'src=ipv4.j2 dest=../configs/{{ item.hostname }}_ipv4.txt', 
            'with_items': '{{routers}}',
            'tags': ['ipv4']
        }
    ], 
    'ipv6': [ 
        { 
            'name': 'Generate ipv6 config from template', 
            'template': 'src=ipv6.j2 dest=../configs/{{ item.hostname }}_ipv6.txt', 
            'with_items': '{{routers}}',
            'tags': ['ipv6']
        }
    ], 
    'hostname': [ 
        { 
            'name': 'Generate hostname config from template', 
            'template': 'src=hostname.j2 dest=../configs/{{ item.hostname }}_hostname.txt', 
            'with_items': '{{routers}}',
            'tags': ['hostname']
        }
    ], 
    'ospf': [ 
        { 
            'name': 'Generate ospf config from template', 
            'template': 'src=ospf.j2 dest=../configs/{{ item.hostname }}_ospf.txt', 
            'with_items': '{{routers}}',
            'tags': ['ospf']
        }
    ] 
}

 
WR_MEM_TASK = { 
    'name': 'Save running config', 
    'cisco.ios.ios_command': { 
        'commands': ['write memory'] 
    }
}


def csv_to_hostvars(csv_filename):
    """Converts a CSV file containing device configuration information into Ansible host variables in YAML format.

    Args:
        csv_filename (string): The path to the CSV file containing device configuration information.
    """
    os.makedirs('roles/router/vars', exist_ok=True)
    
    vars = []
    csv_data = {}
    
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not any(row.values()):
                continue
            stripped_row = {}
            for key, value in row.items():
                if value is not None:
                    stripped_row[key.strip()] = value.strip()
            row = stripped_row
            
            hostname = row.pop('hostname')
            
            if hostname not in csv_data:
                csv_data[hostname] = {
                    'hostname': hostname,
                    'interfaces': [],
                    'ospf': {
                        'process_id': int(row['process_id']),
                        'networks': []
                    }
                }
            
            interface = { 
                'name': row['name'], 
                'ip_address': row['ip_address'], 
                'subnet_mask': row['subnet_mask'], 
                'ipv6_address': row['ipv6_address'], 
                'prefix_length': int(row['prefix_length']) 
            }
            
            network = {
                'address': row['ospf_network'], 
                'wildcard': row['ospf_wildcard'], 
                'area': int(row['area_id']) 
            }
            
            csv_data[hostname]['interfaces'].append(interface)
            csv_data[hostname]['ospf']['networks'].append(network)
            
            for router in csv_data.values():
                vars.append(router)

            with open(f'roles/router/vars/main.yaml', 'w') as output:
                yaml.dump({'routers': vars}, output, default_flow_style=False)
                
def csv_to_inventory(csv_filename, output_file='inventory/hosts.yaml'):
    """_summary_

    Args:
        csv_filename (_type_): _description_
        output_file (str, optional): _description_. Defaults to 'inventory/hosts.yaml'.
    """
    os.makedirs('inventory', exist_ok=True)
    
    inventory = { 'all': { 'children': { 'routers': { 'hosts': {}}}}}
    hosts = inventory['all']['children']['routers']['hosts']
    
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hostname = row['hostname']
            hosts[hostname] = {
                # NEED TO UPDATE THE NAMES OF THESE TO PROPERLY MAKE A CSV FOR CONNECTING
                'ansible_host': row['ansible_host'],
                'ansible_user': row['ansible_user'],
                'ansible_password': row['ansible_password'],
                'ansible_connection': 'network_cli',
                'ansible_network_os': 'ios'
            }
    
    
    
    with open(output_file, 'w') as output:
        yaml.dump(inventory, output, default_flow_style=False)    

def generate_tasks(selected_cfgs):
    os.makedirs('roles/router/tasks', exist_ok=True)
    
    tasks = []
    
    # tasks.append({
    #     'name': 'Create configs directory',
    #     'file': {
    #         'path': './configs',
    #         'state': 'directory'
    #     }
    # })
    
    for cfg in selected_cfgs:
        if cfg in TASK_TEMPLATES:
            tasks.extend(TASK_TEMPLATES[cfg])
        
    # tasks.append(WR_MEM_TASK)
    
    with open('roles/router/tasks/main.yaml', 'w') as taskfile:
        yaml.dump(tasks, taskfile, default_flow_style=False, allow_unicode=True)

def generate_playbook(output_file, template, hosts='localhost'):
    """_summary_

    Args:
        output_file (_type_): _description_
        template (_type_): _description_
        hosts (str, optional): _description_. Defaults to 'localhost'.
    """
    os.makedirs('playbooks', exist_ok=True)
    
    playbook = [{
        'name': f'Configure {template.upper()} Interface',
        'hosts': hosts,
        'gather_facts': False,
        'roles': ['router']
    }]
    
    with open(output_file, 'w') as output:
        yaml.dump(playbook, output, default_flow_style=False, allow_unicode=True)
        
        
def run_playbook(playbook_file, inventory='inventory/hosts.yaml', dry_run=False):
    cmd = ['ansible-playbook', '-i', inventory, playbook_file]
    
    if dry_run:
        cmd.append('--check')
        
    env = os.environ.copy()
    env['LC_ALL'] = 'C.UTF-8'
    env['LANG'] = 'C,UTF-8'
        
    result = subprocess.run(cmd, env=env)
    
    if result.returncode != 0:
        print(f"Playbook failed:\n{result.stderr}")
    else:
        print("Playbook completed successfully")
    
    return result.returncode
        

def config_devices(selected_cfgs, host_info_csv):
    hosts = []
    
    with open(host_info_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hosts.append(row)
            
    for host in hosts:
        device = {
            'device_type': 'cisco_ios',
            'host': host['ansible_host'],
            'username': host['ansible_user'],
            'password': host['ansible_password'],
            'secret': host['ansible_password']
        }
        
        connection = ConnectHandler(**device)
        connection.enable()
        for cfg in selected_cfgs:
            cfg_file = f"./configs/{host['hostname']}_{cfg}.txt"
            print(cfg_file)
            print(connection.send_config_from_file(cfg_file))
        connection.disconnect()
        

csv_to_inventory('./csv/ansible_hosts.csv')
csv_to_hostvars('./csv/device_config_info.csv')

generate_tasks(['ipv4', 'ipv6', 'ospf'])

generate_playbook('./playbooks/config_ipv4.yaml', template='ipv4')
generate_playbook('./playbooks/config_ipv6.yaml', template='ipv6')
generate_playbook('./playbooks/config_ospf.yaml', template='ospf')

if run_playbook('playbooks/config_ipv4.yaml') == 0:
    config_devices(['ipv4'], './csv/ansible_hosts.csv')
if run_playbook('playbooks/config_ipv6.yaml') == 0:
    config_devices(['ipv6'], './csv/ansible_hosts.csv')
if run_playbook('playbooks/config_ospf.yaml') == 0:
    config_devices(['ospf'], './csv/ansible_hosts.csv')
