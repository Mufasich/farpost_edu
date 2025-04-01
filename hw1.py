"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List
import string


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    for punct in string.punctuation:
        text = text.replace(punct, ' ')
    words = text.split()

    def sort_key(word):
        return (-len(word), -len(set(word)))

    sorted_words = sorted(words, key=sort_key)

    result = []
    seen = set()
    for word in sorted_words:
        if word not in seen:
            seen.add(word)
            result.append(word)
            if len(result) == 10:
                break
    return result


def get_rarest_char(file_path: str) -> str:
    char_count = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char in char_count:
                    char_count[char] += 1
                else:
                    char_count[char] = 1

    if not char_count:
        return ''

    rarest_char = None
    min_count = float('inf')
    for char, count in char_count.items():
        if count < min_count:
            min_count = count
            rarest_char = char
    return rarest_char


def count_punctuation_chars(file_path: str) -> int:
    count = 0
    punct_set = set(string.punctuation)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char in punct_set:
                    count += 1
    return count


def count_non_ascii_chars(file_path: str) -> int:
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if ord(char) > 127:
                    count += 1
    return count


def get_most_common_non_ascii_char(file_path: str) -> str:
    non_ascii_counts = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if ord(char) > 127:
                    if char in non_ascii_counts:
                        non_ascii_counts[char] += 1
                    else:
                        non_ascii_counts[char] = 1

    if not non_ascii_counts:
        return ''
    most_common = None
    max_count = 0
    for char, count in non_ascii_counts.items():
        if count > max_count:
            max_count = count
            most_common = char
    return most_common







print(get_longest_diverse_words("data.txt"))
print(get_rarest_char("data.txt"))
print(count_punctuation_chars("data.txt"))
print(count_non_ascii_chars("data.txt"))
print(get_most_common_non_ascii_char("data.txt"))