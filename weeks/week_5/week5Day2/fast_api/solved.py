import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
import uuid
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import pickle
import uvicorn

# Create a simple ML model for the exercise
iris = load_iris()
X = iris.data
y = iris.target
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model as a global variable for this exercise
iris_model = model
feature_names = iris.feature_names

# Define the input data model
class IrisFeatures(BaseModel):
    features: List[float]

    class Config:
        schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }
# TODO: Complete the code below to create a rate limiter
class RateLimiter:
    def __init__(self, requests_limit: int = 5, window_seconds: int = 60):
        # TODO: Initialize the rate limiter with empty request tracking
        self.rate_limiter={}
        self.requests_limit=requests_limit
        self.window_seconds=window_seconds

    def is_rate_limited(self, client_id: str) -> bool:
        # TODO: Check if the client has exceeded the rate limit
        if client_id in self.rate_limiter:
            if(rate_limiter[client_id]>=requests_limit):
              return True
            else:
              return False
        else:
          return None        

    def add_request(self, client_id: str) -> None:
        # TODO: Record a new request for the client
        if client_id in self.rate_limiter:
          rate_limiter.update({client_id,rate_limiter[client_id]+1})
        else:
          rate_limiter[client_id]=1


# Create the app and rate limiter
app = FastAPI(title="Iris Model API with Rate Limiting")
rate_limiter=RateLimiter()
# TODO: Initialize the rate limiter

# TODO: Implement the rate limiting dependency
async def check_rate_limit(request: Request):
      # Extract client IP or use a default for testing
    client_id=request.client.host
    rate_limiter.add_request(client_id)
    # Check if client is rate limited
    if(rate_limiter.is_rate_limited(client_id)):
      raise HTTPException(status_code=400, detail="Bad Request")
    else:
      print("Sab Fit hai boss")  

# PART 2: Implement performance tracking
# --------------------------------------
# Create a system to track prediction latency and model performance

# TODO: Complete the code below to track performance metrics
performance_metrics = {
    # TODO: Initialize performance metrics dictionary
    'prediction_count':0,
    'response_time':0.0
}

# TODO: Implement the function to update performance metrics
async def update_metrics(features, prediction, response_time):
    # TODO: Update the performance metrics with the new prediction data
    performance_metrics['prediction_count']=len(prediction)
    performance_metrics['response_time']=response_time

# PART 3: Create the prediction endpoint
# --------------------------------------
# Implement the prediction endpoint with rate limiting and performance tracking

@app.post("/predict")
async def predict(iris_data: IrisFeatures, request: Request, rate_limit: None = Depends(check_rate_limit)):
  

    # TODO: Implement the prediction endpoint
    # 1. Record start time
    start_time=time.time()
    # 2. Make prediction
    features = np.array(iris_data.features).reshape(1, -1)
    predictions=model.predict(features).tolist()
    # 3. Calculate response time
    response_time=time.time()-start_time
    # 4. Update metrics
    update_metrics(features,prediction,response_time)
    # 5. Return prediction response
    return prediction


# PART 4: Create a dashboard endpoint
# -----------------------------------
# Implement an endpoint to display performance metrics

@app.get("/dashboard")
async def dashboard():
    return performance_metrics

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)