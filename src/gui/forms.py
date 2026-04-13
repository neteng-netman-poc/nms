from fasthtml.common import Label, Button, Div, Form, Fieldset, H2, Input

def ospf_form():
    return Form(
        method="post",
        action="/ospf_config",
    )(
        Div(
            H2("OSPF Configuration", cls="mb-3"),
            Fieldset(
                Div(
                    Label("Hostname", cls="col-sm-4 col-form-label"),
                    Div(Input(name="host", cls="form-control"), cls="col-sm-8"),
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
            cls="col-md-6 col-lg-4 mx-auto",
        )
    )


def int_ipv4_form():
    return Form(
        method="post",
        action="/ipv4_config",
    )(
        Div(
            H2("Interface IPv4 Configuration", cls="mb-3"),
            Fieldset(
                Div(
                    Label("Hostname", cls="col-sm-4 col-form-label"),
                    Div(Input(name="host", cls="form-control"), cls="col-sm-8"),
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

def int_ipv6_form():
    return Form(
        method="post",
        action="/ipv6_config",
    )(
        Div(
            H2("Interface IPv6 Configuration", cls="mb-3"),
            Fieldset(
                Div(
                    Label("Hostname", cls="col-sm-4 col-form-label"),
                    Div(Input(name="host", cls="form-control"), cls="col-sm-8"),
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
                    Label("Prefix Length", cls="col-sm-4 col-form-label"),
                    Div(Input(name="ip_mask", cls="form-control"), cls="col-sm-8"),
                    cls="row mb-2 align-items-center",
                ),
            ),
            Button("Send", type="submit", cls="btn btn-primary mt-3"),
            cls="col-md-6 col-lg-4 mx-auto",
        )
    )
