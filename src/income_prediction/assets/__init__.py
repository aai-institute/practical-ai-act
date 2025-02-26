import dagster as dg
import mlflow
import sklearn.pipeline
from sklearn.model_selection import train_test_split
from asec.model_factory import ModelFactory


import optuna
import pandas as pd



from asec.features import get_income_prediction_features
from asec.data import CensusASECMetadata, download_and_filter_census_data

from ..resources.configuration import Config, OptunaCVConfig
from ..resources.mlflow_session import MlflowSession



@dg.asset(io_manager_key="lakefs_io_manager")
def census_asec_dataset(config: Config):
    """Downloads and filters the Census ASEC dataset based on the UCI Adult dataset criteria."""
    return download_and_filter_census_data(config.census_asec_dataset_year)


@dg.asset(io_manager_key="lakefs_io_manager")
def income_prediction_features(
    config: Config, census_asec_dataset: pd.DataFrame
) -> pd.DataFrame:
    """Pre-processes the Census ASEC dataset for income prediction."""
    return get_income_prediction_features(config.salary_bands, census_asec_dataset)


@dg.multi_asset(
    outs={
        "train_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
        "test_data": dg.AssetOut(io_manager_key="lakefs_io_manager"),
    }
)
def train_test_data(
    config: Config, income_prediction_features: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset for income prediction into training and test sets."""
    train_data, test_data = train_test_split(
        income_prediction_features, random_state=config.random_state
    )
    return train_data, test_data



@dg.asset
def optuna_search_xgb(
        context: dg.AssetExecutionContext,
        mlflow_session: MlflowSession,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        optuna_cv_config: OptunaCVConfig,
        optuna_xgb_param_distribution: dg.ResourceParam[dict[str, optuna.distributions.BaseDistribution]],
):

    optuna_search = optuna.integration.OptunaSearchCV(
        ModelFactory.create_xgb(), param_distributions=optuna_xgb_param_distribution, **optuna_cv_config.as_dict()
    )

    optuna_search.fit(train_data.drop(columns=CensusASECMetadata.TARGET), train_data[CensusASECMetadata.TARGET])

    with mlflow_session.start_run(context):
        with mlflow.start_run(nested=True, run_name="xgboost-classifier"):
            mlflow.autolog(log_datasets=False)
            best_model = optuna_search.best_estimator_
            best_model.fit(train_data.drop(columns=CensusASECMetadata.TARGET), train_data[CensusASECMetadata.TARGET])
            mlflow.evaluate(
                model=best_model.predict,
                data=test_data,
                targets=CensusASECMetadata.TARGET,
                model_type="classifier",
            )
            return best_model




@dg.asset(io_manager_key="lakefs_io_manager")
def reference_dataset(
    optuna_search_xgb: sklearn.pipeline.Pipeline,
    test_data: pd.DataFrame,
) -> pd.DataFrame:
    """Reference dataset for post-deployment performance monitoring

    Based on predictions of the model on the test dataset"""

    y_proba = optuna_search_xgb.predict_proba(test_data)

    df = test_data.rename({CensusASECMetadata.TARGET: "target"}, axis=1)
    df = pd.concat(
        [df, pd.Series(y_proba.tolist(), name="predicted_probabilities")], axis=1
    )
    return df
