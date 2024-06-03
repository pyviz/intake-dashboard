### The HoloViz Dashboard

This repository is used to generate a dashboard that allows statuses for various
services to be shown for all holoviz-related packages.

The main configuration of the dashboard is done via the ``dashboard.yml`` file,
which can contain several sections with a list of packages, and a list of services for each
section.

To build the site:

- Create a virtual environment
- Install the dependencies with `pip install -r requirements.txt`
- Run `python build_website.py`

The dashboard can be seen online [here](http://status.holoviz.org)
