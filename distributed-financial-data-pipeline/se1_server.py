from kafka import KafkaProducer
from json import dumps
import time
import random
import datetime
import holidays


stock_exchange_holidays = holidays.US(years=range(2000, datetime.date.today().year + 1), observed=True)

stock1 = [
    ('IBM', 128.25), ('AAPL', 151.60), ('FB', 184.51), ('AMZN', 93.55),
    ('GOOG', 93.86), ('META', 184.51), ('MSI', 265.96), ('INTC', 25.53),
    ('AMD', 82.11), ('MSFT', 254.15), ('DELL', 38.00), ('ORKL', 88.36)
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
    weekends = [5, 6]
    return (date.weekday() not in weekends) and (date not in stock_exchange_holidays)

date_iter = start_date
while date_iter < current_date:
    if is_trading_day(date_iter):
        # For each stock, generate a random price and create a message
        # to send to the Kafka topic
        for s in stock1:
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

producer.flush() 
producer.close()