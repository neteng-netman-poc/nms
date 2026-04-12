import time
# import requests

from fasthtml.common import *

from gui.navbar import navbar
from gui.utils import bootscript
from gui.configs import pull_backup_files, edit_config
from classes.router import TextConf


hdrs = (
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB",
        type="text/css",
        crossorigin="anonymous"
    ),
)


app = FastHTML(pico=False, hdrs=hdrs)

@app.get("/")
def home():
    return (
        Title("Grafana"),
        navbar(),
        Div(
            H1("Router Metrics"),
            cls="container"
        ),
        bootscript(),
    )

@app.get("/router_forms")
def router_forms():
    return (
        Title("Configs"),
        navbar(),
        Div(
            H1("Modify Router Configurations"),
            cls="container"
        ),
        bootscript(),
    )

@app.get("/router_confs")
def router_confs():
    return (
        Title("Configs"),
        navbar(),
        Div(
            H1("Pull Router Configurations"),
            cls="container"
        ),
        bootscript(),
    )

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
    with open(f"./src/backups/{file}", "r")  as f:
        text = f.read()
    return edit_config(file, text)

@app.post("/save_conf")
def save_conf(conf: TextConf):
    print(conf)
    time.sleep(3)
    # webhook to jenkins api endpoint
    return H4(f"sent config to {conf.ip}", cls="alert")

if __name__ == "__main__":
    serve()
