"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys
from datetime import datetime

# Add the source directory to Python path
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------

project = 'SurrealEngine'
copyright = f'{datetime.now().year}, SurrealEngine Contributors'
author = 'SurrealEngine Contributors'

# The full version, including alpha/beta/rc tags
release = '0.5.1'
version = '0.5.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx_wagtail_theme',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# MyST parser settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_wagtail_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
# Sidebar template configuration
try:
    _theme_name = html_theme
except NameError:
    _theme_name = 'alabaster'

if _theme_name == 'sphinx_wagtail_theme':
    html_sidebars = {}
else:
    html_sidebars = {}

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Set the permalink icon
html_permalinks_icon = "<span>¶</span>"

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# Todo extension settings
todo_include_todos = True

# Copy button settings
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# MyST parser settings
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    # "linkify",  # Disabled - requires linkify-it-py package
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# HTML output options
html_title = f"{project} Documentation"
html_short_title = project
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Wagtail theme options
html_theme_options = {
    'project_name': 'SurrealEngine Documentation',
    'logo': None,
    'logo_alt': 'SurrealEngine',
    'logo_height': 59,
    'logo_url': '/',
    'logo_width': 45,
    'github_url': 'https://github.com/iristech-systems/surrealengine',
}

# LaTeX output options
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'fncychap': '',
    'printindex': '',
}

# Grouping the document tree into LaTeX files
latex_documents = [
    (master_doc, 'SurrealEngine.tex', 'SurrealEngine Documentation',
     'SurrealEngine Contributors', 'manual'),
]

# -- Custom configuration ---------------------------------------------------

# Add custom CSS
def setup(app):
    """Set up the Sphinx application."""
    app.add_css_file('custom.css')

# Suppress warnings for external links
suppress_warnings = ['image.nonlocal_uri']

# Set up source file encoding
source_encoding = 'utf-8-sig'