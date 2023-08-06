import os
import decimal

from flask import (
    abort,
    Blueprint,
    json,
    render_template,
    request,
    send_from_directory,
    render_template_string
)

from .form import create_nexus_form_cls
from .utils import (
    DecimalEncoder,
    get_asset_url,
    get_nexus_apps,
    load_json,
    render_nexus,
    render_form,
    PROJECTS_DIR
)

nexus_dev_pages = Blueprint(
    'nexus_dev_pages',
    __name__,
    static_folder=None,
    template_folder=None
)

@nexus_dev_pages.route(f'/{PROJECTS_DIR}/<appname>/assets/<path:filename>')
def asset_file(appname, filename):
    return send_from_directory(f'{PROJECTS_DIR}/{appname}/assets/', filename)

@nexus_dev_pages.route('/')
def dev_home():
    nexus_apps = get_nexus_apps()
    template = ''
    for nexus in nexus_apps:
        template += f'<a href="/{nexus}/">{nexus}</a><br />'
    return render_template_string(template, **{})

@nexus_dev_pages.route('/<nexus_name>/')
def nexus_home(nexus_name):
    html = render_nexus(nexus_name, **{'section': 'render'})
    return html if html else render_template_string('Error', **{})

@nexus_dev_pages.route('/<nexus_name>/form/', methods = ['POST', 'GET'])
def nexus_form(nexus_name):
    schema = load_json(f'apps/{nexus_name}/', 'form.json')
    form_cls = create_nexus_form_cls(schema)
    if request.method == 'POST':
        nexus_form = form_cls(request.form)
        if nexus_form.validate():
            try:
                with open(f'cache/{nexus_name}.json', 'w') as f:
                    json.dump(nexus_form.data, f, cls=DecimalEncoder)
            except Exception as e:
                print(e)
        form = nexus_form
    else:
        data = load_json('cache', f'{nexus_name}.json')
        #create_fields_dict()
        form = form_cls(**data)

    extra_kwargs = {
        'section': 'form',
        'form_html': render_form(nexus_name, **{'form': form})
    }
    html = render_nexus(nexus_name, **extra_kwargs)
    return html if html else abort(404)
