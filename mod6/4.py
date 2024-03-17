import json
from collections import Counter
from datetime import datetime


with open('skillbox_json_messages.log', 'r') as file:
    logs = []
    for line in file:
        decoded_line = json.loads(line.strip())
        logs.append(decoded_line)

level_count = Counter(log['level'] for log in logs)

hour_counts = Counter(datetime.strptime(log['time'], '%H:%M:%S').hour for log in logs)
most_common_hour = max(hour_counts, key=hour_counts.get)

start_time = datetime.strptime('05:00:00', '%H:%M:%S')
end_time = datetime.strptime('05:20:00', '%H:%M:%S')
critical_logs_in_interval = [log for log in logs if log['level'] == 'CRITICAL' and
                             start_time <= datetime.strptime(log['time'], '%H:%M:%S') <= end_time]

dog_message_count = sum('dog' in log['message'] for log in logs)

warning_messages = [log['message'] for log in logs if log['level'] == 'WARNING']
word_counts = Counter(word for message in warning_messages for word in message.split())
if not word_counts:
    most_common_word = "Нет сообщений уровня WARNING"
else:
    most_common_word = max(word_counts, key=word_counts.get)
    if most_common_word.startswith('"'):
        most_common_word = most_common_word[1:]
    if most_common_word.endswith('"'):
        most_common_word = most_common_word[:-1]

print("Количество сообщений каждого уровня за сутки:", level_count)
print("В какой час было больше всего логов:", most_common_hour)
print("Количество логов уровня CRITICAL в период с 05:00:00 по 05:20:00:", len(critical_logs_in_interval))
print("Количество сообщений, содержащих слово 'dog':", dog_message_count)
print("Слово, которое чаще всего встречается в сообщениях уровня WARNING:", most_common_word)

