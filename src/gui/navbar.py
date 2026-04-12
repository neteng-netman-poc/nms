from fasthtml.common import Nav, Div, Ul, A, Li

def navbar():
    return (
        Nav(
            Div(
                Div(
                    Ul(
                        Li(A("metrics", cls="nav-link", href="/"), cls="nav-item"),
                        Li(A("modify configs", cls="nav-link", href="/router_forms"), cls="nav-item"),
                        Li(A("view configs", cls="nav-link", href="/router_confs"), cls="nav-item"),
                        Li(A("backups", cls="nav-link", href="/router_backups"), cls="nav-item"),
                        cls="navbar-nav"
                    ),
                    cls="collapse navbar-collapse", id="navbarNav"
                ),
                cls="container-fluid"
            ),
            cls="navbar navbar-expand-lg bg-body-tertiary"
        )
    )
