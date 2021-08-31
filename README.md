### The HoloViz Dashboard

This repository is used to generate a dashboard that allows statuses for various
services to be shown for all holoviz-related packages.

The main configuration of the dashboard is done via the ``dashboard.yml`` file,
which can contain several sections with a list of packages, and a list of services for each
section.

To build the site, start by installing `pyctdev` either in your *base* environment or in a dedicated one:
```
conda install -c pyviz "pyctdev>=0.5"
```

Then run the following commands to create the dev environment *status*, activate it and built the website:
```
doit env_create --name status
conda activate status
doit build_website
```

The dashboard can be seen online [here](http://status.holoviz.org)
