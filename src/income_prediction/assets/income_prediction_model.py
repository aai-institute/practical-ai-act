import mlflow
import pandas as pd
from dagster import asset, AssetExecutionContext
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier

from income_prediction.census_asec_data_description import CensusASECDataDescription
from income_prediction.config import RANDOM_STATE
from income_prediction.resources.mlflow_session import MlflowSession

ALL_TRAINING_COLS = list(CensusASECDataDescription.COLS_NUMERIC + CensusASECDataDescription.COLS_CATEGORICAL + CensusASECDataDescription.COLS_ORDINAL)


@asset
def income_prediction_model(
    context: AssetExecutionContext,
    mlflow_session: MlflowSession,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> None:
    train_input = train_data[ALL_TRAINING_COLS].copy()
    train_output = train_data[CensusASECDataDescription.TARGET]

    categorical_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])

    numerical_pipeline = Pipeline([("scaler", StandardScaler())])

    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    # Column sets given to Pipeline objects need to be `pd.Index`es, so we go indirectly over
    # df[list(COLS)].columns, for different sets of COLS.
    column_transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                categorical_pipeline,
                train_input[list(CensusASECDataDescription.COLS_CATEGORICAL)].columns,
            ),
            ("numerical_pipeline", numerical_pipeline, train_input[list(CensusASECDataDescription.COLS_NUMERIC)].columns),
            ("ordinal_pipeline", ordinal_pipeline, train_input[list(CensusASECDataDescription.COLS_ORDINAL)].columns),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessor", column_transformer),
            ("classifier", XGBClassifier(random_state=RANDOM_STATE)),
        ]
    )

    with mlflow_session.get_run(context):
        mlflow.sklearn.autolog()
        mlflow.xgboost.autolog()

        pipeline.fit(train_input, train_output)

        mlflow.evaluate(
            model=pipeline.predict,
            data=test_data,
            targets=CensusASECDataDescription.TARGET,
            model_type="classifier",
        )


if __name__ == "__main__":
    from dagster import build_asset_context
    from income_prediction import mlflow_session
    train_data = pd.read_csv("data/train_data.csv", index_col=0)
    test_data = pd.read_csv("data/test_data.csv", index_col=0)

    # TODO: This won't run, since the context is missing a `run` attribute.
    ctx = build_asset_context()
    income_prediction_model(ctx, mlflow_session, train_data, test_data)
