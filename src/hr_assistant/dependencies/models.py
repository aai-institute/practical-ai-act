from typing import Annotated

import mlflow.pyfunc
from fastapi import Depends, Request


def _get_model(request: Request) -> mlflow.pyfunc.PyFuncModel:
    return request.app.state.model


ModelDependency = Annotated[mlflow.pyfunc.PyFuncModel, Depends(_get_model)]
