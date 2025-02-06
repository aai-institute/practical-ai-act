from typing import Annotated

import mlflow.sklearn
from fastapi import Depends, Request


def _get_model(request: Request) -> mlflow.sklearn.Model:
    return request.app.state.model


ModelDependency = Annotated[mlflow.sklearn.Model, Depends(_get_model)]
