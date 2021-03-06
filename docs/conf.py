# -- Path setup --

import os
import sys
import django
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MangAdventure.settings')
os.environ['MANGADV_IGNORE_CONFIG'] = 'true'
django.setup()

# -- Project information --

import MangAdventure

project = MangAdventure.__name__
author = MangAdventure.__author__
release = MangAdventure.__version__
copyright = MangAdventure.__copyright__


# -- General configuration --

extensions = [
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'en'
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store', 'desktop.ini', '.directory'
]
pygments_style = 'manni'


# -- Custom CSS --

def setup(app): app.add_stylesheet('css/style.css')


# -- Options for HTML output --

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'display_version': False,
    'collapse_navigation': True,
}
html_static_path = ['_static']
# html_sidebars = {}


# -- Options for HTMLHelp output --

htmlhelp_basename = '%sDoc' % project


# -- Options for LaTeX output --

latex_elements = {}
latex_documents = [(
    master_doc, '%s.tex' % project,
    '%s Documentation' % project, author, 'manual'
)]


# -- Options for manual page output --

man_pages = [(
    master_doc, project.lower(),
    '%s Documentation' % project, [author], 7
)]


# -- Options for Texinfo output --

texinfo_documents = [(
    master_doc, project, '%s Documentation' % project,
    author, project, MangAdventure.__doc__, 'Miscellaneous'
)]

