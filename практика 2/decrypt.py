import sys


def decrypter(text):
    decrypted_message = ''
    i = 0
    while i < len(text):
        if text[i].isalpha() or text[i] == '-':
            decrypted_message += text[i]
            i += 1
        elif text[i] == '.':
            if i + 1 < len(text) and text[i + 1] == '.':
                decrypted_message = decrypted_message[:-1]
                i += 2
            else:
                i += 1
        elif text[i] == ' ':
            decrypted_message += ' '
            i += 1
        else:
            i += 1

    return decrypted_message


if __name__ == '__main__':
    text = sys.stdin.read().strip()
    result = decrypter(text)
    print(result)
