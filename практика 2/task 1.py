import os


def get_summary_rss(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]

        total_memory = 0

        for line in lines:
            columns = line.split()
            rss_value = int(columns[5])
            total_memory += rss_value

    def convert_bytes(size):
        power = 2 ** 10
        n = 0
        power_labels = {0: 'Б', 1: 'Кб', 2: 'Мб', 3: 'Гб', 4: "Тб"}
        while size > power:
            size /= power
            n += 1

        return f"{round(size)} {power_labels[n]}"

    readable_memory = convert_bytes(total_memory)
    return readable_memory


if __name__ == '__main__':
    file_path = 'output_file.txt'
    result = get_summary_rss(file_path)
    print(result)
