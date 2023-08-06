# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.series']

package_data = \
{'': ['*'], 'pelican.plugins.series': ['test_data/*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-series',
    'version': '2.0.0',
    'description': 'Series is a Pelican plugin that joins multiple posts into a series',
    'long_description': 'Series: A Plugin for Pelican\n============================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/series/build)](https://github.com/pelican-plugins/series/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-series)](https://pypi.org/project/pelican-series/)\n![License](https://img.shields.io/pypi/l/pelican-series?color=blue)\n\nSeries is a Pelican plugin that joins multiple posts into a series.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-series\n\nUsage\n-----\n\nIn order to mark reStructuredText-formatted posts as part of a series, use the `:series:` metadata:\n\n    :series:  NAME_OF_THIS_SERIES\n\nOr, for Markdown-formatted content:\n\n    Series: NAME_OF_THIS_SERIES\n\nThe plugin collects all articles belonging to the same series and provides series-related variables that you can use in your template.\n\nIndexing\n--------\n\nBy default, articles in a series are ordered by date and then automatically numbered.\n\nIf you want to force a given order, specify the `:series_index:` (reST) or `series_index:` (Markdown) metadata, starting from 1. All articles with this enforced index are put at the beginning of the series and ordered according to the index itself. All the remaining articles come after them, ordered by date.\n\nThe plugin provides the following variables to your templates:\n\n* `article.series.name` is the name of the series as specified in the article metadata\n* `article.series.index` is the index of the current article inside the series\n* `article.series.all` is an ordered list of all articles in the series (including the current one)\n* `article.series.all_previous` is an ordered list of the articles published before the current one\n* `article.series.all_next` is an ordered list of the articles published after the current one\n* `article.series.previous` is the previous article in the series (a shortcut to `article.series.all_previous[-1]`)\n* `article.series.next` is the next article in the series (a shortcut to `article.series.all_next[0]`)\n\nFor example:\n\n```jinja\n{% if article.series %}\n    <p>This post is part {{ article.series.index }} of the "{{ article.series.name }}" series:</p>\n    <ol class="parts">\n        {% for part_article in article.series.all %}\n            <li {% if part_article == article %}class="active"{% endif %}>\n                <a href=\'{{ SITEURL }}/{{ part_article.url }}\'>{{ part_article.title }}</a>\n            </li>\n        {% endfor %}\n    </ol>\n{% endif %}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/series/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL 3.0 license.\n',
    'author': 'Leonardo Giordani',
    'author_email': 'giordani.leonardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/series',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
