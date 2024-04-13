import subprocess


def process_count(username: str) -> int:
    command = f"ps -u {username} -o pid="
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return len(result.stdout.splitlines())


def total_memory_usage(root_pid: int) -> float:
    command = f"ps -o pid= --ppid {root_pid}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    child_pids = [int(pid) for pid in result.stdout.splitlines()]

    memory_usage = 0.0
    for pid in child_pids:
        command = f"ps -o %mem= -p {pid}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        memory_usage += float(result.stdout.strip())

    return memory_usage


username = "username"
print("Количество процессов:", process_count(username))

root_pid = 12345
print("Суммарное потребление памяти:", total_memory_usage(root_pid), "%")
