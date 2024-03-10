import subprocess
import signal
import os
from flask import Flask


app = Flask(__name__)


def is_port_in_use(port):
    result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
    return bool(result.stdout)


def kill_process_using_port(port):
    result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
    if result.stdout:
        process_info = result.stdout.strip().split('\n')[1]
        process_id = int(process_info.split()[1])
        os.kill(process_id, signal.SIGTERM)
        print(f"Terminated process using port {port}")


@app.route('/testing/')
def testing():
    return 'Server has successfully started'


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        if is_port_in_use(5000):
            kill_process_using_port(5000)
        try:
            app.run(debug=True)
        except Exception:
            print(f'Failed:{e}')