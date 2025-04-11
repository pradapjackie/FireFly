# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Path setup --------------------------------------------------------------

# Add backend path if you want to auto-document backend code later
sys.path.insert(0, os.path.abspath('../backend'))

# -- Project information -----------------------------------------------------

project = 'FireFly'
copyright = '2025, Oleg Gusak, Exinity'
author = 'Oleg Gusak'

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",  # Enable Markdown support
]

# Allow both .rst and .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ["_static"]

# -- MyST-Parser settings ----------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
]
