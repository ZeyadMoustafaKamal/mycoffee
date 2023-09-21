import os

bind = "0.0.0.0:8000"
reload = True
reload_extra_files = ["gunicorn_config.py"]

def get_files_from_dir(dir, suffix='.html'):
    """ This name and the paramers are exists just for the resuability """
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(suffix):
                files.append(os.path.join(dirpath, filename))
    return files

def get_apps_dirs(dir):
    """ A help function to get all apps dirs assuming that the 
    apps should contain a templates subdir """
    apps = []
    for dir in os.listdir(dir):
        if os.path.exists(os.path.join(dir, 'templates')): # Just get the dirs that contains a "templates" subdir
            apps.append(dir)
    return apps

templates_files = get_files_from_dir('templates')
for app_dir in get_apps_dirs(os.getcwd()):
    templates_files.extend(get_files_from_dir(app_dir))

if templates_files:
    reload_extra_files.extend(templates_files)

