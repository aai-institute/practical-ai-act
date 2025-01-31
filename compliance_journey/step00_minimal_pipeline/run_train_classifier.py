import logging

import mlflow
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split

from compliance_journey.step00_minimal_pipeline.asec.data import AdultData
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from xgboost import XGBClassifier

from compliance_journey.step00_minimal_pipeline.asec.preprocessing import (
    default_preprocessing,
)
from config import MLFLOW_SUBFOLDER, FILE_NAME_ADULT


def main():
    name = "train_classifier"
    model_id = "xgb_classifier"

    adult_data = AdultData(FILE_NAME_ADULT)
    io_data = adult_data.load_input_output_data()
    X_train, X_test, y_train, y_test = train_test_split(
        io_data.inputs, io_data.outputs, test_size=0.2, random_state=31
    )

    y_train["income"] = y_train["income"].apply(lambda x: 1 if x == ">50K" else 0)
    y_test["income"] = y_test["income"].apply(lambda x: 1 if x == ">50K" else 0)

    pipeline = Pipeline([
        (
            "scale",
            ColumnTransformer([
                (
                    "scale",
                    StandardScaler(),
                    [col.value for col in AdultData.COLS_NUMERIC],
                )
            ]),
        ),
        ("model", XGBClassifier()),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    # precision = precision_score(y_test, y_pred)
    # recall = recall_score(y_test, y_pred)
    # f1 = f1_score(y_test, y_pred)

    mlflow.set_tracking_uri(MLFLOW_SUBFOLDER)
    mlflow.set_experiment(name)
    with mlflow.start_run():
        mlflow.log_metric("accuracy", accuracy)

        mlflow.set_tag("Training Info", "Basic LR model for iris data")

        signature = infer_signature(X_train, pipeline.predict(X_train))

        model_info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="asec_model",
            signature=signature,
            input_example=X_train,
            registered_model_name="xgb_classifier",
        )
        print(model_info)
        print(model_info.model_uri)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
