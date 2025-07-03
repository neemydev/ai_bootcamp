
import requests


# Example features for Iris dataset (sepal length, sepal width, petal length, petal width)
example_features = [5.1, 3.5, 1.4, 0.2]  # Example of Iris setosa

# The following would work if the Flask server was running
response = requests.post('http://127.0.0.1:5000/predict',
                        json={'features': example_features})
print(response)