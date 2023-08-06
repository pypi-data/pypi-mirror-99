from flask import Flask, render_template
import os
import json
import subprocess

current_directory = os.path.dirname(os.path.abspath(__file__))
templates_directory = os.path.join(current_directory, 'templates')
commands_config_directory = os.path.join(current_directory, 'config.json')

app = Flask(__name__, template_folder=templates_directory)


with open(commands_config_directory) as f:
    routes_config = json.load(f)


def validate_route(route):
    if 'title' not in route:
        raise RuntimeError('Route title is missing!')
    if 'commands' not in route:
        raise RuntimeError('Commands is missing!')
    if 'route_url' not in route:
        raise RuntimeError('Route URL is missing!')
    if not isinstance(route['commands'], list):
        raise RuntimeError('Commands should be list!')
    for command in route['commands']:
        if 'title' not in command:
            raise RuntimeError('Command title is missing!')
        if 'command' not in command:
            raise RuntimeError('Command is missing!')
        if not isinstance(command['command'], list):
            raise RuntimeError('Command should be list!')
    return route


if 'routes' in routes_config:
    if isinstance(routes_config['routes'], list):
        for i, route in enumerate(routes_config['routes']):
            route = validate_route(route)

            @app.route(route['route_url'])
            def __route_func():
                results = []
                for command in route['commands']:
                    command_result = subprocess.check_output(command['command']).decode('utf-8')
                    results.append({
                        'title': command['title'],
                        'result': command_result
                    })
                return render_template(
                    'index.html',
                    title=route['title'],
                    results=results
                )

            __route_func.__name__ = f'{__route_func.__name__}__{i}'


if __name__ == '__main__':
    app.run('0.0.0.0', '8118')
