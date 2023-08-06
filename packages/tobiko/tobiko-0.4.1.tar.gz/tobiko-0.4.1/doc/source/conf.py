# Copyright 2019 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOBIKO_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
sys.path.insert(0, TOBIKO_DIR)


# -- Python logging ----------------------------------------------------------

import logging
from tools import common

common.setup_logging(level=logging.INFO)


# -- Project information -----------------------------------------------------

project = 'Tobiko'
copyright = "2019, Red Hat"
author = "Tobiko's Team"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

from tools import get_version
release = get_version.get_version()
version = '.'.join(release.split('.', 2)[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.graphviz',
    'sphinx.ext.todo',
    'oslo_config.sphinxext',
    'oslo_config.sphinxconfiggen',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# openstackdocstheme options
repository_name = 'x/tobiko'
bug_project = 'tobiko'
bug_tag = 'doc'

# Set to True if using StoryBoard
use_storyboard = True

todo_include_todos = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "canonical_url": "https://docs.openstack.org/tobiko/latest/",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "top",
    "style_external_links": True,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for oslo_config.sphinxconfiggen ---------------------------------

_config_generator_config_files = [
    'tobiko.conf',
]


def _get_config_generator_config_definition(conf):
    config_file_path = '../../etc/oslo-config-generator/%s' % conf
    # oslo_config.sphinxconfiggen appends '.conf.sample' to the filename,
    # strip file extentension (.conf or .ini).
    output_file_path = '_static/config-samples/%s' % conf.rsplit('.', 1)[0]
    return config_file_path, output_file_path


config_generator_config_file = [
    _get_config_generator_config_definition(conf)
    for conf in _config_generator_config_files
]
