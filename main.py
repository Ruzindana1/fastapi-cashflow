from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# Allow your WordPress site to access this API
origins = ["*"]  # For production, replace "*" with your WordPress domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load the dummy model
with open("cashflow_model.pkl", "rb") as f:
    model = pickle.load(f)

# Month mapping
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Pydantic model for POST requests
class CashflowRequest(BaseModel):
    months: list[int]  # e.g., [9, 10, 11]

@app.get("/")
def read_root():
    return {"message": "FastAPI Cashflow API is running!"}

@app.post("/predict_cashflow")
def predict_cashflow(request: CashflowRequest):
    """
    Predict cashflow for given months.
    Accepts POST JSON like:
    {
        "months": [9, 10, 11]
    }
    """

    month_indices = request.months

    # Validate month indices
    for m in month_indices:
        if m < 1 or m > 12:
            return {"error": f"Invalid month index {m}. Must be between 1 and 12."}

    # Prepare input for model
    input_data = pd.DataFrame({"month_index": month_indices})

    # Predict
    predictions = model.predict(input_data)

    # Build response
    response = []
    for m, pred in zip(month_indices, predictions):
        response.append({"month": MONTH_NAMES[m-1], "cashflow": float(pred)})

    return {"predictions": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}
