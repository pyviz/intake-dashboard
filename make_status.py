#!/usr/bin/env python

import sys
from jinja2 import Template
from yaml import load
import requests

with open('dashboard.yml') as f:
    config = load(f)

existing = {package['repo'].split('/')[1].lower(): package for section in config for package in section['packages']}

# Also get affiliated packages
registry = requests.get('http://www.astropy.org/affiliated/registry.json').json()['packages']
for section in config:
    if section['name'] == 'Affiliated Packages':
        affiliated = section
        break
else:
    print("Could not find affiliated package section in dashboard.yml")
    sys.exit(1)

for package in registry:
    if package['name'].lower() in existing:
        entry = existing[package['name'].lower()]
    else:
        entry = {}
    if 'repo' not in entry:
        if 'github.com' in package['repo_url']:
            entry['repo'] = package['repo_url'].split('github.com/')[1]
        else:
            print("Skipping package {0} which is not on GitHub".format(package['name']))
    if 'pypi_name' not in entry:
        entry['pypi_name'] = package['pypi_name']
    if 'badges' not in entry:
        entry['badges'] = 'travis, coveralls, rtd, pypi'
    if package['name'].lower() not in existing:
        affiliated['packages'].append(entry)

for section in config:
    for package in section['packages']:
        package['user'], package['name'] = package['repo'].split('/')
        package['badges'] = [x.strip() for x in package['badges'].split(',')]
        if 'rtd_name' not in package:
            package['rtd_name'] = package['name']
        if 'pypi_name' not in package:
            package['pypi_name'] = package['name']
        if 'appveyor' in package['badges'] and 'appveyor_project' not in package:
            package['appveyor_project'] = package['repo']
        if 'circleci' in package['badges'] and 'circleci_project' not in package:
            package['circleci_project'] = package['repo']
        if 'travis' in package['badges'] and 'travis_project' not in package:
            package['travis_project'] = package['repo']

affiliated['packages'] = sorted(affiliated['packages'], key=lambda x: x['name'].lower())

template = Template(open('template.html', 'r').read())


with open('status.html', 'w') as f:
    f.write(template.render(config=config))
