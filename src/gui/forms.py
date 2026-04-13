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
            H2("OSPF Configuration", cls="mb-3"),
            Fieldset(
                Div(
                    Label("Management IP", cls="col-sm-4 col-form-label"),
                    Div(Input(name="mgmt_ip", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("User", cls="col-sm-4 col-form-label"),
                    Div(Input(name="user", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("Secret", cls="col-sm-4 col-form-label"),
                    Div(Input(name="secret", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("OSPF ID", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ospf_id", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("OSPF Area", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ospf_area", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("OSPF Network", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ospf_network", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("OSPF Mask", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ospf_mask", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
            ),
            Button("Send", type="submit", cls="btn btn-primary mt-3"),
            cls="col-md-6 col-lg-4 mx-auto",  # <-- constrains width and centers
        )
    )


def int_ip_form():
    return Form(
        method="post",
        action="/ip_config",
    )(
        Div(
            H2("Interface IP Configuration", cls="mb-3"),
            Fieldset(
                Div(
                    Label("Management IP", cls="col-sm-4 col-form-label"),
                    Div(Input(name="mgmt_ip", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("User", cls="col-sm-4 col-form-label"),
                    Div(Input(name="user", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("Secret", cls="col-sm-4 col-form-label"),
                    Div(Input(name="secret", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("Interface", cls="col-sm-4 col-form-label"),
                    Div(Input(name="interface", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("New IP", cls="col-sm-4 col-form-label"),
                    Div(Input(name="new_ip", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
                Div(
                    Label("IP Mask", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ip_mask", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
            ),
            Button("Send", type="submit", cls="btn btn-primary mt-3"),
            cls="col-md-6 col-lg-4 mx-auto",
        )
    )
