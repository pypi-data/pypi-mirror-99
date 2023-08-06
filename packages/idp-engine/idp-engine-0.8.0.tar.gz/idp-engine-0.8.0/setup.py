# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idp_engine']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'sphinxcontrib-mermaid==0.6.3',
 'textX>=2.1.0,<3.0.0',
 'z3-solver==4.8.8.0']

entry_points = \
{'console_scripts': ['idp-engine = idp_engine.IDP_Z3:cli']}

setup_kwargs = {
    'name': 'idp-engine',
    'version': '0.8.0',
    'description': 'IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the FO(.) language and a Z3 SMT solver.',
    'long_description': 'idp-engine is the core component of IDP-Z3, a software collection implementing the Knowledge Base paradigm using the FO(.) language.\nFO(.) is First Order logic, extended with definitions, types, arithmetic, aggregates and intensional objects.\nThe idp-engine uses the Z3 SMT solver as a back-end.\n\nIt is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).\n\nSee more information at [www.IDP-Z3.be](https://www.IDP-Z3.be).\n\n\n# Installation\n\n``idp_engine`` can be installed from [pypi.org](https://pypi.org/), e.g. using [pip](https://pip.pypa.io/en/stable/user_guide/):\n\n```\n   pip install idp_engine\n```\n\n# Get started\n\nThe following code illustrates how to run inferences on the IDP knowledge.\n\n```\n    from idp_engine import IDP, model_expand\n    kb = IDP.parse("path/to/file.idp")\n    T, S = kb.get_blocks("T, S")\n    for model in model_expand(T,S):\n        print(model)\n```\n\nFor more information, please read [the documentation](http://docs.idp-z3.be/en/latest/).\n\n# Contribute\n\nContributions are welcome!  The repository is [on GitLab](https://gitlab.com/krr/IDP-Z3).',
    'author': 'pierre.carbonnelle',
    'author_email': 'pierre.carbonnelle@cs.kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.idp-z3.be',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
