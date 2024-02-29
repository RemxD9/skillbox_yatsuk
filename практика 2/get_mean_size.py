import sys


def get_mean_size(data):
    lines = data.split('\n')[1:]

    total_size = 0
    file_count = 0

    for line in lines:
        columns = line.split()

        if len(columns) >= 5:
            size = int(columns[4])
            total_size += size
            file_count += 1

    if file_count > 0:
        mean_size = total_size / file_count
        return f"{mean_size:.2f} bytes"
    else:
        return 'Пустая директория или неудалось получить доступ'


if __name__ == '__main__':
    data = sys.stdin.read()
    result = get_mean_size(data)
    print(result)
