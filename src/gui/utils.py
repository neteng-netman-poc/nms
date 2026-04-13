from fasthtml.common import Script


def bootscript():
    """
    add required bootstrap js script
    """

    return Script(
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
    )
