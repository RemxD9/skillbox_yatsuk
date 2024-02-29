import os
from flask import Flask

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size, relative_path):
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(current_directory, relative_path)

        abs_path = os.path.normpath(abs_path)

        with open(abs_path, 'r', encoding='utf-8') as file:
            content = file.read(size)

        result_size = len(content)
        result_text = content.replace('\n', '<br>')

        return f'{abs_path} {result_size}<br>{result_text}'

    except FileNotFoundError as e:
        return f"File not found: {abs_path}", 404
    except IOError as e:
        return f"IOError: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
