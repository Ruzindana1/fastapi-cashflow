from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your WordPress site to access this API
origins = ["*"]  # For security, replace "*" with your WordPress domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Root route for testing if the app is live
@app.get("/")
def read_root():
    return {"message": "FastAPI Cashflow API is running!"}

# Predict cashflow route
@app.get("/predict_cashflow")
def predict_cashflow():
    # Example static data; later we will replace this with real ML predictions
    return {
        "predictions": [
            {"month": "September", "cashflow": 1200},
            {"month": "October", "cashflow": 1450},
            {"month": "November", "cashflow": 1600}
        ]
    }

# Optional: Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}
