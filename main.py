from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

# Allow your WordPress site to access this API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the dummy model
with open("cashflow_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def read_root():
    return {"message": "FastAPI Cashflow API is running!"}

@app.get("/predict_cashflow")
def predict_cashflow():
    # Dummy input for the next 3 months
    input_data = pd.DataFrame({"month_index": [9, 10, 11]})
    predictions = model.predict(input_data)

    month_names = ["September", "October", "November"]
    response = [{"month": m, "cashflow": float(c)} for m, c in zip(month_names, predictions)]
    return {"predictions": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}
