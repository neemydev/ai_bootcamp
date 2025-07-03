# Import necessary libraries for Flask
import flask
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
def create_model():
    # Load iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Train a simple RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return model, iris.feature_names

# Create and save the model
model, feature_names = create_model()