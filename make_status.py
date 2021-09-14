#!/usr/bin/env python

from jinja2 import Template
from yaml import safe_load

with open('dashboard.yml') as f:
    config = safe_load(f)

for section in config:
    for package in section['packages']:
        package['user'], package['name'] = package['repo'].split('/')
        package['badges'] = [x.strip() for x in package['badges'].split(',')]
        package['conda_package'] = package.get('conda_package', package['name'])
        if 'rtd' in package['badges'] and 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'pypi' in package['badges'] and 'pypi_name' not in package:
            package['pypi_name'] = package['name']
        if 'gha' in package['badges']:
            if not all(ppt in package for ppt in ['gha_workflow', 'gha_branch']):
                msg = f'Missing Github Actions workflow file and/or target branch for {package["repo"]}'
                raise ValueError(msg)
            package['gha'] = True
        if 'circleci' in package['badges'] and 'circleci_project' not in package:
            package['circleci_project'] = package['repo']
        if 'conda' in package['badges'] and 'conda_channel' not in package:
            package['conda_channel'] = 'pyviz'
        if 'site' in package['badges']:
            package['site_protocol'] = package.get('site_protocol', 'http')
            package['site'] = package.get('site', '{}.holoviz.org'.format(package['name']))

template = Template(open('template.html', 'r').read())

with open('status.html', 'w') as f:
    f.write(template.render(config=config))
