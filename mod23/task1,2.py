import json
from wsgiref.simple_server import make_server


class WSGIApp:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        handler, params = self.match_route(path)

        if handler:
            response, content_type = handler(**params)
            status = '200 OK'
        else:
            response = json.dumps({"error": "Not Found"}, indent=4)
            content_type = 'application/json'
            status = '404 Not Found'

        headers = [('Content-Type', content_type)]
        start_response(status, headers)
        return [response.encode('utf-8')]

    def match_route(self, path):
        for route, handler in self.routes.items():
            if '<' in route and '>' in route:
                param_name = route.split('<')[1].split('>')[0]
                base_route = route.split('<')[0]
                if path.startswith(base_route):
                    param_value = path[len(base_route):]
                    return handler, {param_name: param_value}
            elif path == route:
                return handler, {}
        return None, {}


app = WSGIApp()

route = app.route


@route("/hello")
def say_hello():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, world!</h1>
        <img src="/static/image1.png" alt="Image 1">
    </body>
    </html>
    """
    return html_content, 'text/html'


@route("/hello/<name>")
def say_hello_with_name(name):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello {name}</title>
    </head>
    <body>
        <h1>Hello, {name}!</h1>
        <img src="/static/image2.png" alt="Image 2">
        <img src="/static/image3.png" alt="Image 3">
    </body>
    </html>
    """
    return html_content, 'text/html'


if __name__ == '__main__':
    httpd = make_server('', 5000, app)
    print("Serving on port 8000...")
    httpd.serve_forever()
