from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import InputRequired, NumberRange
from subprocess import Popen, PIPE, TimeoutExpired
import shlex


app = Flask(__name__)


class CodeExecutionForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=1, max=30)])


@app.route('/execute_code', methods=['POST'])
def execute_code():
    form = CodeExecutionForm()

    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data

        try:
            result = run_python_code(code, timeout)
            return jsonify({'result': result})
        except TimeoutExpired:
            return jsonify({'error': 'Execution timed out'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid input'}), 400


def run_python_code(code, timeout):
    cmd = ['prlimit', '--nproc=1:1', 'python', '-c', f"{shlex.quote(code)}"]

    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            error_message = stderr.decode('utf-8').strip()
            raise RuntimeError(f'Execution failed with error: {error_message}')
    except TimeoutExpired:
        process.kill()
        raise


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
