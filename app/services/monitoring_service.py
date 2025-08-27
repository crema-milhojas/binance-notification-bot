import os
from typing import List
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
import requests
import math
from ..utils.telegram import send_message
from sqlalchemy.orm import Session
from ..config.db import SessionLocal
from ..models.arbitration_ustd import ArbitrationUstd


class MonitoringService:
     ROWS = 10
     SPREAD_EXPECTED = 0.0025

     session: Session = SessionLocal()

     def arbitration_ustd(self, trans_amount: int) -> List[ArbitrationUstdResponse]:
          print("\n")
          print("Obteniendo precios de COMPRA USDT")          
          buy_info = self.get_best_price('BUY', ["Yape", "Plin"], trans_amount)
          buy_price = buy_info["price"]
          buy_nickname = buy_info["nickname"]

          print("Obteniendo precios de VENTA USDT")
          sell_info = self.get_best_price('SELL', ["Yape", "Plin"], trans_amount)
          sell_price = sell_info["price"]
          sell_nickname = sell_info["nickname"]

          spread = round(sell_price - buy_price, 4)
          spread_pct = round((spread / buy_price) * 100, 2)

          last_arbitration_ustd = self.session.query(ArbitrationUstd).order_by(ArbitrationUstd.create_at.desc()).first()
          last_spread = None
          
          if(last_arbitration_ustd):
               last_spread = last_arbitration_ustd.spread

          if(spread >= self.SPREAD_EXPECTED and not math.isclose(spread, last_spread, abs_tol=1e-6)):
               message = (
                    f"💲 Monto mínimo: S/ {trans_amount}\n"
                    f"🟢 Mejor precio COMPRA USDT: S/ {buy_price} al usuario {buy_nickname}\n"
                    f"🔴 Mejor precio VENTA USDT: S/ {sell_price} al usuario {sell_nickname}\n"
                    f"💰 Spread: S/ {spread} ({spread_pct}%)"
               )
               # send_message(message)
               print("\n")
               print(message)

          new_arbitration_ustd = ArbitrationUstd(
               trans_amount = trans_amount,
               buy_price = buy_price,
               buyer_nickname = buy_nickname,
               sell_price = sell_price,
               seller_nickname= sell_nickname,
               spread = spread
          )

          try:
               self.session.add(new_arbitration_ustd)
               self.session.commit()
          except Exception as err:
               print(err)
          finally:
               self.session.close()

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
     
     

          