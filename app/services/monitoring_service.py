import os
from typing import List
from datetime import datetime
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
import requests
import math
from typing import List
from ..utils.telegram import send_message


class MonitoringService:
     ROWS = 10
     SPREAD_EXPECTED = 0.0025

     def arbitration_ustd(self, trans_amount: int) -> List[ArbitrationUstdResponse]:
          print("Obteniendo precios de COMPRA USDT")          
          buy_price = self.get_best_price('BUY', ["Yape", "Plin"], trans_amount)

          print("Obteniendo precios de VENTA USDT")
          sell_price = self.get_best_price('SELL', ["Yape", "Plin"], trans_amount)

          spread = round(sell_price - buy_price, 4)
          spread_pct = round((spread / buy_price) * 100, 2)

          if(spread >= self.SPREAD_EXPECTED):
               message = (
                    f"💲 Monto mínimo: S/ {trans_amount}\n"
                    f"🟢 Mejor precio COMPRA USDT: S/ {buy_price}\n"
                    f"🔴 Mejor precio VENTA USDT: S/ {sell_price}\n"
                    f"💰 Spread: S/ {spread} ({spread_pct}%)"
               )
               send_message(message)
               print("\n")
               print(message)

          return [
               ArbitrationUstdResponse(
                    response_code="00",
                    message="OK",
                    data={
                         "buy_price": buy_price, 
                         "sell_price": sell_price,
                         "spread": spread,
                    }
               )
          ]
     
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

          if(tradeType == "BUY"):
              max_price = min(
                    float(item["adv"]["price"])
                    for item in buyers_list
                    if "adv" in item and "price" in item["adv"]
               )
          elif(tradeType == "SELL"):
               max_price = max(
                    float(item["adv"]["price"])
                    for item in buyers_list
                    if "adv" in item and "price" in item["adv"]
               )
          else:
               raise Exception("Tipo de comercio no soportado")

         

          return max_price


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
     
     

          