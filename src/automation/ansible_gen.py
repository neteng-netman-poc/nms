import csv
import yaml
import os
import subprocess
from netmiko import ConnectHandler


TASK_TEMPLATES = {
    "all": [
        {
            "name": "Generate full config from template",
            "template": "src=master_template.j2 dest=../configs/{{ item.hostname }}_all.txt",
            "with_items": "{{ routers }}",
            "tags": ["all"],
        }
    ],
    "ipv4": [
        {
            "name": "Generate ipv4 config from template",
            "template": "src=ipv4.j2 dest=../configs/{{ item.hostname }}_ipv4.txt",
            "with_items": "{{routers}}",
            "tags": ["ipv4"],
        }
    ],
    "ipv6": [
        {
            "name": "Generate ipv6 config from template",
            "template": "src=ipv6.j2 dest=../configs/{{ item.hostname }}_ipv6.txt",
            "with_items": "{{routers}}",
            "tags": ["ipv6"],
        }
    ],
    "hostname": [
        {
            "name": "Generate hostname config from template",
            "template": "src=hostname.j2 dest=../configs/{{ item.hostname }}_hostname.txt",
            "with_items": "{{routers}}",
            "tags": ["hostname"],
        }
    ],
    "ospf": [
        {
            "name": "Generate ospf config from template",
            "template": "src=ospf.j2 dest=../configs/{{ item.hostname }}_ospf.txt",
            "with_items": "{{routers}}",
            "tags": ["ospf"],
        }
    ],
}


WR_MEM_TASK = {
    "name": "Save running config",
    "cisco.ios.ios_command": {"commands": ["write memory"]},
}


