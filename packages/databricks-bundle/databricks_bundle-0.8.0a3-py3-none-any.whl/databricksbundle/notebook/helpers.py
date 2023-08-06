import sys
from databricksbundle.dbutils.IPythonDbUtilsResolver import resolve_db_utils


def get_notebook_context():
    return resolve_db_utils().notebook.entry_point.getDbutils().notebook().getContext()


def get_user_email():
    return get_notebook_context().tags().get("user").get()


def get_notebook_path():
    return get_notebook_context().notebookPath().get()


def is_notebook_environment():
    return sys.argv and sys.argv[0][-15:] == "/PythonShell.py"
