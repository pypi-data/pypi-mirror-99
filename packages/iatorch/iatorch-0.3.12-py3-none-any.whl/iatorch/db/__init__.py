import os
from ..utils.utils import _get_package_dir
from mlflow.store.db.utils import _get_package_dir as _get_mlflow_dir

# package dir
IATORCH_PACKAGE_DIR = _get_package_dir()
MLFLOW_PACKAGE_DIR = _get_mlflow_dir()

# migration config for project database
IATORCH_PROJECT_ALEMBIC_DIR = os.path.join(IATORCH_PACKAGE_DIR, "db", "project", "migrations")

# migration config for experiments(mlflow) database
IATORCH_MLFLOW_ALEMBIC_DIR = os.path.join(IATORCH_PACKAGE_DIR, "db", "experiments", "migrations")
MLFLOW_ALEMBIC_DIR = os.path.join(MLFLOW_PACKAGE_DIR, "store", "db_migrations")
