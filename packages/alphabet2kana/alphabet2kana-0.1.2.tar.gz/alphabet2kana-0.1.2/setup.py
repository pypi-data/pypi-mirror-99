# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alphabet2kana']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alphabet2kana',
    'version': '0.1.2',
    'description': 'Convert English alphabet to Katakana',
    'long_description': '# alphabet2kana\n\nConvert English alphabet to Katakana\n\nアルファベットの日本語表記は [Unidic](https://unidic.ninjal.ac.jp/) \nと [英語アルファベット - Wikipedia](https://ja.wikipedia.org/wiki/%E8%8B%B1%E8%AA%9E%E3%82%A2%E3%83%AB%E3%83%95%E3%82%A1%E3%83%99%E3%83%83%E3%83%88) を参考にしています。\n\n特に、`Z` は `ゼット` 表記です。\n\n## Usage\n\n```python\nfrom alphabet2kana import a2k\n\na2k(\'ABC\')\n# \'エービーシー\'\n\na2k(\'Alphabetと日本語\')\n# \'エーエルピーエイチエービーイーティーと日本語\'\n\na2k(\'Alphabetと日本語\', delimiter="・")\n# \'エー・エル・ピー・エイチ・エー・ビー・イー・ティーと日本語\'\n``` \n\n半角にのみ対応しています。\n全角アルファベットは [mojimoji](https://github.com/studio-ousia/mojimoji) や [jaconv](https://github.com/ikegami-yukino/jaconv) \nなどで半角に変換してください。\n\nOnly supported with half-width characters.',
    'author': 'shihono',
    'author_email': '26952997+shihono@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shihono/alphabet2kana',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
