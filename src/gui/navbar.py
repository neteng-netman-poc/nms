from fasthtml.common import Nav, Div, Ul, A, Li


def navbar():
    """
    render navbar for GUI
    """

    return Nav(
        Div(
            Div(
                Ul(
                    Li(
                        A(
                            "Initial Confs",
                            cls="btn btn-outline-primary mx-2",
                            href="/router_confs",
                        ),
                        cls="nav-item",
                    ),
                    Li(
                        A("Metrics", cls="btn btn-outline-primary mx-2", href="/"),
                        cls="nav-item",
                    ),
                    Li(
                        A(
                            "Modify Configs",
                            cls="btn btn-outline-primary mx-2",
                            href="/router_forms",
                        ),
                        cls="nav-item",
                    ),
                    Li(
                        A(
                            "Backups",
                            cls="btn btn-outline-primary mx-2",
                            href="/router_backups",
                        ),
                        cls="nav-item",
                    ),
                    cls="navbar-nav justify-content-center w-100",
                ),
                cls="container w-100",
            ),
            cls="container",
        ),
        cls="navbar navbar-expand-lg bg-body-tertiary",
    )
