from fasthtml.common import Label, Button, Div, Form, Fieldset, H2, Input

"""
@dataclass
class IpChange:
    mgmt_ip: str
    user: str
    secret: str
    interface: str
    new_ip: str
    ip_mask: str

@dataclass
class OspfChange:
    mgmt_ip: str
    user: str
    secret: str
    ospf_id: int
    ospf_area: int
    ospf_network: str
    ospf_mask: str
"""

def ospf_form():
    return Form(
            method="post",
            action="/ospf_config",
        )(
        Div(
            Div(
                H2("OSPF Configuration"),
                Fieldset(
                    Div(
                        Label("Management IP", cls="col-xs-4"),
                        Input(name="mgmt_ip", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("User", cls="col-xs-4"),
                        Input(name="user", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("Secret", cls="col-xs-4"),
                        Input(name="secret", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("OSPF ID", cls="col-xs-4"),
                        Input(name="ospf_id", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("OSPF Network", cls="col-xs-4"),
                        Input(name="ospf_network", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("OSPF Mask", cls="col-xs-4"),
                        Input(name="ospf_mask", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                ),
                Button("Send", type="submit", cls="btn btn-primary mt-4"),
            ),
        )
    )


def int_ip_form():
    return Form(
            method="post",
            action="/ip_config",
        )(
        Div(
            Div(
                H2("Interface IP Configuration"),
                Fieldset(
                    Div(
                        Label("Management IP", cls="col-xs-4"),
                        Input(name="mgmt_ip", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("User", cls="col-xs-4"),
                        Input(name="user", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("Secret", cls="col-xs-4"),
                        Input(name="secret", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("Interface", cls="col-xs-4"),
                        Input(name="interface", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("New IP", cls="col-xs-4"),
                        Input(name="new_ip", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                    Div(
                        Label("IP Mask", cls="col-xs-4"),
                        Input(name="ip_mask", type="text", cls="col-xs-8"),
                        cls="row",
                    ),
                ),
                Button("Send", type="submit", cls="btn btn-primary mt-4"),
            ),
        )
    )
