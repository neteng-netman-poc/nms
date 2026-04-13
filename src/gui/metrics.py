from fasthtml.common import A, Button, Div, Table, Th, Tr, Td

from classes.router import GrafanaQuery


def query_grafana():
    """
    hit grafana api to find routers that are up and their status
    """

    test_data = [
        GrafanaQuery("R1", "10.0.0.1", False),
        GrafanaQuery("R2", "11.0.0.1", True),
        GrafanaQuery("R3", "11.0.0.2", False),
        GrafanaQuery("R4", "11.0.0.4", False),
        GrafanaQuery("R5", "10.0.0.2", False),
    ]
    return test_data


def metric_table():
    """
    get grafana data and renter as table with 'hostname' 'ip' and 'status'
    """

    data = query_grafana()
    rows = []
    for r in data:
        tr = Tr(
            Td(A(r.host, href="www.google.com")),
            Td(r.ip),
            Td(f"{'⚠' if r.error else '✓'}"),
            cls=f"{'table-warning' if r.error else ''}",
        )
        rows.append(tr)
    return Table(
        Tr(Th("Hostname"), Th("Management IP"), Th("Status")),
        *rows,
        cls="table table-bordered",
    )
