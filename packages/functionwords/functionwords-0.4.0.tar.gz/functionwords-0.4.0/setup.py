# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functionwords']

package_data = \
{'': ['*'],
 'functionwords': ['resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_comprehensive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_classical_naive.json',
                   'resources/chinese_modern.json',
                   'resources/chinese_modern.json',
                   'resources/chinese_modern.json',
                   'resources/chinese_modern.json',
                   'resources/chinese_modern.json',
                   'resources/chinese_modern.json',
                   'resources/description.json',
                   'resources/description.json',
                   'resources/description.json',
                   'resources/description.json',
                   'resources/description.json',
                   'resources/description.json',
                   'resources/english.json',
                   'resources/english.json',
                   'resources/english.json',
                   'resources/english.json',
                   'resources/english.json',
                   'resources/english.json',
                   'resources/names.json',
                   'resources/names.json',
                   'resources/names.json',
                   'resources/names.json',
                   'resources/names.json',
                   'resources/names.json']}

setup_kwargs = {
    'name': 'functionwords',
    'version': '0.4.0',
    'description': 'Better curated Chinese and English function words.',
    'long_description': '# functionwords\n\n\nThe functionwords package aims at providing **better curated** function words.\n\n\nFor now, it supports four kinds of function words: modern Chinese ([`chinese_simplified_modern`][1]), classical Chinese (in simplified Chinese character, [`chinese_classical_naive`][2] and [`chinese_classical_comprehensive`][3]), and modern English ([`english`][4]).\n\nThe `FunctionWords` class does the heavy lifting. Initiate it with the desired function word list `name`. The instance has three methods (.`remove_function_words()`, `count_function_words()`, and `get_function_words()`) and three attributes (`name`, `function_words`, and `description`).\n\n\n|Name      |# of function words| &nbsp; &nbsp; &nbsp; &nbsp;Description &nbsp; &nbsp; &nbsp; &nbsp;|\n|:----:|:----:|:----|\n| `chinese_simplified_modern`      |  819 |compiled from the [dictionary][1]     |\n| `chinese_classical_naive`        |  32  |harvested from the [platforms][2] |\n| `chinese_classical_comprehensive`|  466 |compiled from the [dictionary][3]     |\n| `english`                        |  403 |adapted from [software][4]     |\n\nFor more details, see FunctionWords instance\'s attribute `description`.\n\n## Installation\n\n```bash\npip install -U functionwords\n```\n\n## Getting started\n\n\n```python\nfrom functionwords import FunctionWords\n\nraw = "The present King of Singapore is bald."\n\n# to instantiate a FunctionWords instance\n# `name` can be either \'chinese_classical_comprehensive\', \n# \'chinese_classical_naive\', \'chinese_simplified_modern\', or \'english\'\nfw = FunctionWords(name=\'english\')\n\n# to remove function words\nfw.remove_function_words(raw)\n\n# to count function words accordingly\n# returns a dict\nfw.count_function_words(raw)\n\n# to list all function words in \n# returns a list\nfw.get_function_words(raw)\n\n```\n\n## Requirements\n\nOnly python 3.8+ is required.\n\n## Important links\n\n- Source code: https://github.com/Wang-Haining/functionwords\n- Issue tracker: https://github.com/Wang-Haining/functionwords/issues\n\n## License\n\nThis package is licensed under the MIT License.\n\n## TO do\n\n- write some tests\n- add more function word list\n\n## References\n[1]: Ziqiang, W. (1998). Modern Chinese Dictionary of Function Words. Shanghai Dictionary Press.\n\n[2]: https://baike.baidu.com/item/%E6%96%87%E8%A8%80%E8%99%9A%E8%AF%8D and \nhttps://zh.m.wikibooks.org/zh-hans/%E6%96%87%E8%A8%80/%E8%99%9B%E8%A9%9E\n\n[3]: Hai, W., Changhai, Z., Shan, H., Keying, W. (1996). Classical Chinese Dictionary of Function Words. Peking University Press.\n\n[4]: [Jstylo](https://github.com/psal/jstylo/blob/master/src/main/resources/edu/drexel/psal/resources/functionWord.txt) with minor correction.\n\n',
    'author': 'Haining Wang',
    'author_email': 'hw56@indiana.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Wang-Haining/functionwords',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
