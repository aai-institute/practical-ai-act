import logging

import mlflow
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

from compliance_journey.step00_minimal_pipeline.asec.model_factory import ModelFactory
from compliance_journey.step00_minimal_pipeline.asec.data import AdultData

from config import MLFLOW_SUBFOLDER, FILE_NAME_ADULT


def main():
    name = "train_classifier"
    model_id = "xgb_classifier"

    adult_data = AdultData(FILE_NAME_ADULT)
    X, y = adult_data.load_input_output_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=31
    )

    pipeline = ModelFactory.create_xgb()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)

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
