# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sogou_tr']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0',
 'httpx>=0.17.1,<0.18.0',
 'langid>=1.1.6,<2.0.0',
 'logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'sogou-tr',
    'version': '0.1.1',
    'description': 'sogou translate no frills',
    'long_description': '# sogou-tr\n<!--- sogou-tr-simple  sogou_tr  sogou_tr sogou_tr --->\n[![tests](https://github.com/ffreemt/sogou-tr-simple/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sogou_tr.svg)](https://badge.fury.io/py/sogou_tr)\n\nsogou translate no frills\n\n## Installation\n\n```bash\npip install sogou-tr\n```\n\n## Usage\n\n```python\nfrom sogou_tr.sogou_tr import sogou_tr\n\ntext = "An employee at Spataro\'s No Frills, located at 8990 Chinguacousy Rd, has tested positive for the virus."\nprint(text, "\\n")\nprint("to zh:", sogou_tr(text), "\\n")\nprint("to de:", sogou_tr(text, to_lang="de"), "\\n")\n\n# to zh: 位于金瓜库西路8990号的斯帕塔罗百货公司的一名员工检测出病毒呈阳性。\n# to de: Ein Mitarbeiter von Spataro es No Frills, gelegen 8990 Chinguacousy Rd, hat positiv auf das Virus getestet.\n```\n\nConsult sogou fanyi\'s homepage for language pairs supported.\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/sogou-tr-simple',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
