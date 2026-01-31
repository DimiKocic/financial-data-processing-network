from kafka import KafkaConsumer, KafkaProducer
from json import dumps
import json


IN_TOPIC = "StockExchange"
OUT_TOPIC = "portfolios"


p11 = {
    "IBM": 1300,
    "AAPL": 2200,
    "FB": 1900,
    "AMZN": 2500,
    "GOOG": 1900,
    "AVGO": 2400,
}

p12 = {
    "VZ": 2900,
    "INTC": 2600,
    "AMD": 2100,
    "MSFT": 1200,
    "DELL": 2700,
    "ORKL": 1200,
}

portfolios = {"P11": p11, "P12": p12}


prev_evaluation = {"P11": 0, "P12": 0}

last_evaluated_date = {"P11": "", "P12": ""}

temp_dicts = {"P11": {}, "P12": {}}

kdszer = lambda x: x.decode('utf-8')
vdszer = lambda x: json.loads(x.decode('utf-8'))

# Initialize the Kafka consumer

consumer = KafkaConsumer(IN_TOPIC, bootstrap_servers=['localhost:9092'],
                         key_deserializer=kdszer,
                         value_deserializer=vdszer,
                         auto_offset_reset='earliest')

# Define lambda functions to serialize the key and value of the outgoing message

kszer = lambda x: x.encode('utf-8')
vszer = lambda x: dumps(x).encode('utf-8')

# Initialize the Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer=kszer,
                         value_serializer=vszer)


stock_prices = {}


def evaluate_portfolio(portfolio):
    total_value = 0
    for stock, qty in portfolio.items():
        price = stock_prices.get(stock)
        if price:
            total_value += price * qty
    return total_value

for msg in consumer:
    stock_data = msg.value
    stock_prices[stock_data["TICK"]] = float(stock_data["PRICE"])
    current_date = stock_data["TS"]

    for portfolio_name, portfolio in portfolios.items():
        if stock_data["TICK"] in portfolio:
            if current_date not in temp_dicts[portfolio_name]:
                temp_dicts[portfolio_name][current_date] = set()
            temp_dicts[portfolio_name][current_date].add(stock_data["TICK"])

            if temp_dicts[portfolio_name][current_date] == set(portfolio.keys()):
                current_evaluation = evaluate_portfolio(portfolio)
                diff = current_evaluation - prev_evaluation[portfolio_name]
                percent_diff = (diff / prev_evaluation[portfolio_name]) * 100 if prev_evaluation[portfolio_name] != 0 else 0
                result = {
                    "investor": "Inv1",
                    "portfolio": portfolio_name,
                    "date": current_date,
                    "value": current_evaluation,
                    "diff": diff,
                    "percent_diff": round(percent_diff, 2),
                }
                print(result)
                producer.send(OUT_TOPIC, key=portfolio_name, value=result)

                prev_evaluation[portfolio_name] = current_evaluation

                del temp_dicts[portfolio_name][current_date]