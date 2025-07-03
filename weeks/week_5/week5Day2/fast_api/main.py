


from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from typing import List, Dict, Any, Optional
import numpy as np
import pickle

# Define data model for API input
class IrisFeatures(BaseModel):
    features: List[float]

    class Config:
        schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }


# Define data model for API output
class PredictionResponse(BaseModel):
    prediction: List[int]
    probability: List[List[float]]
    feature_importance: Optional[Dict[str, float]] = None


# Create FastAPI app
app_fastapi = FastAPI(
    title="Iris Classifier API",
    description="API for classifying iris flowers using a RandomForest model",
    version="1.0.0"
)


# Load the model at startup
model = load_model()

@app_fastapi.post("/predict", response_model=PredictionResponse)
async def predict_iris(iris_data: IrisFeatures):
    try:
        # Convert input features to numpy array
        features = np.array(iris_data.features).reshape(1, -1)

        # Make predictions
        prediction = model.predict(features).tolist()
        prediction_proba = model.predict_proba(features).tolist()

        # Get feature importance
        feature_importance = {}
        if hasattr(model, 'feature_importances_'):
            for i, importance in enumerate(model.feature_importances_):
                feature_name = feature_names[i] if i < len(feature_names) else f"feature_{i}"
                feature_importance[feature_name] = float(importance)

        return {
            "prediction": prediction,
            "probability": prediction_proba,
            "feature_importance": feature_importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app_fastapi.get("/health")
async def health_check():
    return {"status": "healthy"}



# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app_fastapi", host="0.0.0.0", port=8000, reload=True)
