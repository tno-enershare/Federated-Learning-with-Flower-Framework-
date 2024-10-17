import logging
import os

from flwr import server as fl_server
from numpy import concatenate, load as np_load
from tensorflow import keras

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_model(input_shape):
    logger.info(f"Creating global model with input shape {input_shape}...")
    model = keras.Sequential([
        keras.layers.LSTM(128, activation='relu', input_shape=input_shape, return_sequences=True),
        keras.layers.LSTM(64, activation='relu'),
        keras.layers.Dense(96)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


def load_test_data(num_clients):
    logger.info("Loading test data...")
    x_test, y_test = [], []
    for i in range(num_clients):
        x_test.append(np_load(f'/results/client_data_{i}_test_features.npy'))
        y_test.append(np_load(f'/results/client_data_{i}_test_labels.npy'))
    return concatenate(x_test), concatenate(y_test)


if __name__ == "__main__":
    num_clients = int(os.environ.get('NUM_CLIENTS', 5))
    num_rounds = int(os.environ.get('NUM_ROUNDS', 3))
    logger.info(f"Number of clients: {num_clients}")
    x_test, y_test = load_test_data(num_clients)
    global_model = create_model((96, 1))

    def get_evaluate_fn():
        def evaluate(weights):
            global_model.set_weights(weights)
            loss, mae = global_model.evaluate(x_test, y_test, verbose=0)
            logger.info(f"Server evaluation finished. Loss: {loss}, MAE: {mae}")
            return loss, {"mae": mae}
        return evaluate

    strategy = fl_server.strategy.FedAvg(
        min_fit_clients=num_clients,
        min_available_clients=num_clients,
        eval_fn=get_evaluate_fn()
    )
    logger.info("Starting Flower server...")
    fl_server.start_server(
        server_address="0.0.0.0:8080",
        config={"num_rounds": num_rounds},
        strategy=strategy,
    )
    logger.info("Flower server finished.")