def csv_to_hostvars(csv_filename):
    """Converts a CSV file containing device configuration information into Ansible host variables in YAML format.

    Args:
        csv_filename (string): The path to the CSV file containing device configuration information.
    """
    os.makedirs("./src/automation/roles/router/vars", exist_ok=True)

    vars = []
    csv_data = {}

    with open(csv_filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not any(row.values()):
                continue
            stripped_row = {}
            for key, value in row.items():
                if value is not None:
                    stripped_row[key.strip()] = value.strip()
            row = stripped_row

            hostname = row.pop("hostname")

            if hostname not in csv_data:
                csv_data[hostname] = {
                    "hostname": hostname,
                    "interfaces": [],
                    "ospf": {"process_id": int(row["process_id"]), "networks": []},
                }

            interface = {
                "name": row["name"],
                "ip_address": row["ip_address"],
                "subnet_mask": row["subnet_mask"],
                "ipv6_address": row["ipv6_address"],
                "prefix_length": int(row["prefix_length"]),
            }

            network = {
                "address": row["ospf_network"],
                "wildcard": row["ospf_wildcard"],
                "area": int(row["area_id"]),
            }

            csv_data[hostname]["interfaces"].append(interface)
            csv_data[hostname]["ospf"]["networks"].append(network)

    vars = list(csv_data.values())

    with open(f"./src/automation/roles/router/vars/main.yaml", "w") as output:
        yaml.dump({"routers": vars}, output, default_flow_style=False)


def csv_to_inventory(csv_filename, output_file="./src/automation/inventory/hosts.yaml"):
    """converts a csv file containing device connection information into an Ansible inventory file in YAML format.

    Args:
        csv_filename (str): The path to the CSV file containing device connection information.
        output_file (str, optional): The path to the output YAML inventory file. Defaults to 'inventory/hosts.yaml'.
    """
    os.makedirs("./src/automation/inventory", exist_ok=True)

    inventory = {"all": {"children": {"routers": {"hosts": {}}}}}
    hosts = inventory["all"]["children"]["routers"]["hosts"]

    with open(csv_filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            hostname = row["hostname"]
            hosts[hostname] = {
                "ansible_host": row["ansible_host"],
                "ansible_user": row["ansible_user"],
                "ansible_password": row["ansible_password"],
                "ansible_connection": "network_cli",
                "ansible_network_os": "ios",
            }

    with open(output_file, "w") as output:
        yaml.dump(inventory, output, default_flow_style=False)


def generate_tasks(selected_cfgs):
    """A function that generates Ansible tasks based on the selected configuration types and writes them to a YAML file.

    Args:
        selected_cfgs (list): A list of selected configuration types.
    """
    os.makedirs("./src/automation/roles/router/tasks", exist_ok=True)

    tasks = []
    
    tasks.append({
        'name': 'Create configs directory',
        'file': {
            'path': 'src/automation/configs',
            'state': 'directory',
            'mode': '0755' 
        }
    })

    for cfg in selected_cfgs:
        if cfg in TASK_TEMPLATES:
            tasks.extend(TASK_TEMPLATES[cfg])

    # tasks.append(WR_MEM_TASK)

    with open("./src/automation/roles/router/tasks/main.yaml", "w") as taskfile:
        yaml.dump(tasks, taskfile, default_flow_style=False, allow_unicode=True)


def generate_playbook(output_file, hosts="localhost"):
    """A function that generates an Ansible playbook and writes it to a YAML file.

    Args:
        output_file (str): The path to the output YAML playbook file.
        hosts (str, optional): The hosts to include in the playbook. Defaults to 'localhost'.
    """
    os.makedirs("./src/automation/playbooks", exist_ok=True)

    playbook = [
        {
            "name": f"Configure Network Devices",
            "hosts": hosts,
            "gather_facts": False,
            "roles": ["router"],
        }
    ]

    with open(output_file, "w") as output:
        yaml.dump(playbook, output, default_flow_style=False, allow_unicode=True)


def run_playbook(playbook_file, tags, inventory="./src/automation/inventory/hosts.yaml", dry_run=False):
    """A function to run an Ansible playbook with specific tags associated with tasks.

    Args:
        playbook_file (str): The path to the playbook file to run.
        tags (list): A list of tags to include in the playbook run.
        inventory (str, optional): The path to the inventory file. Defaults to "./src/automation/inventory/hosts.yaml".
        dry_run (bool, optional): Whether to perform a dry run. Defaults to False.

    Returns:
        int: The return code of the Ansible playbook run.
    """
    cmd = ["ansible-playbook", "-i", inventory, playbook_file]

    if dry_run:
        cmd.append("--check")

    if tags:
        cmd.extend(["--tags", ",".join(tags)])

    env = os.environ.copy()
    env["LC_ALL"] = "C.UTF-8"
    env["LANG"] = "C,UTF-8"

    result = subprocess.run(cmd, env=env)

    if result.returncode != 0:
        print(f"Playbook failed:\n{result.stderr}")
    else:
        print("Playbook completed successfully")

    return result.returncode


def config_devices(selected_cfgs, host_info_csv):
    """A function to configure devices using jinja 2 configs.

    Args:
        selected_cfgs (list): A list of selected configuration types.
        host_info_csv (str): The path to the CSV file containing host information.
    """
    hosts = []

    with open(host_info_csv, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            hosts.append(row)

    for host in hosts:
        device = {
            "device_type": "cisco_ios",
            "host": host["ansible_host"],
            "username": host["ansible_user"],
            "password": host["ansible_password"],
            "secret": host["ansible_password"],
        }

        connection = ConnectHandler(**device)
        connection.enable()
        os.makedirs("src/automation/configs", exist_ok=True)
        for cfg in selected_cfgs:
            cfg_file = f"src/automation/configs/{host['hostname']}_{cfg}.txt"
            print(cfg_file)
            connection.send_config_from_file(cfg_file)
        connection.disconnect()

def day1_configs():
    """
    A function to run the initial day 1 configurations on devices using Ansible playbooks and jinja2 templates.
    Generates the necessary IPv4 interface, IPv6 interface, and OSPF configuration files from templates, creates the Ansible playbook and tasks, and runs the playbook to apply the configurations to the devices.
    """
    selected_configs = ["all"]

    csv_to_inventory("src/automation/csv/ansible_hosts.csv")
    csv_to_hostvars("src/automation/csv/device_config_info.csv")

    generate_tasks(selected_configs)

    generate_playbook("src/automation/playbooks/config.yaml")

    run_playbook("src/automation/playbooks/config.yaml", tags=selected_configs)
    # if run_playbook("src/automation/playbooks/config.yaml", tags=selected_configs) == 0:
    #     config_devices(selected_configs, "src/automation/csv/ansible_hosts.csv")
