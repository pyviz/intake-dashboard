#!/usr/bin/env python

from jinja2 import Template
from yaml import safe_load

def make_status():

    with open('dashboard.yml') as f:
        config = safe_load(f)

    for section in config:
        for package in section['packages']:
            package['user'], package['name'] = package['repo'].split('/')
            package['badges'] = [x.strip() for x in package['badges'].split(',')]
            package['conda_package'] = package.get('conda_package', package['name'])
            if 'branch' not in package:
                package['branch'] = 'main'  # Assumes 'main' branch is the default
            if 'rtd' in package['badges'] and 'rtd_name' not in package:
                package['rtd_name'] = package['name']
            if 'pypi' in package['badges'] and 'pypi_name' not in package:
                package['pypi_name'] = package['name']
                package['gha'] = True
            if 'circleci' in package['badges'] and 'circleci_project' not in package:
                package['circleci_project'] = package['repo']
            if 'conda' in package['badges'] and 'conda_channel' not in package:
                package['conda_channel'] = 'pyviz'
            if 'site' in package['badges']:
                package['site_protocol'] = package.get('site_protocol', 'http')
                package['site'] = package.get('site', '{}.holoviz.org'.format(package['name']))

    with open('template.html', 'r') as f:
        template = Template(f.read())

    with open('status.html', 'w') as f:
        f.write(template.render(config=config))
