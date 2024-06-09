import os
import neptune
from joblib import load
from dotenv import load_dotenv

load_dotenv()
NEPTUNE_PROJECT = os.getenv("NEPTUNE_PROJECT")
NPETUNE_API_TOKEN = os.getenv("NPETUNE_API_TOKEN")
MODEL_ID = os.getenv("MODEL_ID")
MODEL_LOCAL_PATH = "model.joblib"


def get_model_versions(model_id=MODEL_ID):
    """
    Get the model neptune object and dataframe of the model version
    """
    model = neptune.init_model(
        project=NEPTUNE_PROJECT, api_token=NPETUNE_API_TOKEN, with_id=model_id
    )
    model_versions_df = model.fetch_model_versions_table().to_pandas()
    return model, model_versions_df


def get_production_models(model_versions_df):
    """
    Get the production ready models
    """
    condition = model_versions_df["sys/stage"] == "production"
    return model_versions_df[condition]


def download_production_ready_model():
    """
    Retrieve the production-ready model from Neptune and downloads it.

    Returns
        str: The ID of the downloaded model version.
    """
    model, model_versions_df = get_model_versions(model_id=MODEL_ID)

    production_models = get_production_models(model_versions_df)

    for _, model_version in production_models.iterrows():
        version_id = model_version["sys/id"]
        model_version = neptune.init_model_version(
            project=NEPTUNE_PROJECT, api_token=NPETUNE_API_TOKEN, with_id=version_id
        )
        model_version["model"].download(MODEL_LOCAL_PATH)

    model_version.stop()
    model.stop()
