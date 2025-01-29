import mlflow
import pandas as pd
from dagster import asset
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from xgboost import XGBClassifier

from income_prediction.census_asec_data_description import CensusASECDataDescription
from income_prediction.config import RANDOM_STATE


@asset()
def income_prediction_model(train_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
    train_input = train_data.drop([CensusASECDataDescription.Column.TARGET], axis=1)
    train_output = train_data[CensusASECDataDescription.Column.TARGET]

    # test_input = test_data.drop(CensusASECDataDescription.TARGET, axis=1)
    # test_outout = test_data[CensusASECDataDescription.TARGET]

    categorical_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])

    numerical_pipeline = Pipeline([("scaler", StandardScaler())])

    ordinal_pipeline = Pipeline([("encoder", OrdinalEncoder())])

    column_transformer = ColumnTransformer(
        [
            (
                "categorical_pipeline",
                categorical_pipeline,
                CensusASECDataDescription.COLS_CATEGORICAL,
            ),
            ("numerical_pipeline", numerical_pipeline, CensusASECDataDescription.COLS_NUMERIC),
            ("ordinal_pipeline", ordinal_pipeline, CensusASECDataDescription.COLS_ORDINAL),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessor", column_transformer),
            ("classifier", XGBClassifier(random_state=RANDOM_STATE)),
        ]
    )

    mlflow.set_tracking_uri("http://localhost:4040")
    mlflow.set_experiment("Income Prediction")

    mlflow.sklearn.autolog()
    mlflow.xgboost.autolog()

    with mlflow.start_run():
        pipeline.fit(train_input, train_output)

        mlflow.evaluate(
            model=pipeline.predict,
            data=test_data,
            targets=CensusASECDataDescription.TARGET,
            model_type="classifier",
        )


if __name__ == "__main__":
    train_data = pd.read_csv("data/train_data.csv", index_col=0)
    test_data = pd.read_csv("data/test_data.csv", index_col=0)

    income_prediction_model(train_data, test_data)
