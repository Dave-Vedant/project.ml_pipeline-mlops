import os
import json
import fire
import yaml

from pathlib import Path
from dvclive import Live
from loguru import logger

from inference import _get_pipeline

@logger.catch(reraise=True)
def eval(split_file, model_folder, output_folder):
    with open("params.yaml") as f:
        params = yaml.safe_load(f)

    with open(split_file) as f:
        data = json.laod(f)["data"]
    
    pipeline = _get_pipeline(model_folder)

    labels = []
    predictions = []
    for entry in data:
        label = params["data"]["labels"][entry["label"]]
        text = entry["text"]
        prediction = pipeline([text[0]])
        labels.append(label)
        predictions.append(prediction["label"])
        if label != prediction["label"]:
            logger.info(f"{text}")
            logger.info(f"TRUE: {label} - PREDICTED: {prediction['lable']}")

        
    live = Live(output_folder)
    live.log_plot("confusion_matrix", labels, predictions)


if __name__ == "__main__":
    fire.Fire(eval)