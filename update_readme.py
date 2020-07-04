#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import collections
import urllib.parse


class InvalidFileFormatException(Exception):
    pass


WordEntry = collections.namedtuple("WordEntry", "word definition examples file_addr")


def load_words():
    words = []

    russian_text_pattern = r"""([\.\,\-\_\'\"\@\?\!\:\;\w\/\\ ]+)"""

    word_pattern = russian_text_pattern
    definition_pattern = russian_text_pattern
    example_pattern = russian_text_pattern

    definition_pattern = re.compile(definition_pattern, re.VERBOSE)

    dir = 'words'
    for basename in os.listdir(dir):
        filename = os.path.join(dir, basename)
        if not os.path.isfile(filename):
            print('Skipping non-file "%s"' % filename)
            continue

        with open(filename) as inp:
            word_line = inp.readline().strip()

            word_match = re.match(word_pattern, word_line)
            if not word_match:
                raise InvalidFileFormatException()
            word = word_match.group(1)

            # skip separator line
            inp.readline()

            definition_line = inp.readline().strip()

            definition_match = re.match(definition_pattern, definition_line)
            if not definition_match:
                raise InvalidFileFormatException()
            definition = definition_match.group(1)

            # skip separator line
            inp.readline()

            examples = []
            for example_line in inp:
                example_match = re.match(example_pattern, example_line)
                if not example_match:
                    raise InvalidFileFormatException

                examples.append(example_match.group(1))

            file_addr = "https://github.com/Azatik1000/russian-it-dict/blob/master/" \
                        + urllib.parse.quote(filename)

            words.append(WordEntry(word=word, definition=definition, examples=examples, file_addr=file_addr))

    words.sort(key=lambda wordEntry: wordEntry.word)
    return words


def write_words(wordEntries, outp):
    for wordEntry in wordEntries:
        examples_str = ""
        for i, example in enumerate(wordEntry.examples):
            examples_str += f"{i + 1}. {example} "

        outp.write(f'| {wordEntry.word} | {wordEntry.definition} | {examples_str} | [Тык]({wordEntry.file_addr}) |\n')


def update_readme(words):
    shutil.copyfile("readme_header.md", "README.md")

    with open('README.md', 'a', encoding='UTF-8') as outp:
        write_words(words, outp)


def main():
    words = load_words()
    update_readme(words)


if __name__ == '__main__':
    main()
