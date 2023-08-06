from . import render_func
from docutils.core import publish_parts


@render_func('.rst')
def render_rst(content):
    """Render the reStructuredText ``content`` to HTML.
    """

    parts = publish_parts(content, writer_name='html')
    return parts["html_body"]
