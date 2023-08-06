RENDER_FUNCTIONS = {}


def render_func(*extensions):
    """Register a function as an HTML renderer for the given file
    extensions.
    """

    def inner(function):
        global RENDER_FUNCTIONS
        for ext in extensions:
            RENDER_FUNCTIONS[ext] = function

        return function
    return inner


from . import restructuredtext
from . import markdown
