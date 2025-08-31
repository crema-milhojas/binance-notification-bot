from typing import List
from datetime import datetime, timedelta
import numpy as np
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..config.db import SessionLocal
from ..models.arbitration_ustd import ArbitrationUstd
from ..utils.binance import Binance
from ..utils.telegram import send_message
import math
import time


class SwingTrading:
    session: Session
    binance: Binance
    SPREAD_EXPECTED = 0.0025

    def __init__(self,):
        self.binance = Binance()
        self.session: Session = SessionLocal()

    def execute(self, trans_amount: int)-> List[ArbitrationUstdResponse]:
        start = time.time()
        time_ago = datetime.utcnow() - timedelta(days=3)
        last_buy_price = None
        last_sell_price = None

        recent_arbitrations = (
            self.session.query(ArbitrationUstd)
            .filter(ArbitrationUstd.create_at >= time_ago)
            .order_by(ArbitrationUstd.create_at.desc())
            .all()
        )
                     
        recent_arbitrations_list = [a.as_dict() for a in recent_arbitrations]

        buyPriceList = []
        sellPriceList = []

        for arbitration in recent_arbitrations_list:
            buyPriceList.append(float(arbitration.get("buy_price")))
            sellPriceList.append(float(arbitration.get("sell_price")))

        best_buy_price = self.best_buy_price(buyPriceList)
        best_sell_price = self.best_sell_price(sellPriceList)

        last_arbitration_ustd = self.session.query(ArbitrationUstd).order_by(ArbitrationUstd.create_at.desc()).first()

        if(last_arbitration_ustd):
            last_buy_price = last_arbitration_ustd.buy_price
            last_sell_price = last_arbitration_ustd.sell_price

        buy_zone_prices = self.session.execute(text("SELECT * FROM v_latest_buy_zone")).mappings()
        list_buy_zone_prices = list(buy_zone_prices)   

        buy_info = self.binance.get_best_price('BUY', ["Yape", "Plin"], trans_amount)            
        sell_info = self.binance.get_best_price('SELL', ["Yape", "Plin"], trans_amount)

        enable_to_notify_buy = not math.isclose(buy_info['price'], last_buy_price, abs_tol=1e-6)        
                
        if buy_info['price'] <= best_buy_price and enable_to_notify_buy:
            message = (
                    f"💲 Monto mínimo: S/ {trans_amount}\n"
                    f"🟢 Mejor precio COMPRA USDT: S/ {buy_info['price']} al usuario {buy_info['nickname']}\n"
            )
            print(message)
            print("\n")
            send_message(message)        

        for buy_zone_price in list_buy_zone_prices:            
            buy_price = float(buy_zone_price["buy_price"])
            spread = round(sell_info['price'] - buy_price, 4)

            enable_to_notify_sell = not math.isclose(sell_info['price'], last_sell_price, abs_tol=1e-6)

            if spread >= self.SPREAD_EXPECTED and enable_to_notify_sell:
                message = (
                        f"💲 Monto mínimo: S/ {trans_amount}\n"
                        f"🟢 Precio guardado de COMPRA USDT: S/ {buy_price}\n"
                        f"🔴 Mejor precio VENTA USDT: S/ {sell_info['price']} al usuario {sell_info['nickname']}\n"
                        f"💰 Spread: S/ {spread}"
                )
                print(message)
                print("\n")
                send_message(message)
                
        new_arbitration_ustd = ArbitrationUstd(
            trans_amount = trans_amount,
            buy_price = buy_info['price'],
            buyer_nickname = buy_info['nickname'],
            sell_price = sell_info['price'],
            seller_nickname= sell_info['nickname'],
            spread = round(sell_info['price'] - buy_info['price'], 4)
        )

        try:
            self.session.add(new_arbitration_ustd)
            self.session.commit()
        except Exception as err:
            print(err)
        finally:
            self.session.close()

        end = time.time()
        duration = end - start
        print(f"SwingTrading.execute terminó en {duration:.2f} segundos")
        
        return [
            ArbitrationUstdResponse(
                response_code="00",
                message="OK",
                data= {
                    "best_buy_price": best_buy_price,
                    "best_sell_price": best_sell_price,
                    "current_buy": buy_info['price']
                }              
            )
        ]
    
    def best_buy_price(self, priceList: List[float]):
        p25_buy = np.percentile(priceList, 25)
        return p25_buy

    def best_sell_price(self, priceList: List[float]):
        p75_buy = np.percentile(priceList, 75)
        return p75_buy