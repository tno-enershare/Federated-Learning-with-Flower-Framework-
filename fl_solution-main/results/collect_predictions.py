import os
import logging

from numpy import load as np_load
from pandas import DataFrame

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def collect_predictions(num_clients):
    prediction_dict = {}
    for i in range(num_clients):
        prediction_path = f'/results/client_prediction_{i}.npy'
        if os.path.exists(prediction_path):
            prediction = np_load(prediction_path).flatten()
            logger.info(f"Client {i} prediction: {prediction}")
            prediction_dict[f'Client_{i}'] = prediction
        else:
            logger.error(f"File {prediction_path} not found")

    if not prediction_dict:
        logger.error("No predictions found. Exiting.")
        return

    df = DataFrame(prediction_dict)
    os.makedirs('/results', exist_ok=True)
    df.to_csv('/results/predictions.csv', index=False)
    logger.info("Predictions collected and saved to /results/predictions.csv")


if __name__ == "__main__":
    num_clients = int(os.environ.get('NUM_CLIENTS', 5))
    logger.info(f"Collecting predictions for {num_clients} clients...")
    collect_predictions(num_clients)
