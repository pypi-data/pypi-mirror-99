# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['penelope',
 'penelope.co_occurrence',
 'penelope.co_occurrence.hal_or_glove',
 'penelope.common',
 'penelope.corpus',
 'penelope.corpus.dtm',
 'penelope.corpus.readers',
 'penelope.corpus.readers.tng',
 'penelope.corpus.sparv',
 'penelope.ner',
 'penelope.network',
 'penelope.network.graphtool',
 'penelope.network.graphviz',
 'penelope.network.networkx',
 'penelope.notebook',
 'penelope.notebook.cluster_analysis',
 'penelope.notebook.co_occurrence',
 'penelope.notebook.dtm',
 'penelope.notebook.mdw',
 'penelope.notebook.token_counts',
 'penelope.notebook.topic_modelling',
 'penelope.notebook.word_trends',
 'penelope.notebook.word_trends.displayers',
 'penelope.pipeline',
 'penelope.pipeline.spacy',
 'penelope.pipeline.sparv',
 'penelope.plot',
 'penelope.resources',
 'penelope.scripts',
 'penelope.topic_modelling',
 'penelope.topic_modelling.engine_gensim',
 'penelope.topic_modelling.engine_gensim.wrappers',
 'penelope.topic_modelling.engine_textacy',
 'penelope.utility',
 'penelope.vendor',
 'penelope.vendor.gensim',
 'penelope.vendor.nltk',
 'penelope.vendor.spacy',
 'penelope.vendor.stanza',
 'penelope.vendor.textacy',
 'penelope.workflows']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'alive-progress>=1.6.1,<2.0.0',
 'bokeh==2.2.3',
 'click>=7.1.2,<8.0.0',
 'ftfy>=5.8,<6.0',
 'gensim>=3.8.3,<4.0.0',
 'holoviews>=1.13.5,<2.0.0',
 'ipyaggrid==0.2.1',
 'ipycytoscape==1.1.0',
 'ipyfilechooser>=0.4.0,<0.5.0',
 'ipywidgets==7.5.1',
 'jupyter_bokeh==2.0.4',
 'lxml>=4.5.2,<5.0.0',
 'memoization>=0.3.1,<0.4.0',
 'more_itertools>=8.5.0,<9.0.0',
 'nltk>=3.5,<4.0',
 'numpy==1.19.3',
 'openpyxl>=3.0.5,<4.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pydotplus>=2.0.2,<3.0.0',
 'python-louvain>=0.14,<0.15',
 'qgrid>=1.3.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'sklearn',
 'smart_open>=2.2.1,<3.0.0',
 'spacy>=2.3.2,<3.0.0',
 'statsmodels>=0.12.0,<0.13.0',
 'textacy>=0.10.1,<0.11.0',
 'toml>=0.10.2,<0.11.0',
 'wordcloud>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['co_occurrence = penelope.scripts.co_occurrence:main',
                     'compute_topic_model = '
                     'penelope.scripts.compute_topic_model:main',
                     'vectorize_corpus = '
                     'penelope.scripts.vectorize_corpus:main']}

setup_kwargs = {
    'name': 'humlab-penelope',
    'version': '0.3.10',
    'description': 'Utilities that simplify enelpeing in Jupyter Lab',
    'long_description': '# Humlab Penelope\n(p)NL(o)P\n======\n\n[![current release version](https://img.shields.io/github/release/humlab/penelope.svg?style=flat-square)](https://github.com/humlab/penelope/releases)\n[![pypi version](https://img.shields.io/pypi/v/humlab-penelope.svg?style=flat-square)](https://pypi.python.org/pypi/humlab-penelope)\n[![build-status](https://github.com/humlab/penelope/workflows/ci/badge.svg)](https://github.com/humlab/penelope/workflows/ci/badge.svg)\n<!-- [![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.595120-blue.svg)](https://doi.org/10.5281/zenodo.595120) -->\n\n|MIT license|\n\nInstallation\n------------\n\n- Install pre-commit (recommend with pipx)\n- ``make init && make install``\n\nDependencies\n\nUsage\n\nDevelopment\n\nTesting\n\n`make pytest`\n\nVersioning\n\nReferences\n\n- `Humlab-pENELoPE`\n\n<!-- .. |Coverage-Status| image:: https://coveralls.io/repos/tqdm/tqdm/badge.svg?branch=master\n   :target: https://coveralls.io/github/tqdm/tqdm\n.. |CII Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/3264/badge\n   :target: https://bestpractices.coreinfrastructure.org/projects/3264\n.. |GitHub-Status| image:: https://img.shields.io/github/tag/tqdm/tqdm.svg?maxAge=86400&logo=github&logoColor=white\n   :target: https://github.com/tqdm/tqdm/releases\n.. |GitHub-Stars| image:: https://img.shields.io/github/stars/tqdm/tqdm.svg?logo=github&logoColor=white\n   :target: https://github.com/tqdm/tqdm/stargazers\n.. |GitHub-Commits| image:: https://img.shields.io/github/commit-activity/y/tqdm/tqdm.svg?logo=git&logoColor=white\n   :target: https://github.com/tqdm/tqdm/graphs/commit-activity\n.. |GitHub-Issues| image:: https://img.shields.io/github/issues-closed/tqdm/tqdm.svg?logo=github&logoColor=white\n   :target: https://github.com/tqdm/tqdm/issues?q=\n.. |GitHub-PRs| image:: https://img.shields.io/github/issues-pr-closed/tqdm/tqdm.svg?logo=github&logoColor=white\n   :target: https://github.com/tqdm/tqdm/pulls\n.. |GitHub-Contributions| image:: https://img.shields.io/github/contributors/tqdm/tqdm.svg?logo=github&logoColor=white\n   :target: https://github.com/tqdm/tqdm/graphs/contributors\n.. |GitHub-Updated| image:: https://img.shields.io/github/last-commit/tqdm/tqdm/master.svg?logo=github&logoColor=white&label=pushed\n   :target: https://github.com/tqdm/tqdm/pulse\n.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/tqdm.svg?label=pypi%20downloads&logo=PyPI&logoColor=white\n   :target: https://pypi.org/project/tqdm\n.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/tqdm.svg?logo=python&logoColor=white\n   :target: https://pypi.org/project/tqdm\n.. |LICENCE| image:: https://img.shields.io/pypi/l/tqdm.svg\n   :target: https://raw.githubusercontent.com/tqdm/tqdm/master/LICENCE\n.. |DOI| image:: https://img.shields.io/badge/DOI-10.5281/zenodo.595120-blue.svg\n   :target: https://doi.org/10.5281/zenodo.595120\n.. |binder-demo| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/tqdm/tqdm/master?filepath=DEMO.ipynb\n -->\n',
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/humlab/penelope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
