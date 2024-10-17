from pathlib import Path
from typing import Dict, Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4


app = FastAPI(
    title="Federated learning Module for Energy Consumption Prediction",
    name="A federated learning module for predicting energy consumption data produced.",
    description="A federated learning module for energy consumption data produced in the EU Enershare project.",
    version="0.2.0-oas3.1",
    license="MIT",
)

run_dict: Dict[str, Dict] = {"test": {"run_id": "test", "ready": "False"}}

THE_FOLDER = Path("../results")
# For now the input and result is fixed.
THE_RESULT_PATH = THE_FOLDER / "predictions.csv"
THE_INPUT_FILE = THE_FOLDER / "input.csv"


def get_result_file_for(run_id: str):
    if not Path.exists(THE_RESULT_PATH):
        return None
    return THE_RESULT_PATH


def get_input_file_for(run_id: str):
    if not Path.exists(THE_INPUT_FILE):
        return None
    return THE_INPUT_FILE


@app.get("/", name="Test endpoint",
         description="Test endpoint for health checks.")
def health():
    return {"Hello": "World"}


@app.get("/simulation_runs", name="Simulation runs",
         description="Returns the identifiers and statuses for the started runs, details can be found using this id.")
def get_all_runs():
    return run_dict


@app.get("/simulation_runs/{run_id}", name="Simulation run status",
         description="Endpoint to check if the run status, if it is ready or not.")
def show_run(run_id: str):
    if run_id not in run_dict:
        raise HTTPException(status_code=404, detail="Run ID not found")
    status = get_result_file_for(run_id) is not None
    return {"run_id": run_id, "no_clients": run_dict.get("no_clients", 2), "ready": str(status)}


@app.post("/simulation_runs", name="Start simulation run",
          description="Start a run to predict energy consumption data, with optionally specifying the number of clients to use in the federated learning process (default is 2).")
def start_run(no_clients: Union[int, None] = None):
    new_uuid = str(uuid4())
    run_dict[new_uuid] = {"run_id": new_uuid, "no_clients": no_clients}
    return {"run_id": new_uuid}


@app.get("/simulation_runs/{run_id}/result", name="Simulation run result",
         description="Get the result CSV of a run with the predicted energy consumption data.")
def download_run_result(run_id: str):
    if run_id not in run_dict:
        raise HTTPException(status_code=404, detail="Run ID not found")
    result_path = get_result_file_for(run_id)
    if result_path is None:
        raise HTTPException(status_code=400, detail=f"Run result is not ready for run {run_id}")
    response = FileResponse(filename=f"predictions-{run_id}", path=result_path, media_type="text/csv")
    return response


@app.get("/simulation_runs/{run_id}/input_file", name="Simulation run input file",
         description="Returns the used input CSV for a given simulation run. Warning: this can be a big file (~50MB).")
def download_run_input(run_id: str):
    if run_id not in run_dict:
        raise HTTPException(status_code=404, detail="Run ID not found")
    input_path = get_input_file_for(run_id)
    if input_path is None:
        raise HTTPException(status_code=400, detail="Run input is not ready")
    response = FileResponse(filename=f"input-{run_id}", path=input_path, media_type="text/csv")
    return response
