import dagster as dg
import pandas as pd


# FIXME: This is a hack to demonstrate the sensor concepts
class InferenceLog(dg.ConfigurableResource):
    api_base_url: str = "http://localhost:8000"

    def fetch_inference_log(self):
        """Fetch inference logs from the FastAPI application"""
        return pd.read_csv(f"{self.api_base_url}/model/logs")
