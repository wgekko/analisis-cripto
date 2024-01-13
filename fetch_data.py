# datos
import requests
from datetime import datetime

def get_binance_data(symbol, interval, limit):
    base_url = "https://api.binance.com"
    endpoint = "/api/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(base_url + endpoint, params=params)
    data = response.json()
    return data

# Extract the data

def data_extract(data):
    dates = [datetime.fromtimestamp(entry[0] / 1000) for entry in data]
    popen = [float(entry[1]) for entry in data]
    phigh = [float(entry[2]) for entry in data]
    plow = [float(entry[3]) for entry in data]
    pclose = [float(entry[4]) for entry in data]  
    return dates, popen, phigh, plow, pclose


    