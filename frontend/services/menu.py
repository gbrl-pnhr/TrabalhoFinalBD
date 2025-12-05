import pandas as pd
from services.api_client import get, post


def fetch_dishes():
    data = get("menu/dishes")
    if data:
        return pd.DataFrame(data)
    return pd.DataFrame()


def create_dish(name, price, category):
    payload = {"name": name, "price": price, "category": category}
    return post("menu/dishes", payload)
