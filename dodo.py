import os
if "PYCTDEV_ECOSYSTEM" not in os.environ:
    os.environ["PYCTDEV_ECOSYSTEM"] = "conda"

from pyctdev import *  # noqa: api

############################################################
# Website building task

def task_build_website():
    return {'actions': [
        'python make_status.py',
        'mkdir builtdocs',
        'mv status.html builtdocs/index.html',
        'cp static/style.css builtdocs/']}
