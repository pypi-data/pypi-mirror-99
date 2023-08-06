from . import render_func
import markdown


@render_func('.md', '.mkd', '.markdown')
def render_markdown(content):
    """Render the Markdown ``content`` to HTML.
    """

    return markdown.markdown(content)
