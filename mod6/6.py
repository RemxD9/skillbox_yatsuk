from flask import Flask, render_template_string
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class EndpointListConverter(BaseConverter):
    def to_python(self, value):
        return app.url_map.converters['default'].to_python(value)

    def to_url(self, value):
        return app.url_map.converters['default'].to_url(value)


app.url_map.converters['endpoint_list'] = EndpointListConverter


def track_endpoints(func):
    app.config.setdefault('TRACK_ENDPOINTS', [])
    app.config['TRACK_ENDPOINTS'].append(func.__name__)
    return func


@app.errorhandler(404)
def page_not_found(error):
    available_endpoints = app.config.get('TRACK_ENDPOINTS', [])
    return render_template_string(
        'The requested URL was not found on the server. Available endpoints: <ul>{% for endpoint in endpoints %}<li><a href="{{ url_for(endpoint) }}">{{ endpoint }}</a></li>{% endfor %}</ul>',
        endpoints=available_endpoints
    ), 404


@app.route('/index')
@track_endpoints
def index():
    return 'Index Page'


@app.route('/about')
@track_endpoints
def about():
    return 'About Page'


if __name__ == '__main__':
    app.run(debug=True)
