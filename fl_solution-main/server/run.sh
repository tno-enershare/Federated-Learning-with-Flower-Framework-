#!/bin/bash
num_clients=${NUM_CLIENTS:-5}
python server.py $num_clients
sleep 10  # Wait for 10 seconds to ensure the server is ready
