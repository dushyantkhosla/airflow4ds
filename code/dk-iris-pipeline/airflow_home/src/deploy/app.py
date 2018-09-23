#!flask/bin/python
from flask import Flask, jsonify, request
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)

@app.route('/isAlive')
def status():
    """
    """
    return 1


@app.route('/')
def hi():
    """
    """
    return "Welcome to the IRIS Prediction Model!"

@app.route('/api', methods=['POST'])
def predict():
    """
    """
    lr = joblib.load('models/logistic.pkl')
    dt = joblib.load('models/tree.pkl')

    dict_iris_type = {
        0: 'setosa',
        1: 'versicolor',
        2: 'virginica'
    }

    query = request.get_json(force=True)

    X_te = np.array([[
        query.get('sl'),
        query.get('sw'),
        query.get('pl'),
        query.get('pw')
    ]])

    y_pr = lr.predict(X_te) if query.get('algo') == 'lr' else dt.predict(X_te)
    output = dict_iris_type.get(y_pr.item())

    return jsonify(iris_type=output, model=query.get('algo'))

if __name__ == '__main__':
     app.run(port=5000, host='0.0.0.0')
