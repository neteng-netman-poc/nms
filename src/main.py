import time
# import requests

from fasthtml.common import *

from gui.forms import int_ip_form, ospf_form
from gui.navbar import navbar
from gui.utils import bootscript
from gui.configs import pull_backup_files, edit_config
from gui.metrics import metric_table
from classes.router import IpChange, OspfChange, TextConf


hdrs = (
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB",
        type="text/css",
        crossorigin="anonymous",
    ),
)


app = FastHTML(pico=False, hdrs=hdrs)


@app.get("/")
def home():
    """
    render homepage as grafana table
    """

    return (
        Title("Grafana"),
        navbar(),
        Div(
            H1("Router Metrics"),
            metric_table(),
            cls="container text-center",
        ),
        bootscript(),
    )


@app.get("/router_forms")
def router_forms():
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
                    "Interface",
                    hx_post="/ip_form",
                    hx_target="#router_form",
                    hx_swap="innerHTML",
                    cls="btn btn-outline-primary",
                ),
            ),
            Div(id="router_form", cls="mt-3"),
            cls="container mt-4 text-center",
        ),
        bootscript(),
    )


@app.post("/ospf_form")
def ospf_form_html():
    return ospf_form()


@app.post("/ip_form")
def ip_form_html():
    return int_ip_form()


@app.get("/router_confs")
def router_confs():
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
    )


@app.post("/init_conf")
def init_conf():
    time.sleep(2)
    return H4(f"sent initial configurations", cls="alert")


@app.get("/router_backups")
def router_backups():
    return (
        Title("Backup Configs"),
        navbar(),
        Div(
            H1("Backed Up Router Configurations"),
            pull_backup_files(),
            cls="container",
        ),
        bootscript(),
    )


@app.post("/load_conf")
def load_conf(file: str):
    with open(f"./src/backups/{file}", "r") as f:
        text = f.read()
    return edit_config(file, text)


@app.post("/save_conf")
def save_conf(conf: TextConf):
    print(conf)
    time.sleep(3)
    # webhook to jenkins api endpoint
    return H4(f"sent config to {conf.ip}", cls="alert")


@app.post("/ospf_config")
def ospf_config(conf: OspfChange):
    pass


@app.post("/ip_config")
def ip_config(conf: IpChange):
    pass


if __name__ == "__main__":
    serve()
