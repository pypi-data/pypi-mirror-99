# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scilib',
 'scilib.antv',
 'scilib.cnki',
 'scilib.db',
 'scilib.gender',
 'scilib.gender.agefromname_pypi',
 'scilib.gender.benchmark',
 'scilib.gender.chinese_naive_bayes',
 'scilib.gender.gender_guesser_pypi',
 'scilib.gender.gender_predictor',
 'scilib.gender.gender_r',
 'scilib.gender.genderizer_pypi',
 'scilib.gender.imdb_wiki_dataset',
 'scilib.iolib',
 'scilib.scripts',
 'scilib.tests',
 'scilib.tests.test_wos',
 'scilib.wos']

package_data = \
{'': ['*'],
 'scilib.tests.test_wos': ['fixtures/*'],
 'scilib.wos': ['configs/*']}

install_requires = \
['agefromname>=0.0.8,<0.0.9',
 'gender-guesser==0.4.0',
 'genderizer>=0.1.2,<0.2.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'naiveBayesClassifier>=0.1.3,<0.2.0',
 'nltk>=3.5,<4.0',
 'numpy>=1.18.2,<2.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'orjson>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pypinyin>=0.38.1,<0.39.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['scilib-gender-benchmark = '
                     'scilib.gender.benchmark.benchmark:run',
                     'scilib-wos-import = scilib.scripts.wos_import:run']}

setup_kwargs = {
    'name': 'scilib',
    'version': '0.0.13',
    'description': 'scilib',
    'long_description': '\n# scilib\n\n[![Github](https://github.com/phyng/scilib/workflows/test/badge.svg)](https://github.com/phyng/scilib/actions) [![Pypi](https://img.shields.io/pypi/v/scilib.svg?style=flat&label=PyPI)](https://pypi.org/project/scilib/)\n\n## documentation\n\nhttps://phyng.com/scilib/\n\n## install\n\n```bash\n# use pip\npip install scilib\n\n# or use poetry\npoetry add scilib\n```\n\n## usage\n\n### import wos data to ElasticSearch\n\n```bash\nenv ES_API=http://localhost:9205 scilib-wos-import --from /path/to/wos_data/ --to es --index wos\n```\n\n## test\n\n```bash\nnpm test\nnpm test_coverage\n```\n',
    'author': 'phyng',
    'author_email': 'phyngk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phyng/scilib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
