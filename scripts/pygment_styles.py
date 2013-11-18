#!/usr/bin/env python
"""
Print CSS declarations required by the Pygments syntax highlighter. This
should be saved to src/static/stylesheets/pygments.css
"""

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

print(HtmlFormatter().get_style_defs('.highlight'))
