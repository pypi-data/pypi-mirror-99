from datetime import datetime, timezone
from enum import Enum
from typing import List, Union

from src.typegenie.api import AccountAPI, DeploymentAPI, UserAPI
import pandas as pd
import traceback


class __Authenticator:
    def __init__(self):
        self._account_api = None
        self._deployment_api = {}
        self._user_api = {}
        self._automatic_fallback = False
        self._automatic_renew = False

    def authenticate_account(self, username, password):
        self._account_api = AccountAPI(username=username, password=password)

    def authenticate_deployment(self, deployment_id, token):
        self._deployment_api[deployment_id] = DeploymentAPI(token=token)
        if self._automatic_renew:
            self._deployment_api[deployment_id].enable_auto_renew()

    def authenticate_user(self, deployment_id, user_id, token):
        self._user_api[(deployment_id, user_id)] = UserAPI(token=token)
        if self._automatic_renew:
            self._user_api[(deployment_id, user_id)].enable_auto_renew()

    def reset(self):
        self._account_api = None
        if self._automatic_renew:
            for api in self._deployment_api.values():
                api.disable_auto_renew()
            for api in self._user_api.values():
                api.disable_auto_renew()

        self._deployment_api = {}
        self._user_api = {}

    def get_account_api(self):
        if self._account_api is None:
            raise RuntimeError('First authenticate using `authenticator.authorize_account(username, password)`')
        return self._account_api

    def get_deployment_api(self, deployment_id):
        if deployment_id in self._deployment_api:
            return self._deployment_api[deployment_id]
        elif self._automatic_fallback:
            account_api = self.get_account_api()
            token = account_api.get_deployment_access_token(deployment_id=deployment_id)['token']
            self.authenticate_deployment(deployment_id=deployment_id, token=token)
        else:
            raise RuntimeError('First authenticate using `authenticator.authenticate_deployment(deployment_id, token)`')

    def get_user_api(self, user_id, deployment_id=None):
        if (deployment_id, user_id) in self._user_api:
            return self._user_api[(deployment_id, user_id)]
        elif self._automatic_fallback and deployment_id is not None:
            deployment_api = self.get_deployment_api(deployment_id=deployment_id)
            token = deployment_api.get_user_access_token(user_id=user_id)['token']
            return self.authenticate_user(deployment_id=deployment_id, user_id=user_id, token=token)
        else:
            raise RuntimeError('First authenticate using `authenticator.authenticate_user(deployment_id, user_id, token)`')

    def enable_auto_fallback(self):
        self._automatic_fallback = True

    def enable_auto_renew(self):
        self._automatic_renew = True


authenticator = __Authenticator()


class Configuration:
    def __init__(self):
        self._id = None
        self._description = None

    @property
    def id(self):
        return self._id

    @staticmethod
    def from_dict(json):
        config = Configuration()
        config._id = json['id']
        config._description = json['description']
        return config

    def __repr__(self):
        return repr(self.to_dict())

    def to_dict(self):
        json = {
            'id': self._id,
            'description': self._description
        }
        return json


class EventType(Enum):
    CONTEXTUAL = "CONTEXTUAL"
    MESSAGE = "MESSAGE"


class Author(Enum):
    SYSTEM = "SYSTEM"
    AGENT = "AGENT"
    USER = "USER"


