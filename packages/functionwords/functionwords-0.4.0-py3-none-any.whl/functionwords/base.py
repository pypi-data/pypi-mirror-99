"""
@author: Haining Wang {whn395436129@gmail.com}
Created on March 17, 2021.
"""

import re
import os
import json


class FunctionWords(object):
    """
    The main class does the heavy lifting.

    Attr:
        name: Which function word list is called. Either 'chinese_classical_comprehensive', 'chinese_classical_naive',
         'chinese_simplified_modern', or 'english'.
        function_words: The corresponding function word list.
        description: The description of the function word list.
    """

    def __init__(self, name):
        self.__path__ = os.path.dirname(__file__)
        NAMES = json.load(open(os.path.join(self.__path__, 'resources', 'names.json'), 'r'))
        if name.lower() in NAMES:
            self.name = name.lower()
        else:
            raise ValueError(
                f"""Pass in desired function word list in {NAMES}."""
            )
        self.function_words = json.load(open(os.path.join(self.__path__, 'resources', self.name + '.json'), 'r'))
        self.description = json.load(open(os.path.join(self.__path__, 'resources', 'description.json'), 'r'))[self.name]

    def remove_function_words(self, raw):
        """
        Removes all function words in a text.
        param:
            raw: A string.
        return:
            A string without function words.
        """
        if not isinstance(raw, str):
            raise ValueError(
                f"""List of raw text documents expected, {type(raw)} object received."""
            )
        remove = "|".join(self.function_words)
        pattern = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)

        return re.sub(pattern=pattern, string=raw, repl='')

    def get_function_words(self):
        """
        Returns a list of desired function words.
        """

        return self.function_words

    def count_function_words(self, raw):
        """
        Counts function words in the `raw`.
        param:
            raw: A string.
        return:
            A dict keyed by a function word, valued the corresponding count.
        """
        if not isinstance(raw, str):
            raise ValueError(
                f"""List of raw text documents expected, {type(raw)} object received."""
            )
        counts_ = [len(re.findall(r"\b" + function_word + r"\b", raw.lower()))
                           for function_word in self.function_words]

        return dict(zip(self.function_words, counts_))
