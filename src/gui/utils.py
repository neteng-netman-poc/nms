from fasthtml.common import Script, Footer, Div, A, P


def bootscript():
    """
    add required bootstrap js script
    """

    return Script(
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
    )

def footer():
    footer = Footer(
        Div(
            Div(
                Div(
                    P("© 2026 Barista. All rights reserved.", cls="mb-0 text-muted"),
                    cls="col-md-6"
                ),
                Div(
                    A("Privacy Policy", href="#", cls="text-muted me-3 text-decoration-none"),
                    A("Terms of Service", href="#", cls="text-muted me-3 text-decoration-none"),
                    A("Contact", href="#", cls="text-muted text-decoration-none"),
                    cls="col-md-6 text-md-end"
                ),
                cls="row align-items-center"
            ),
            cls="container"
        ),
        cls="footer bg-light border-top py-4 mt-auto"
    )
    return footer
