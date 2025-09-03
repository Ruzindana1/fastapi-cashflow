from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

# Allow your WordPress site to access this API
origins = ["*"]  # For production, replace "*" with your WordPress domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
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

@app.get("/")
def read_root():
    return {"message": "FastAPI Cashflow API is running!"}

@app.get("/predict_cashflow")
def predict_cashflow(months: str = Query("9,10,11", description="Comma-separated month indices, 1-12")):
    """
    Predict cashflow for given months.
    Example: /predict_cashflow?months=9,10,11
    """

    # Parse months from query parameter
    try:
        month_indices = [int(m) for m in months.split(",")]
    except ValueError:
        return {"error": "Invalid month indices. Must be comma-separated integers 1-12."}

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
