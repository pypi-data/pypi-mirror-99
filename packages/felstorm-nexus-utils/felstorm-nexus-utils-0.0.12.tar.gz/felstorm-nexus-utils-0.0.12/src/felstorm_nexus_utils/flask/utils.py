import os
import sys
import glob, os.path
import decimal
import jinja2
import pkgutil

from datetime import datetime
from flask import current_app, json
from jinja2 import (
    meta,
    ChoiceLoader,
    FunctionLoader,
    FileSystemLoader,
    ModuleLoader,
    PackageLoader
)
from jinja2.sandbox import SandboxedEnvironment


PROJECTS_DIR = 'projects'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def get_asset_url(nexus_name, filename):
    now = datetime.now()
    ts = datetime.timestamp(now)
    return f'/{PROJECTS_DIR}/{nexus_name}/assets/{filename}?ts={ts}'

def get_nexus_projects():
    return next(os.walk(f'{PROJECTS_DIR}/'))[1]

def load_json(path, file_name):
    form_url = os.path.join(current_app.root_path, path, file_name)
    try:
        data = json.load(open(form_url))
        return data
    except Exception as e:
        print(e)
        return {}


def get_nexus_data(nexus_name):
    cache_json = load_json('', f'cache.json')
    return cache_json.get(nexus_name, {})


def store_nexus_data(nexus_name, data):
    cache_json = load_json('', 'cache.json')
    cache_json[nexus_name] = data
    try:
        with open(f'cache.json', 'w') as f:
            json.dump(cache_json, f, cls=DecimalEncoder)
    except Exception as e:
        print(e)


def get_render_form_kwargs(nexus_name):
    return {
        'asset_url': get_asset_url,
        'config': load_json(f'{PROJECTS_DIR}/{nexus_name}/', 'config.json'),
        'nexus': nexus_name
    }


def get_render_nexus_kwargs(nexus_name):
    return {
        'asset_url': lambda fn: get_asset_url(nexus_name, fn),
        'config': load_json(f'{PROJECTS_DIR}/{nexus_name}/', 'config.json'),
        'form_schema': load_json(f'{PROJECTS_DIR}/{nexus_name}/', 'form.json'),
        'data': get_nexus_data(nexus_name),
        'nexus': nexus_name
    }


def render_form(nexus_name, **kwargs):
    app_loader = ChoiceLoader([
        FileSystemLoader([f'{PROJECTS_DIR}/{nexus_name}/templates']),
        PackageLoader('felstorm_nexus_utils.flask', 'templates')
    ])
    env = SandboxedEnvironment(
        loader=app_loader,
        autoescape=True
    )
    template = env.get_template('form_master.html')
    template_kwargs = {**kwargs, **get_render_form_kwargs(nexus_name)}
    return template.render(**template_kwargs)


def render_nexus(nexus_name, **kwargs):
    app_loader = ChoiceLoader([
        PackageLoader('felstorm_nexus_utils.flask', 'templates'),
        FileSystemLoader([f'{PROJECTS_DIR}/{nexus_name}/templates'])
    ])
    env = SandboxedEnvironment(
        loader=app_loader,
        autoescape=True
    )
    template = env.get_template('index_master.html')
    template_kwargs = {**kwargs, **get_render_nexus_kwargs(nexus_name)}
    return template.render(**template_kwargs)
