# functionwords


The functionwords package aims at providing **better curated** function words.


For now, it supports four kinds of function words: modern Chinese ([`chinese_simplified_modern`][1]), classical Chinese (in simplified Chinese character, [`chinese_classical_naive`][2] and [`chinese_classical_comprehensive`][3]), and modern English ([`english`][4]).

The `FunctionWords` class does the heavy lifting. Initiate it with the desired function word list `name`. The instance has three methods (.`remove_function_words()`, `count_function_words()`, and `get_function_words()`) and three attributes (`name`, `function_words`, and `description`).


|Name      |# of function words| &nbsp; &nbsp; &nbsp; &nbsp;Description &nbsp; &nbsp; &nbsp; &nbsp;|
|:----:|:----:|:----|
| `chinese_simplified_modern`      |  819 |compiled from the [dictionary][1]     |
| `chinese_classical_naive`        |  32  |harvested from the [platforms][2] |
| `chinese_classical_comprehensive`|  466 |compiled from the [dictionary][3]     |
| `english`                        |  403 |adapted from [software][4]     |

For more details, see FunctionWords instance's attribute `description`.

## Installation

```bash
pip install -U functionwords
```

## Getting started


```python
from functionwords import FunctionWords

raw = "The present King of Singapore is bald."

# to instantiate a FunctionWords instance
# `name` can be either 'chinese_classical_comprehensive', 
# 'chinese_classical_naive', 'chinese_simplified_modern', or 'english'
fw = FunctionWords(name='english')

# to remove function words
fw.remove_function_words(raw)

# to count function words accordingly
# returns a dict
fw.count_function_words(raw)

# to list all function words in 
# returns a list
fw.get_function_words(raw)

```

## Requirements

Only python 3.8+ is required.

## Important links

- Source code: https://github.com/Wang-Haining/functionwords
- Issue tracker: https://github.com/Wang-Haining/functionwords/issues

## License

This package is licensed under the MIT License.

## TO do

- write some tests
- add more function word list

## References
[1]: Ziqiang, W. (1998). Modern Chinese Dictionary of Function Words. Shanghai Dictionary Press.

[2]: https://baike.baidu.com/item/%E6%96%87%E8%A8%80%E8%99%9A%E8%AF%8D and 
https://zh.m.wikibooks.org/zh-hans/%E6%96%87%E8%A8%80/%E8%99%9B%E8%A9%9E

[3]: Hai, W., Changhai, Z., Shan, H., Keying, W. (1996). Classical Chinese Dictionary of Function Words. Peking University Press.

[4]: [Jstylo](https://github.com/psal/jstylo/blob/master/src/main/resources/edu/drexel/psal/resources/functionWord.txt) with minor correction.