class Event:
    def __init__(self, author_id: str, author: Author, event: EventType, value: str,
                 timestamp: Union[str, datetime]):
        self._author_id = author_id
        self._author = author.name
        self._event = event.name
        self._value = value
        self._timestamp = timestamp if isinstance(timestamp, datetime) else pd.to_datetime(
            timestamp).to_pydatetime().replace(tzinfo=timezone.utc)

    def to_dict(self):
        json = {
            'author_id': self._author_id,
            'author': self._author,
            'event': self._event,
            'value': self._value,
            'timestamp': self._timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        return json


class Dialogue:
    def __init__(self, dialogue_id, metadata={}):
        self.id = dialogue_id
        self.metadata = metadata
        self.events: List[Dialogue.Event] = []

    def to_dict(self):
        json = {
            'id': self.id,
            'metadata': self.metadata,
            'events': [e.to_dict() for e in self.events]
        }
        return json


class DeploymentEvent:
    def __init__(self):
        self._dataset_ids = None
        self._configuration_id = None
        self._timestamp = None
        self._event = None

    def __repr__(self):
        return repr(self.to_dict())

    @staticmethod
    def from_dict(json):
        event = DeploymentEvent()
        event._dataset_ids = json['dataset_ids']
        event._configuration_id = json['configuration_id']
        event._timestamp = pd.to_datetime(json['timestamp']).to_pydatetime().replace(tzinfo=timezone.utc)
        event._event = json['event']
        return event

    def to_dict(self):
        json = {
            'dataset_ids': self._dataset_ids,
            'configuration_id': self._configuration_id,
            'timestamp': self._timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'event': self._event
        }
        return json


class Dataset:
    def __init__(self):
        self._id = None
        self._deployment_id = None
        self._metadata = None
        self._num_dialogues = None

    @property
    def id(self):
        return self._id

    @property
    def deployment_id(self):
        return self._deployment_id

    @property
    def metadata(self):
        return self._metadata

    @property
    def created_at(self):
        return self._created_at

    @property
    def num_dialogues(self):
        return self._num_dialogues

    def update(self, metadata):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        deployment_api.update_dataset(dataset_id=self._id, metadata=metadata)
        self._metadata = metadata

    def upload(self, dialogues: List[Dialogue]):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        deployment_api.upload_dialogues(dataset_id=self._id, dialogues=[d.to_dict() for d in dialogues])

    @staticmethod
    def from_dict(json):
        # TODO(abhi) remove these after Omkar's fix
        metadata = json['metadata'] if 'metadata' in json else {}
        dataset = Dataset()
        dataset._id = json['id']
        dataset._metadata = metadata
        dataset._deployment_id = json['deployment_id']
        dataset._num_dialogues = json['num_dialogues']
        dataset._created_at = pd.to_datetime(json['created_at']).to_pydatetime().replace(tzinfo=timezone.utc)
        return dataset

    def delete(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        deployment_api.delete_dataset(dataset_id=self._id)
        self._id = None

    def get_download_links(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        return deployment_api.download_dataset(dataset_id=self._id)

    def __del__(self):
        # Only delete from database when user explicitly deleted the instance
        trace = traceback.format_stack()
        user_called = True if len(trace) >= 2 and ' del ' in trace[-2] else False
        if user_called and self._id is not None:
            self.delete()

    def __repr__(self):
        return repr(self.to_dict())

    def to_dict(self):
        json = {
            'id': self._id,
            'metadata': self._metadata,
            'created_at': self._created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'num_dialogues': self._num_dialogues,
            'deployment_id': self._deployment_id
        }
        return json


class Deployment:
    def __init__(self):
        self._id = None
        self._metadata = {}
        self._created_at = None
        self._dataset = None

    @property
    def id(self):
        return self._id

    @staticmethod
    def create(deployment_id, metadata):
        account_api = authenticator.get_account_api()
        account_api.create_deployment(deployment_id=deployment_id, metadata=metadata)
        json = account_api.get_deployment(deployment_id=deployment_id)
        return Deployment.from_dict(json)

    def authenticate(self):
        account_api: AccountAPI = authenticator.get_account_api()
        token = account_api.get_deployment_access_token(deployment_id=self._id)['token']
        authenticator.authenticate_deployment(deployment_id=self._id, token=token)

    @staticmethod
    def get(deployment_id):
        try:
            account_api = authenticator.get_account_api()
            json = account_api.get_deployment(deployment_id=deployment_id)
        except RuntimeError:
            deployment_api = authenticator.get_deployment_api(deployment_id=deployment_id)
            json = deployment_api.info()
        return Deployment.from_dict(json)

    def update(self, metadata):
        account_api = authenticator.get_account_api()
        account_api.update_deployement(deployment_id=self._id, metadata=metadata)
        self._metadata = metadata

    def deploy(self, config: Configuration, datasets: List[Dataset]):
        dataset_ids = [d.id for d in datasets]
        config_id = config.id
        assert all(tid is not None for tid in datasets + [config_id]), "Either `datasets` and `config` is not " \
                                                                       "properly initialized "

        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        return deployment_api.deploy_model(dataset_ids=dataset_ids, model_config_id=config_id)

    def undeploy(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        return deployment_api.undeploy_model()

    def history(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        history = [DeploymentEvent.from_dict(h) for h in deployment_api.get_deployment_history()]
        return sorted(history, key=lambda x: x._timestamp)

    @property
    def configs(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        return [Configuration.from_dict(c) for c in deployment_api.list_model_configs()]

    def delete(self):
        account_api = authenticator.get_account_api()
        account_api.delete_deployment(deployment_id=self._id)
        self._id = None

    def __del__(self):
        # Only delete from database when user explicitly deleted the instance
        trace = traceback.format_stack()
        user_called = True if len(trace) >= 2 and ' del ' in trace[-2] else False
        if user_called and self._id is not None:
            self.delete()

    def datasets(self, dataset_id=None, create=False, metadata={}):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        if create:
            assert dataset_id is not None, "`dataset_id` must be provided to create a Dataset"
            deployment_api.create_dataset(dataset_id=dataset_id, metadata=metadata)
            return Dataset.from_dict(deployment_api.get_dataset(dataset_id=dataset_id))
        else:
            if dataset_id is None:
                return [Dataset.from_dict(r) for r in deployment_api.list_datasets()]
            else:
                return Dataset.from_dict(deployment_api.get_dataset(dataset_id=dataset_id))

    def users(self, user_id=None, create=False, metadata={}):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._id)
        if create:
            assert user_id is not None, "`user_id` must be provided to create a Dataset"
            deployment_api.add_user(user_id=user_id, metadata=metadata)
            return User.from_dict(deployment_api.get_user(user_id=user_id))
        else:
            if user_id is None:
                return [User.from_dict(r) for r in deployment_api.list_users()]
            else:
                return User.from_dict(deployment_api.get_user(user_id=user_id))

    @staticmethod
    def from_dict(json):
        # TODO(abhi) remove these after Omkar's fix
        metadata = json['metadata'] if 'metadata' in json else {}
        deployment = Deployment()
        deployment._id = json['id']
        deployment._metadata = metadata
        deployment._created_at = pd.to_datetime(json['created_at']).to_pydatetime().replace(tzinfo=timezone.utc)
        return deployment

    @staticmethod
    def list():
        result = authenticator.get_account_api().list_deployments()
        deployments = []
        for json in result:
            deployments.append(Deployment.from_dict(json))
        return deployments

    def __repr__(self):
        return repr(self.to_dict())

    def to_dict(self):
        json = {
            'id': self._id,
            'metadata': self._metadata,
            'created_at': self._created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        return json

    @staticmethod
    def get_access_token(deployment_id):
        account_api = authenticator.get_account_api()
        return account_api.get_deployment_access_token(deployment_id=deployment_id)


class User:
    def __init__(self):
        self._id = None
        self._deployment_id = None
        self._metadata = None
        self._created_at = None

    @property
    def id(self):
        return self._id

    @property
    def deployment_id(self):
        return self._deployment_id

    @property
    def metadata(self):
        return self._metadata

    @property
    def created_at(self):
        return self._created_at

    def update(self, metadata):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        deployment_api.update_user(user_id=self._id, metadata=metadata)
        self._metadata = metadata

    def __repr__(self):
        return repr(self.to_dict())

    def to_dict(self):
        json = {
            'id': self._id,
            'metadata': self._metadata,
            'created_at': self._created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'deployment_id': self._deployment_id
        }
        return json

    @staticmethod
    def from_dict(json):
        # TODO(abhi) remove these after Omkar's fix
        metadata = json['metadata'] if 'metadata' in json else {}
        user = User()
        user._id = json['id']
        user._metadata = metadata
        user._deployment_id = json['deployment_id']
        user._created_at = pd.to_datetime(json['created_at']).to_pydatetime().replace(tzinfo=timezone.utc)
        return user

    def delete(self):
        deployment_api = authenticator.get_deployment_api(deployment_id=self._deployment_id)
        deployment_api.delete_user(user_id=self._id)
        self._id = None

    def __del__(self):
        # Only delete from database when user explicitly deleted the instance
        trace = traceback.format_stack()
        user_called = True if len(trace) >= 2 and ' del ' in trace[-2] else False
        if user_called and self._id is not None:
            self.delete()
