import re


def is_strong_password(password, english_words):
    password_words = re.findall(r'\b\w+\b', password.lower())
    for word in password_words:
        if word in english_words:
            return False
    return True


if __name__ == '__main__':
    with open('words.txt', 'r', encoding='utf-8') as file:
        words = set(word.strip().lower() for word in file if len(word.strip()) > 4)

    password = input()
    result = is_strong_password(password, words)
    print(result)
