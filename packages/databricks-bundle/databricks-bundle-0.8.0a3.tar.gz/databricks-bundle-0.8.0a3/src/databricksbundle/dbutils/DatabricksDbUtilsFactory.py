from databricksbundle.dbutils.DbUtilsWrapper import DbUtilsWrapper
from databricksbundle.dbutils.IPythonDbUtilsResolver import resolve_db_utils


class DatabricksDbUtilsFactory:
    def create(self) -> DbUtilsWrapper:
        return DbUtilsWrapper(resolve_db_utils)
