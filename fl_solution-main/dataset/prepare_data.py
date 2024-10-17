import logging
import os

from numpy import array as np_array, save as np_save
from pandas import DatetimeIndex, read_csv
from sklearn.preprocessing import MinMaxScaler

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_features_and_labels(data, look_back=96, predict_ahead=96):
    features, labels = [], []
    for i in range(len(data) - look_back - predict_ahead + 1):
        features.append(data[i:i + look_back])
        labels.append(data[i + look_back:i + look_back + predict_ahead])
    return np_array(features), np_array(labels)


def load_and_prepare_data(num_clients):
    file_path = 'Slovenia_Consumers_15min_2021_2022_Anonymized_WithTimestamp.csv'
    data = read_csv(file_path, sep=';', low_memory=False)

    data['Time'] = data['Time'].astype('datetime64[s]')
    data = data.set_index(DatetimeIndex(data['Time']))
    data.set_index('Time', inplace=True)
    cols = data.columns  # COMMENT THIS PART when working pv data

    data[cols] = data[cols].apply(lambda x: x.str.replace(',', '.')).astype(float)

    scaler = MinMaxScaler()
    client_datasets = []

    columns = ['USER1EDEMAND', 'USER2EDEMAND', 'USER3EDEMAND', 'USER4EDEMAND', 'USER5EDEMAND']
    total_columns = len(columns)

    for i in range(num_clients):
        column = columns[i % total_columns]
        scaled_data = scaler.fit_transform(data[column].values.reshape(-1, 1))
        features, labels = create_features_and_labels(scaled_data)
        train_size = int(len(features) * 0.8)
        x_train, x_test = features[:train_size], features[train_size:]
        y_train, y_test = labels[:train_size], labels[train_size:]
        client_datasets.append((x_train, y_train, x_test, y_test, scaled_data[-96:]))

    return client_datasets


if __name__ == "__main__":
    num_clients = int(os.environ.get('NUM_CLIENTS', 5))
    logger.info(f"Preparing data for {num_clients} clients...")
    datasets = load_and_prepare_data(num_clients)
    for i, (x_train, y_train, x_test, y_test, last_day_data) in enumerate(datasets):
        np_save(f'/results/client_data_{i}_features.npy', x_train)
        np_save(f'/results/client_data_{i}_labels.npy', y_train)
        np_save(f'/results/client_data_{i}_test_features.npy', x_test)
        np_save(f'/results/client_data_{i}_test_labels.npy', y_test)
        np_save(f'/results/client_data_{i}_last_day.npy', last_day_data)
    logger.info("Data preparation finished.")
