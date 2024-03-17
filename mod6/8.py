import re


def my_t9(digits):
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()

    letters = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    pattern = '^' + ''.join(['[' + letters[digit] + ']' for digit in digits]) + '$'
    matching_words = [word for word in words if re.match(pattern, word)]

    return matching_words


digits = '22736368'
matching_words = my_t9(digits)
print(matching_words)
