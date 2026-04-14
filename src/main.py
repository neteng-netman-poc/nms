import time
import requests
import json

from fasthtml.common import *

from gui.forms import int_ipv4_form, int_ipv6_form, ospf_form
from gui.navbar import navbar
from gui.utils import bootscript, footer
from gui.configs import pull_backup_files, edit_config
from gui.metrics import metric_table
from classes.router import IpV4Change, IpV6Change, OspfChange
from automation.ansible_gen import day1_configs
import python.quick_configs as quick_configs


hdrs = (
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB",
        type="text/css",
        crossorigin="anonymous",
    ),
    Style("body { display: flex; flex-direction: column; min-height: 100vh; }"),
)


app = FastHTML(pico=False, hdrs=hdrs)


@app.get("/")
def home():
    """
    Render homepage as grafana table.
    """

    return (
        Title("Grafana"),
        navbar(),
        Div(
            H1("Router Metrics", cls="m-4"),
            metric_table(),
            cls="container text-center",
        ),
        bootscript(),
        footer(),
    )


@app.get("/router_forms")
def router_forms():
    """
    Render router config forms for interface ips or ospf.
    """

    return (
        Title("Configs"),
        navbar(),
        Div(
            H1("Modify Router Configurations", cls="mb-4"),
            Div(
                cls="btn-group mb-4",
                role="group",
            )(
                Button(
                    "OSPF",
                    hx_post="/ospf_form",
                    hx_target="#router_form",
                    hx_swap="innerHTML",
                    cls="btn btn-outline-primary",
                ),
                Button(
                    "IPv4",
                    hx_post="/ipv4_form",
                    hx_target="#router_form",
                    hx_swap="innerHTML",
                    cls="btn btn-outline-primary",
                ),
                Button(
                    "IPv6",
                    hx_post="/ipv6_form",
                    hx_target="#router_form",
                    hx_swap="innerHTML",
                    cls="btn btn-outline-primary",
                ),
            ),
            Div(id="router_form", cls="mt-3"),
            cls="container mt-4 text-center",
        ),
        bootscript(),
        footer(),
    )


@app.post("/ospf_form")
def ospf_form_html():
    """
    Render GUI ospf_form component.
    """

    return ospf_form()


@app.post("/ipv4_form")
def ip_form_html():
    """
    Render GUI int_ip_form component.
    """

    return int_ipv4_form()

@app.post("/ipv6_form")
def ip_form_html():
    """
    Render GUI int_ip_form component.
    """

    return int_ipv6_form()


@app.get("/router_confs")
def router_confs():
    """
    Render page for deploying intial router configurations.
    """

    return (
        Title("Configs"),
        navbar(),
        Div(
            Div(
                H1("Send Initial Configs", cls="mb-3"),
                Button(
                    "Deploy",
                    Span(cls="spinner-border spinner-border-sm ms-1 htmx-indicator"),
                    hx_post="/init_conf",
                    hx_target="#initial_conf",
                    hx_swap="innerHTML",
                    hx_indicator="#init_conf_btn",
                    hx_disabled_elt="#init_conf_btn",
                    type="submit",
                    id="init_conf_btn",
                    cls="btn btn-primary",
                ),
                cls="col",
            ),
            Div(Div(id="initial_conf"), cls="row mt-3"),
            cls="container mt-4 text-center",
        ),
        bootscript(),
        footer(),
    )


@app.post("/init_conf")
def init_conf():
    """
    Run the initial router configurations and render results.
    """
    text = day1_configs()
    print(text)
    
    return Pre(text)


@app.get("/router_backups")
def router_backups():
    """
    Get backups from server and render as a list of clickable buttons. Each button
    loads the config in the textarea of the form to the right.
    """

    return (
        Title("Backup Configs"),
        navbar(),
        Div(
            H1("Backed Up Router Configurations", cls="text-center m-4"),
            pull_backup_files(),
            cls="container",
        ),
        bootscript(),
        footer(),
    )


@app.post("/load_conf")
def load_conf(file: str):
    """
    Load text from configuration. In testing it will be a test file from 'backups/'.
    """

    try:
        req = f"https://api-netman.dheerajgajula.com/api/config/all?router_hostname={file}"
        res = requests.get(req)
        text = res.json()
        text = text["configs"]["golden_running_configs"]["backed_up_config"]
    except:
        text = ""

    return edit_config(file, text)


@app.post("/save_conf")
def save_conf(conf: str, name: str):
    """
    Send updated config to desired device and render the result.
    """

    url = f"https://api-jenkins.dheerajgajula.com/config/{name}"

    payload = json.dumps({
      "config": conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank")


@app.post("/ospf_config")
def ospf_config(conf: OspfChange):
    """
    Send the new OSPF configuration to the desired device and render the result.
    """
    
    new_conf = quick_configs.config_ospf(conf.ospf_id, conf.ospf_area, conf.ospf_network, conf.ospf_mask)

    url = f"https://api-jenkins.dheerajgajula.com/config/{conf.host}"

    payload = json.dumps({
      "config": new_conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return navbar(), H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank"), bootscript(), footer()


@app.post("/ipv6_config")
def ipv6_config(conf: IpV6Change):
    """
    Send the new IP configuration to the desired device and render the result.
    """

    new_conf = quick_configs.config_ipv6_interface(conf.interface, conf.new_ip, conf.prefix_len)

    url = f"https://api-jenkins.dheerajgajula.com/config/{conf.host}"

    payload = json.dumps({
      "config": new_conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return navbar(), H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank"), bootscript(), footer()

@app.post("/ipv4_config")
def ipv4_config(conf: IpV4Change):
    """
    Send the new IP configuration to the desired device and render the result.
    """

    new_conf = quick_configs.config_ipv4_interface(conf.interface, conf.new_ip, conf.ip_mask)

    url = f"https://api-jenkins.dheerajgajula.com/config/{conf.host}"

    payload = json.dumps({
      "config": new_conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return navbar(), H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank"), bootscript(), footer()

@app.post("/ipv4_route")
def ipv4_config(conf: IpV4Change):
    """
    Send the new IP configuration to the desired device and render the result.
    """

    new_conf = quick_configs.config_ipv4_route(conf.interface, conf.new_ip, conf.ip_mask)

    url = f"https://api-jenkins.dheerajgajula.com/config/{conf.host}"

    payload = json.dumps({
      "config": new_conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return navbar(), H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank"), bootscript(), footer()

@app.post("/ipv6_route")
def ipv4_config(conf: IpV6Change):
    """
    Send the new IP configuration to the desired device and render the result.
    """

    new_conf = quick_configs.config_ipv6_route(conf.interface, conf.new_ip, conf.prefix_len)

    url = f"https://api-jenkins.dheerajgajula.com/config/{conf.host}"

    payload = json.dumps({
      "config": new_conf
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = "Sent Config" if response.ok else "Failed to Send"

    return navbar(), H4(text, cls="alert"), A("Jenkins Pipeline", cls="m-4", href="https://jenkins.dheerajgajula.com/job/jenkins-config-change-pipeline/", target="_blank"), bootscript(), footer()


if __name__ == "__main__":
    serve()
