import requests
import hmac
import hashlib
import time

API_KEY = "DXqeIzPtAWMixHlUswGHHZqsebEQNpl11or91Dz5kSmdNARkMmOF4MAbVxbWij5A"
API_SECRET = "ulhFVxGGEkHVM1qY8UPtb9pYEjv4b8ftZWAtUDY24eDhBBxO1e0ZNf2MUCXz3ItZ"

BASE_URL = "https://api.binance.com"

def create_signature(params):
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_server_time():
    endpoint = "/api/v3/time"
    response = requests.get(BASE_URL + endpoint)
    if response.status_code == 200:
        return response.json()["serverTime"]
    else:
        raise Exception("Error fetching server time")

def get_account_balance(asset="USDT"):
    server_time = get_server_time()
    endpoint = "/api/v3/account"
    params = {"timestamp": server_time, "recvWindow": 60000}
    params["signature"] = create_signature(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(BASE_URL + endpoint, params=params, headers=headers)
    
    if response.status_code == 200:
        balances = response.json()["balances"]
        balance = next((item for item in balances if item["asset"] == asset), None)
        return float(balance["free"]) if balance else 0.0
    else:
        raise Exception(f"Error fetching account balance: {response.json()}")

def place_order(symbol, side, quantity):
    endpoint = "/api/v3/order"
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(BASE_URL + endpoint, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error placing order: {response.json()}")

def get_pepe_usdt_price():
    endpoint = "/api/v3/ticker/price"
    params = {"symbol": "PEPEUSDT"}
    
    response = requests.get(BASE_URL + endpoint, params=params)
    
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        raise Exception(f"Error fetching price: {response.json()}")
