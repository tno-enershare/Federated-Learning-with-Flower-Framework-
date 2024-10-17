#![logo_Enershare-300x88](https://github.com/user-attachments/assets/3acef38f-45d5-4bf5-9142-08c73d73718f)
 Federated Learning with Flower Framework in Docker

## Project Description

This project demonstrates a federated learning setup using the Flower framework. It involves preparing data, setting up a federated server, deploying multiple clients, and collecting predictions. The entire workflow is containerized using Docker.

## Files and Directories

- **dataset/**: Contains scripts and Dockerfile for data preparation.
- **server/**: Contains the Flower server script and Dockerfile.
- **client/**: Contains the Flower client script and Dockerfile.
- **results/**: Contains scripts and Dockerfile for collecting predictions.
- **docker-compose.yml**: Docker Compose configuration file.
- **.env**: Environment file to set dynamic variables like `NUM_CLIENTS`.

- **web_app**: Contains a web server that can serve requests for simulation results.

## Running the Project

### Important Note

Runtime takes a long time when you use a high number of clients, so make sure to define the number of clients NUM_CLIENTS<=4 (ideally 3 clients)

### Prerequisites

- Ensure Docker and Docker Compose are installed on your system.

### Step 1: Set Up Environment Variables

You can define the number of clients dynamically using a `.env` file or directly in the command line via:  `NUM_CLIENTS=n docker-compose up --build` (n being the number of clients)
or using `export NUM_CLIENT=n`.

#### Using a `.env` File

Create a file named `.env` in the project root with the following content:
`NUM_CLIENTS=n`

### Step 2: Build Docker Images

Build the Docker images for all services:
`docker-compose build`

### Step 3: Run Docker Compose

Start the containers using Docker Compose:

`docker-compose up`

## Notes

- Data Preparation: The prepare_data service will prepare the data and save it in the results directory.

- Server Startup: The server service will start the Flower server and wait for clients to connect.

- Client Execution: The client service will start multiple clients based on the NUM_CLIENTS environment variable.

- Prediction Collection: The collect_predictions service will start after the client service has completed, collecting predictions from all clients.

## Important Commands

- Build Docker Images: `docker-compose build`
- Start Services: `docker-compose up`
- Stop Services: `docker-compose down`

## Example Output

When you run the project, you should see logs indicating the progress of data preparation, server startup, client training, and prediction collection.

### Troubleshooting

Ensure Docker and Docker Compose are correctly installed.
Check that the NUM_CLIENTS environment variable is set correctly.
Monitor the logs for any errors using: `docker-compose logs -f`.
