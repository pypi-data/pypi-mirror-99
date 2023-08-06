import os
import sqlalchemy
import logging

from mlflow.pytorch import save_model
from mlflow.models.model import Model as MlflowModel

from mlflow.entities.lifecycle_stage import LifecycleStage
from mlflow.utils.uri import extract_db_type_from_uri
from mlflow.utils.file_utils import TempDir

from mlflow.store.tracking.sqlalchemy_store import SqlAlchemyStore
from mlflow.store.db.base_sql_model import Base
from mlflow.store.db.db_types import MYSQL, MSSQL, SQLITE
from mlflow.store.db.utils import create_sqlalchemy_engine_with_retry, _verify_schema, _get_managed_session_maker
from mlflow.store.tracking.dbmodels.models import SqlExperiment, SqlRun, SqlMetric, SqlParam, SqlTag, SqlExperimentTag, SqlLatestMetric

from mlflow.tracking import MlflowClient
from mlflow.tracking._tracking_service import utils
from mlflow.tracking._tracking_service.utils import _TRACKING_URI_ENV_VAR
from mlflow.tracking._tracking_service.registry import TrackingStoreRegistry
from mlflow.tracking._tracking_service.client import TrackingServiceClient
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS

from pytorch_lightning.loggers import MLFlowLogger
from pytorch_lightning.loggers.base import rank_zero_experiment
from pytorch_lightning.utilities import rank_zero_only, rank_zero_warn


ARTIFACT_MODEL_PATH = 'model'
_logger = logging.getLogger(__name__)

################################################################################################################################
# Wrapper for MLflow and PyTorch-Lightning MLflow Logger
#   iatorch local UI 개발을 위해 sqlite 사용 필요 (일반사용자들이 database server를 설치하는 불편을 덜기 위해서)
#   MLFlow(ver. 1.13)는 sqlite 사용 시 artifact_root를 원하는대로 지정할 수 없음 (코드 자체에 문제 있으미)
#   기존 MlflowClient를 override하여 sqlite 사용 시에도 artifact_root를 지정할 수 있도록 변경하여 해결
#   PyTorch-Lightning MLFlowLogger도 새로운 MlflowClient(IAMlflowLogger)를 사용하도록 override (log_model method도 추가)
################################################################################################################################

################################################################
# Wrapper for SqlAlchemyStore
################################################################
class IASqlAlchemyStore(SqlAlchemyStore):

    ARTIFACTS_FOLDER_NAME = "artifacts"

    def __init__(self, db_uri, default_artifact_root, first_experiment_name=None):
        super(SqlAlchemyStore, self).__init__()
        
        self.db_uri = db_uri
        self.db_type = extract_db_type_from_uri(db_uri)
        self.artifact_root_uri = default_artifact_root
        self._first_experiment_name = first_experiment_name if first_experiment_name is not None else 'Default'
        
        self.engine = create_sqlalchemy_engine_with_retry(db_uri)
        _verify_schema(self.engine)
        
        Base.metadata.bind = self.engine
        SessionMaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.ManagedSessionMaker = _get_managed_session_maker(SessionMaker, self.db_type)
        
        # create default experiment if db is empty
        if len(self.list_experiments()) == 0:
            with self.ManagedSessionMaker() as session:
                first_experiment_name = first_experiment_name if first_experiment_name is not None else 'Default'
                self._create_default_experiment(session, first_experiment_name)

    def _create_default_experiment(self, session, first_experiment_name):
        default_experiment_id = 0
        artifact_location = str(self._get_artifact_location(default_experiment_id))
        
        table = SqlExperiment.__tablename__
        default_experiment = {
            SqlExperiment.experiment_id.name: default_experiment_id,
            SqlExperiment.name.name: first_experiment_name,
            SqlExperiment.artifact_location.name: artifact_location,
            SqlExperiment.lifecycle_stage.name: LifecycleStage.ACTIVE,
        }

        quotes = lambda x: f"'{x}'" if isinstance(x, str) else f"{x}"
        columns = list(default_experiment.keys())
        values = ", ".join([quotes(default_experiment.get(c)) for c in columns])

        try:
            self._set_zero_value_insertion_for_autoincrement_column(session)
            session.execute(
                "INSERT INTO {} ({}) VALUES ({});".format(table, ", ".join(columns), values)
            )
        finally:
            self._unset_zero_value_insertion_for_autoincrement_column(session)

################################################################
# Wrapper for TrackingServiceClient
################################################################
class IATrackingServiceClient(TrackingServiceClient):
    def __init__(self, tracking_uri, artifact_root, first_experiment_name=None):
        super(TrackingServiceClient, self).__init__()
        self.tracking_uri = tracking_uri
        os.environ[_TRACKING_URI_ENV_VAR] = self.tracking_uri
        self.store = IASqlAlchemyStore(
            db_uri=self.tracking_uri, 
            default_artifact_root=artifact_root, 
            first_experiment_name=first_experiment_name
        )
        
################################################################
# Wrapper for MlflowClient
################################################################
class IAMlflowClient(MlflowClient):
    def __init__(self, tracking_uri, artifact_root, registry_uri=None, first_experiment_name=None):
        super(MlflowClient, self).__init__()
        self._registry_uri = registry_uri if registry_uri is not None else tracking_uri
        self._tracking_client = IATrackingServiceClient(
            tracking_uri=tracking_uri, 
            artifact_root=artifact_root, 
            first_experiment_name=first_experiment_name,
        )
        
################################################################
# Wrapper for MLFlowLogger (PyTorch-Lightning)
################################################################
class IAMLFlowLogger(MLFlowLogger):
    def __init__(self, tracking_uri, artifact_root, registry_uri=None, experiment_name='Default', tags=None, prefix='',):
        super(MLFlowLogger, self).__init__()
        self._tracking_uri = tracking_uri
        self._experiment_id = None
        self._experiment_name = experiment_name
        self._run_id = None
        self._artifact_path = None
        self.tags = tags
        self._prefix = prefix
        self._mlflow_client = IAMlflowClient(
            tracking_uri=self._tracking_uri, 
            artifact_root=artifact_root,
            registry_uri=None,
            first_experiment_name=experiment_name,
        )
        
    @property
    @rank_zero_experiment
    def experiment(self):
        if self._experiment_id is None:
            expt = self._mlflow_client.get_experiment_by_name(self._experiment_name)
            if expt is not None:
                self._experiment_id = expt.experiment_id
            else:
                _logger.warning(f'Experiment with name {self._experiment_name} not found. Creating it.')
                self._experiment_id = self._mlflow_client.create_experiment(name=self._experiment_name)
        if self._run_id is None:
            run = self._mlflow_client.create_run(experiment_id=self._experiment_id, tags=self.tags)
            self._run_id = run.info.run_id
        return self._mlflow_client
        
    @rank_zero_only
    def log_model(self, model, **kwargs):
        artifact_path=ARTIFACT_MODEL_PATH
        with TempDir() as tmp:
            local_path = tmp.path("model")
            mlflow_model = MlflowModel(run_id=self._run_id, artifact_path=artifact_path)
            # save model to localpath (temporary)
            save_model(
                pytorch_model=model, 
                path=local_path, 
                conda_env=None,
                mlflow_model=mlflow_model, 
                code_paths=None,
                pickle_module=None,
                signature=None,
                input_example=None,
                requirements_file=None,
                extra_files=None,
                **kwargs
            )
            # upload model to artifact_path
            self.experiment.log_artifacts(self._run_id, local_path, artifact_path=artifact_path)
            self.experiment._record_logged_model(self._run_id, mlflow_model)
