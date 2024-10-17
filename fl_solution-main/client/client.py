import logging
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import flwr as fl
from tensorflow import keras
from numpy import load as np_load, save as np_save, newaxis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_data(client_id):
    logger.info(f"Client {client_id}: Loading data...")
    x_train = np_load(f'/results/client_data_{client_id}_features.npy')
    y_train = np_load(f'/results/client_data_{client_id}_labels.npy')
    last_day = np_load(f'/results/client_data_{client_id}_last_day.npy')
    return x_train, y_train, last_day


def create_model(input_shape):
    logger.info(f"Creating model with input shape {input_shape}...")
    model = keras.Sequential([
        keras.layers.LSTM(128, activation='relu', input_shape=input_shape, return_sequences=True),
        keras.layers.LSTM(64, activation='relu'),
        keras.layers.Dense(96)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


class Client(fl.client.NumPyClient):
    def __init__(self, client_id):
        logger.info(f"Client {client_id}: Initializing...")
        self.x_train, self.y_train, self.last_day = load_data(client_id)
        self.model = create_model((self.x_train.shape[1], self.x_train.shape[2]))

    def get_parameters(self):
        logger.info("Getting model parameters...")
        return self.model.get_weights()

    def fit(self, parameters, config):
        logger.info("Starting training...")
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=1, batch_size=32, verbose=0)
        logger.info("Training finished.")
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        logger.info("Starting evaluation...")
        self.model.set_weights(parameters)
        loss, mae = self.model.evaluate(self.x_train, self.y_train, verbose=0)
        logger.info(f"Evaluation finished. Loss: {loss}, MAE: {mae}")
        return loss, len(self.x_train), {"mae": mae}

    def predict(self):
        logger.info("Making predictions...")
        prediction = self.model.predict(self.last_day[newaxis, :, :])
        logger.info("Prediction finished.")
        return prediction


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python client.py <client_id>")
        sys.exit(1)

    client_id = int(sys.argv[1])
    logger.info(f"Client {client_id}: Starting...")
    client = Client(client_id)
    fl.client.start_numpy_client(server_address="server:8080", client=client)
    logger.info(f"Client {client_id}: Federated learning finished.")
    prediction = client.predict()
    np_save(f'/results/client_prediction_{client_id}.npy', prediction)
    logger.info(f"Client {client_id}: Prediction saved at /results/client_prediction_{client_id}.npy")
