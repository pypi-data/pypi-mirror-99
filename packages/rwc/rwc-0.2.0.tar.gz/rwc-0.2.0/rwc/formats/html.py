from . import render_func


@render_func('.html', '.htm')
def render_html(content):
    """Simple passthrough for existing HTML documents.
    """

    return content
