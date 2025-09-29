from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request
# Directly load the pickle
MODEL_PATH = r"models/rf_model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="MLOps Capstone Model API")
# Configure logging
logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InputData(BaseModel):
    features: list  # Example: [5.1, 3.5, 1.4, 0.2]


# Log validation errors globally
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logging.error(f"ERROR - Validation failed - Input: {body} - {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": exc.errors()},
    )

@app.get("/")
def root():
    return {"message": "MLOps Capstone API is running!"}

@app.post("/predict")
def predict(data: InputData):
    try:
        X = pd.DataFrame([data.features])
        prediction = model.predict(X)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}
