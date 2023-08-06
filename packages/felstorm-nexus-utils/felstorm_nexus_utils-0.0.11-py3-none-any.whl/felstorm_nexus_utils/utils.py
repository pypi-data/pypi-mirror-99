import os
import sys
import glob, os.path
import decimal
import jinja2
import pkgutil

from flask import current_app
from datetime import datetime
from jinja2 import (
    meta,
    ChoiceLoader,
    FunctionLoader,
    FileSystemLoader,
    ModuleLoader,
    PackageLoader
)
from jinja2.sandbox import SandboxedEnvironment
from flask import json

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

def get_nexus_apps():
    return next(os.walk(f'{PROJECTS_DIR}/'))[1]

def load_json(path, file_name):
    form_url = os.path.join(current_app.root_path, path, file_name)
    try:
        data = json.load(open(form_url))
        return data
    except Exception as e:
        print(e)
        return {}

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
        'form': {
            'fields': load_json(f'{PROJECTS_DIR}/{nexus_name}/', 'form.json'),
            'data': load_json('cache/', f'{nexus_name}.json'),
        },
        'nexus': nexus_name
    }


def render_form(nexus_name, **kwargs):
    app_loader = ChoiceLoader([
        FileSystemLoader([f'{PROJECTS_DIR}/{nexus_name}/templates']),
        PackageLoader('felstorm_nexus_utils', 'templates')
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
        PackageLoader('felstorm_nexus_utils', 'templates'),
        FileSystemLoader([f'{PROJECTS_DIR}/{nexus_name}/templates'])
    ])
    env = SandboxedEnvironment(
        loader=app_loader,
        autoescape=True
    )
    template = env.get_template('index_master.html')
    template_kwargs = {**kwargs, **get_render_nexus_kwargs(nexus_name)}
    return template.render(**template_kwargs)
