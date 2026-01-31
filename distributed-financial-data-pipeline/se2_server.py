from kafka import KafkaProducer
from json import dumps
import time
import random
import datetime
import holidays


stock_exchange_holidays = holidays.US(years=range(2000, datetime.date.today().year + 1), observed=True)

stock2 = [
    ('HPQ', 27.66), ('CSCO', 48.91), ('ZM', 69.65), ('QCOM', 119.19),
    ('ADBE', 344.80), ('VZ', 37.91), ('TXN', 172.06), ('CRM', 182.32),
    ('AVGO', 625.15), ('NVDA', 232.88), ('VMW', 120.05), ('EBAY', 43.98)
]

KAFKA_TOPIC = "StockExchange"
start_date = datetime.date(2000, 1, 1)
current_date = datetime.date.today()

kszer = lambda x: x.encode('utf-8')
vszer = lambda x: dumps(x).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer=kszer,
                         value_serializer=vszer)

def is_trading_day(date):
    """Check if a given date is a trading day (not a weekend or a stock exchange holiday)."""
    weekends = [6, 7]
    return (date.weekday() not in weekends) and (date not in stock_exchange_holidays)

date_iter = start_date
while date_iter < current_date:
    if is_trading_day(date_iter):
        for s in stock2:
            ticker, price = s
            r = random.random() / 10 - 0.05
            price *= 1 + r
            msg = {
                'TICK': ticker,
                'PRICE': f"{price:.2f}",
                'TS': str(date_iter)
            }
            print(msg)
            producer.send(KAFKA_TOPIC, key=ticker, value=msg)
        time.sleep(2)
    date_iter += datetime.timedelta(days=1)

