import requests
import json

def get_prediction(ser, model, url):
    """
    """
    data = ser.to_dict()
    data['algo'] = model

    r = requests.post(url, json.dumps(data))

    return json.loads(r.text)
