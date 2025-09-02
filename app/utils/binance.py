import os
import requests
from typing import List
import math

class Binance:
    ROWS = 10

    def get_best_price(self, tradeType: str, payTypes: str, transAmount: int):
        buyers_list = []

        def fetch_page(page: int) -> dict:
            return self.search_p2p_binance(page, tradeType, payTypes, transAmount)

        first_response = fetch_page(1)
        buyers_list.extend(first_response.get("data", []))

        total_items = first_response.get("total", 0)
        total_pages = math.ceil(total_items / self.ROWS)

        for page in range(2, total_pages + 1):
            response = fetch_page(page)
            buyers_list.extend(response.get("data", []))
        
        print(f"Número de precios encontrados: {len(buyers_list)}")

        price_and_advertiser = [
            (float(item["adv"]["price"]), item["advertiser"]["nickName"])
            for item in buyers_list
            if "adv" in item and "price" in item["adv"] and "advertiser" in item and "nickName" in item["advertiser"]
        ]

        if(tradeType == "BUY"):
            price, nickname = min(price_and_advertiser, key=lambda x: x[0])
            return {"price": price, "nickname": nickname}

        elif(tradeType == "SELL"):
            price, nickname = max(price_and_advertiser, key=lambda x: x[0])
            return {"price": price, "nickname": nickname}
        else:
            raise Exception("Tipo de comercio no soportado")

    def search_p2p_binance(self, page: int, tradeType: str, payTypes: List[str], transAmount: int = None) -> dict:
        url = os.environ.get("URL_BINANCE")
        payload = {
            "asset": "USDT",
            "fiat": "PEN",
            "page": page,
            "rows": self.ROWS,
            "tradeType": tradeType,
            "payTypes": payTypes,
            "publisherType": None,
            "publisherType": "merchant",
            "transAmount": transAmount
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json() 
    