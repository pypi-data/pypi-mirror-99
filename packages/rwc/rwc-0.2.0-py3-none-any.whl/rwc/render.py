from .formats import RENDER_FUNCTIONS
from html_sanitizer import Sanitizer
from pathlib import Path
import re


def sanitize(content):
    """Get just the text from the HTML ``content``.
    """

    sanitizer = Sanitizer({
        'tags': set('this-tag-will-never-exist-in-html'),
        'attributes': {},
        'empty': set(),
        'separate': set(),
    })

    return sanitizer.sanitize(content)


def can_render(filename):
    ext = Path(filename).suffix
    renderer = RENDER_FUNCTIONS.get(ext, None)
    return renderer is not None


def render(filename, content):
    """Render the ``content`` as HTML, using the renderer from
    the file extension from ``filename``.
    """

    ext = Path(filename).suffix
    renderer = RENDER_FUNCTIONS.get(ext, None)
    if renderer is None:
        return None

    output = renderer(content)
    output = sanitize(output)
    return output


def wordcount(filename, content):
    """Get the word count for the ``content``, using the renderer from
    the file extension from ``filename``.
    """

    output = render(filename, content)
    if output is None:
        return None

    match = re.findall(r"\w+", output, re.MULTILINE)
    return len(match)
