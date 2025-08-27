from typing import List
from datetime import datetime, timedelta
import numpy as np
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
from sqlalchemy.orm import Session
from ..config.db import SessionLocal
from ..models.arbitration_ustd import ArbitrationUstd
from ..utils.binance import Binance


class SwingTrading:
    session: Session
    binance: Binance
    BUY_ZONE_PRICE = 3.515
    SPREAD_EXPECTED = 0.0025
    TRANS_AMOUNT = 0

    def __init__(self):
        self.binance = Binance()
        self.session: Session = SessionLocal()

    def execute(self,)-> List[ArbitrationUstdResponse]:
        time_ago = datetime.utcnow() - timedelta(days=7)
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

        buy_info = self.binance.get_best_price('BUY', ["Yape", "Plin"], self.TRANS_AMOUNT)
        sell_info = self.binance.get_best_price('SELL', ["Yape", "Plin"], self.TRANS_AMOUNT)

        if buy_info['price'] <= best_buy_price:
            message = (
                    f"💲 Monto mínimo: S/ {self.TRANS_AMOUNT}\n"
                    f"🟢 Mejor precio COMPRA USDT: S/ {buy_info['price']} al usuario {buy_info['nickname']}\n"
            )
            print(message)

        spread = round(sell_info['price'] - self.BUY_ZONE_PRICE, 4)

        if spread >= self.SPREAD_EXPECTED:
            message = (
                    f"💲 Monto mínimo: S/ {self.TRANS_AMOUNT}\n"
                    f"🔴 Mejor precio VENTA USDT: S/ {sell_info['price']} al usuario {sell_info['nickname']}\n"
                    f"💰 Spread: S/ {spread}"
            )
            print(message)


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