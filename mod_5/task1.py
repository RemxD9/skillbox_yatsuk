import os
import subprocess
import signal
from flask import Flask, request


app = Flask(__name__)


def port_is_in_use(port):
    result = subprocess.run(['isof', '-i', f':{port}'], capture_output=True, text=True)
    return True if result.stdout else False


def start_server():
    port_number = 5000
    app.run(debug=True, port=port_number)
    if port_is_in_use(port_number):
        terminating_process(port_number)
    else:
        app.run(debug=True, port=port_number)
        terminating_process(port_number)
    try:
        app.run(debug=True, port=port_number)
        print('Success!')
        return
    except Exception as e:
        print(f'{e}')
        return


def terminating_process(port_number):
    cmd = subprocess.run(['isof', '-i', f':{port_number}'], capture_output=True, text=True)
    process_info = cmd.stdout.strip().split('\n')[1]
    process_id = int(process_info.split()[1])
    os.kill(process_id, signal.SIGTERM)
    return


@app.route('/testing/')
def testing_server():
    print(f'Server started on {request.host}')


if __name__ == '__main__':
    start_server()
