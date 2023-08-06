import sys
from databricksbundle.dbutils.IPythonDbUtilsResolver import resolve_db_utils


def get_notebook_context():
    return resolve_db_utils().notebook.entry_point.get_dbutils().notebook().get_context()


def get_user_email():
    return get_notebook_context().tags().get("user").get()


def get_notebook_path():
    return get_notebook_context().notebook_path().get()


def is_notebook_environment():
    return sys.argv and sys.argv[0][-15:] == "/PythonShell.py"
