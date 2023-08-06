import os, logging, dirsync
from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists
from alembic import command
from alembic.config import Config
from iatorch.db import IATORCH_PROJECT_ALEMBIC_DIR, IATORCH_MLFLOW_ALEMBIC_DIR, MLFLOW_ALEMBIC_DIR
from iatorch.db.project.model import Base as ProjectBase
# from mlflow.store.tracking.dbmodels.models import Base as ExperimentsBase
from mlflow.store.tracking.dbmodels.initial_models import Base as ExperimentsBase

logger = logging.getLogger('migrations') 
logger.setLevel(logging.WARNING)

MIGRATIONS = {
    'project': {
        'alembic_src': [IATORCH_PROJECT_ALEMBIC_DIR],
        'subdir': '',
        'fn': 'project.db',
        'Base': ProjectBase,
    },
    'experiments': {
        'alembic_src': [IATORCH_MLFLOW_ALEMBIC_DIR, MLFLOW_ALEMBIC_DIR],
        'subdir': 'results',
        'fn': 'experiments.db',
        'Base': ExperimentsBase,
    }
}

################################################################################################################################
# Utils for db migrations and connection
################################################################################################################################

################################################################
# sort_labels
################################################################
def _migrate(root, alembic_src, subdir, fn, Base):
    '''
    migrate database
    (NOTE) for local database 'sqlite' only!!!
    
    Arguments
    ---------
    root: <str>
      project root directory
    alembic_src: <str>
      alembic migration configuration files
    subdir: <str>
      subdir for database file - your database will be saved into <root>/<subdir>/dbname.db
    fn: <str>
      database file name
    Base: <str>
      sqlalchemy <Base> contains table information
    '''
    root = os.path.abspath(root)
    
    db_dir = os.path.join(root, subdir)
    migration_dir = os.path.join(db_dir, '.migrations')
    migration_versions_dir = os.path.join(migration_dir, 'versions')

    # craete directory if not exist
    if not os.path.exists(migration_versions_dir):
        os.makedirs(migration_versions_dir)
        os.chmod(migration_versions_dir, mode=0o775)

    # sync files for migration
    if not isinstance(alembic_src, list):
        alembic_src = [alembic_src]
    for src in alembic_src:
        dirsync.sync(src, migration_dir, logger=logger, action='sync', verbose=False)

    # create database
    db_uri = f"sqlite:///{os.path.join(db_dir, fn)}"
    engine = create_engine(db_uri)
    if not database_exists(db_uri):
        Base.metadata.create_all(engine)

    # migrate if required
    config = Config(os.path.join(migration_dir, "alembic.ini"))
    config.set_section_option("logger_alembic", "level", "WARN")
    config.set_main_option("script_location", migration_dir)
    config.set_main_option("sqlalchemy.url", db_uri)
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "heads")
        
    return db_uri
        

def migrate_all(root, migrations=MIGRATIONS):
    '''
    migrate two databases
      (1) project database from [IATORCH_PROJECT_ALEMBIC_DIR]
      (2) mlflow database from [IATORCH_MLFLOW_ALEMBIC_DIR, MLFLOW_ALEMBIC_DIR]
    '''
    uri = dict()
    for db, migration in migrations.items():
        uri[db] = _migrate(root=root, **migration)
        
    return uri


def migrate_experiments(root, migration=MIGRATIONS['experiments']):
    '''
    migrate experiments (mlflow database) only
    
    Arguments
    ---------
    root : str
        project root path
    migration : dict()
        use default, no need to change
    '''
    
    artifact_root = os.path.jon(root, migration['subdir'])
    os.environ[ARTIFACT_ROOT_ENV_VAR] = artifact_root
    db_uri = _migrate(root=root, **migration)
    
    return db_uri, artifact_root

################################################################
# require_experiments_database
################################################################
# def require_mlflow_database(root):
#     '''
#     cli startproject <pjt> 시점에 동작, 따라서 root는 pjt root를 입력.
    
#     Arguments
#     ---------
#     root: str or path
#       project root
#     '''
#     # DEFAULT RESULTS DIR & DB NAME
#     RESULTS_DIR = "results"
#     DB_FILENAME = 'mlruns.db'
    
#     # INIT
#     root = os.path.abspath(root)
#     results_dir = os.path.join(root, RESULTS_DIR)
#     migration_dir = os.path.join(results_dir, '.migrations')
#     if not os.path.exists(results_dir):
#         os.makedirs(results_dir)
#         os.chmod(results_dir, mode=0o775)
        
#     # CREATE MIGRATIONS DIR
#     migrations_dir = os.path.join(results_dir, '.migrations')
#     _set_migrations(migrations_dir=migrations_dir)
        
#     # SET store_uri, artifact_root
#     # (not working) store_uri = os.path.join('sqlite:///', results_dir, NAME)
#     store_uri = f"sqlite:///{results_dir}/{NAME}"
#     artifact_root = results_dir
#     os.environ[ARTIFACT_ROOT_ENV_VAR] = artifact_root
    
#     # create db if no exists
#     engine = create_engine(store_uri)
#     if not database_exists(store_uri):
#         InitialBase.metadata.create_all(engine)
#     else:
#         required_tables = [table.__tablename__ for table in [SqlExperiment, SqlRun, SqlMetric, SqlParam, SqlTag, SqlExperimentTag, SqlLatestMetric]]
#         current_tables = inspect(engine).get_table_names()
#         if any([table not in current_tables for table in required_tables]):
#             InitialBase.metadata.create_all(engine)
                
#     # make migration if needed
#     config = Config(os.path.join(migrations_dir, "alembic.ini"))
#     config.set_section_option("logger_alembic", "level", "WARN")
#     config.set_main_option("script_location", migrations_dir)
#     config.set_main_option("sqlalchemy.url", store_uri)
#     with engine.begin() as connection:
#         config.attributes["connection"] = connection  # pylint: disable=E1137
#         command.upgrade(config, "heads")
    
#     return store_uri, artifact_root
