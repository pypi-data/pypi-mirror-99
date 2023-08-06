# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.share_post']

package_data = \
{'': ['*'], 'pelican.plugins.share_post': ['test_data/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-share-post',
    'version': '1.0.0',
    'description': 'A Pelican plugin to create share URLs of article',
    'long_description': '# Share Post: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/share-post/build)](https://github.com/pelican-plugins/share-post/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-share-post)](https://pypi.org/project/pelican-share-post/)\n![License](https://img.shields.io/pypi/l/pelican-share-post?color=blue)\n\nShare Post is a Pelican plugin that creates share links in articles that allow site visitors to share the current article with others in a privacy-friendly manner.\n\nMany web sites have share widgets to let readers share posts on social networks. Most of these widgets are used by vendors for online tracking. These widgets can also be visually-distracting and negatively affect readers’ attention.\n\nShare Post creates old-school URLs for some popular sites which your theme can use. These links do not have the ability to track site visitors. They can also be unobtrusive depending on how Pelican theme uses them.\n\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-share-post\n\nUsage\n-----\n\nThis plugin adds to each Pelican article a dictionary of URLs that, when followed, allows the reader to easily share the article via specific channels. When activated, the plugin adds the attribute `share_post` to each article with the following format:\n\n``` python\narticle.share_post = {\n\t"facebook": "<URL>",\n\t"email": "<URL>",\n\t"twitter": "<URL>",\n\t"diaspora": "<URL>",\n\t"linkedin": "<URL>",\n\t"hacker-news": "<URL>",\n\t"reddit": "<URL>",\n}\n```\n\nYou can then access those variables in your template. For example:\n\n``` html+jinja\n{% if article.share_post and article.status != \'draft\' %}\n<section>\n  <p id="post-share-links">\n    Share on:\n    <a href="{{article.share_post[\'diaspora\']}}" title="Share on Diaspora">Diaspora*</a>\n    ❄\n    <a href="{{article.share_post[\'twitter\']}}" title="Share on Twitter">Twitter</a>\n    ❄\n    <a href="{{article.share_post[\'facebook\']}}" title="Share on Facebook">Facebook</a>\n    ❄\n    <a href="{{article.share_post[\'linkedin\']}}" title="Share on LinkedIn">LinkedIn</a>\n    ❄\n    <a href="{{article.share_post[\'hacker-news\']}}" title="Share on HackerNews">HackerNews</a>\n    ❄\n    <a href="{{article.share_post[\'email\']}}" title="Share via Email">Email</a>\n    ❄\n    <a href="{{article.share_post[\'reddit\']}}" title="Share via Reddit">Reddit</a>\n  </p>\n</section>\n{% endif %}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/share-post/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n\nContributors\n------------\n\n* [Talha Mansoor](https://www.oncrashreboot.com) - talha131@gmail.com\n* [Jonathan DEKHTIAR](https://github.com/DEKHTIARJonathan) - contact@jonathandekhtiar.eu\n* [Justin Mayer](https://justinmayer.com)\n* [Leonardo Giordani](https://www.thedigitalcatonline.com)\n\n\nLicense\n-------\n\nThis project is licensed under the MIT license.\n',
    'author': 'Talha Mansoor',
    'author_email': 'talha131@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/share-post',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
