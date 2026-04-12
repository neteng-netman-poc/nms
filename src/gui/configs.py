from fasthtml.common import H3, Label, Button, Div, Button, Form, Textarea, Ul, Li, Input, Span
import os

def pull_backup_files():
    # pull from api
    files = os.listdir("./src/backups/")

    return Div(
        Div(
            Div(
                H3("Load Config:"),
                Ul(*[Li(Button(f, hx_post="/load_conf", hx_target="#conf", hx_swap="innerHTML", hx_vals={"file": f})) for f in files]),
                cls="col",
            ),
            Div(edit_config("", ""), cls="col", id="conf"),
            cls="row",
        ),
        cls="container",
    )

def edit_config(name, text):
    return Div(
        H3(name),
        Form(
            action="/save_conf",
            method="post",
            hx_post="/save_conf",
            hx_target="#last_save",
            hx_swap="innerHTML",
            hx_indicator="#send_conf_btn",
            hx_disabled_elt="#send_conf_btn",
            )(
            Textarea(text, name="conf", cls="form-control", rows=20),
            Div(
                Label("SSH Secret:"),
                Input(name="secret"),
                cls="row",
            ),
            Div(
                Label("Send to IP:"),
                Input(name="ip"),
                cls="row",
            ),
            Button("Send Config", Span(cls="spinner-border spinner-border-sm ms-2 htmx-indicator"), type="submit", id="send_conf_btn", cls="btn btn-primary mt-2"),
        ),
        Div(id="last_save"),
        cls="container m-3"
    )
