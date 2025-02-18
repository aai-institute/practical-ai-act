from abc import abstractmethod, ABC
from typing import Any

from dagster import ConfigurableResource
from xgboost import XGBClassifier

from asec.model_factory import build_pipeline


class ModelFactory(ConfigurableResource, ABC):

    @abstractmethod
    def create(self) -> Any:
        pass


class XGBClassifierFactory(ModelFactory):
    random_state: int = 42

    def create(self):
        return build_pipeline(XGBClassifier(random_state=self.random_state))


