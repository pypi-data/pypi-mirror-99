# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['timeit2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timeit2',
    'version': '0.1.1',
    'description': 'xtended version of timeit package',
    'long_description': '# timeit2 \n\n\nこのパッケージは処理時間の計測module [timeit](https://docs.python.org/3/library/timeit.html) を使いやすくしたものです。以下の特徴があります。\n\n- 引数を使い回しません(timeitは引数を書き換える処理をした時にそのまま次に渡します)\n- 複数の関数を1度に計測して相対的な速度差を視覚化できます\n- 処理時間の桁数を変えられます(0.00374567より0.0037の方が見やすい)\n- 返り値を一緒にprintできます\n\n![test](https://github.com/atu4403/timeit2/workflows/test/badge.svg)\n\n\n## Install\n\n```\n$ pip install timeit2\n```\n\n\n## Example\n\n```python\nfrom timeit2 import ti2\n\narg = range(10 ** 6)\nti2(\n    max,\n    sum,\n    args=[arg],\n    floor=4,\n    print_return=True,\n    return_label="ret: ",\n    relative=True,\n)\n# max:\n#         0.0356 sec\n#         ret: 999999\n# sum:\n#         0.0249 sec\n#         ret: 499999500000\n# relative:\n#         sum:\n#                 1\n#         max:\n#                 1.43\n```\n\n最小限の使い方\n\n```python\nfrom timeit2 import ti2\n\ndef f():\n    li = []\n    for i in range(10 ** 5):\n        li.append(i * i)\n    return li\n\nti2(f)\n\n# f:\n#         0.015094 sec\n```\n\n配列作成に`list.append`,`list.insert`,`deque`をそれぞれ使った処理時間と相対評価\n\n```python\nfrom collections import deque\nfrom timeit2 import ti2\n\n\ndef append_(n):\n    li = []\n    for i in range(n):\n        li.append(i)\n    return li\n\n\ndef insert_(n):\n    li = []\n    for i in range(n):\n        li.insert(0, i)\n    return li\n\n\ndef deque_right(n):\n    li = deque()\n    for i in range(n):\n        li.append(i)\n    return li\n\n\ndef deque_left(n):\n    li = deque()\n    for i in range(n):\n        li.appendleft(i)\n    return li\n\n\nti2(\n    append_,\n    insert_,\n    deque_right,\n    deque_left,\n    args=[10 ** 4],\n    relative=True,\n)\n\n# append_:\n#         0.001118 sec\n# insert_:\n#         0.021187 sec\n# deque_right:\n#         0.000891 sec\n# deque_left:\n#         0.000855 sec\n# relative:\n#         deque_left:\n#                 1\n#         deque_right:\n#                 1.04\n#         append_:\n#                 1.31\n#         insert_:\n#                 24.77\n```\n\n## API\n\n```python\nti2(\n    *fn: Callable,\n    args: list = [],\n    number: int = 100,\n    floor: int = 6,\n    relative: bool = False,\n    print_return: bool = False,\n    return_label: str = "",\n)\n```\n\n### argument\n\n#### fn\n\nType: Callable\n\n計測する関数、可変長引数なので複数指定が可能。\n引数がある場合は`args=` で指定する。\n\n### Options\n\n#### args \n\nType: list\n\nDefault: []\n\nfnに渡す引数のlist\n\n#### number \n\nType: int\n\nDefault: 100\n\n各関数を計測する回数、結果はその最速値が表示される\n\n\n#### floor\n\nType: int\n\nDefault: 6\n\n表示する小数点以下の桁数\n\n\n#### relative\n\nType: bool\n\nDefault: False\n\n計測結果に相対評価を追加する\n\n#### print_return\n\nType: bool\n\nDefault: False\n\n計測結果に関数の返り値を追加する\n\n#### return_label\n\nType: str\nDefault: ""\n\n`print_return=True`の場合、返り値のラベルを指定する\n\n\n## alias\n\nti2, ti, timeit, timeit2 をimportできますが、全て同じものです。\n\n\n```python\nfrom timeit2 import ti2, ti, timeit, timeit2\n```\n\n## Related\n- [timeit](https://docs.python.org/3/library/timeit.html)\n\n\n## License\n\nMIT © 2021 [atu4403](https://github.com/atu4403)\n',
    'author': 'atu4403',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atu4403',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
