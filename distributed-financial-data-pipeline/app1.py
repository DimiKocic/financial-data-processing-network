import json
import mysql.connector
from kafka import KafkaConsumer

# Define Kafka topic name
IN_TOPIC = "portfolios"

# Establish database connection
connection = mysql.connector.connect(
    host="localhost",
    user="itc6107",
    password="itc6107",
    database="InvestorsDB"
)
cursor = connection.cursor()

# Define Kafka deserialization functions
kdszer = lambda x: x.decode('utf-8')  # Decode message keys from bytes to strings
vdszer = lambda x: json.loads(x.decode('utf-8'))  # Convert message values from JSON format

# Initialize Kafka consumer
consumer = KafkaConsumer(
    IN_TOPIC,
    bootstrap_servers=['localhost:9092'],
    key_deserializer=kdszer,
    value_deserializer=vdszer,
    auto_offset_reset='earliest'
)

# Function to store portfolio details in the database
def insert_portfolio_data(investor, portfolio, date, evaluation, diff, percent_diff):
    table_name = f"{investor}_{portfolio}"
    diff = 'NULL' if diff is None else diff  # Handle NULL values for change amount
    percent_diff = 'NULL' if percent_diff is None else percent_diff  # Handle NULL values for percentage change

    cursor.execute(f"""
        INSERT INTO {table_name} (As_Of, Evaluation, Daily_Evaluation_Change, Daily_Evaluation_Change_Percentage)
        VALUES ('{date}', {evaluation}, {diff}, {percent_diff})
    """)
    connection.commit()  # Save changes to the database

# Read messages from Kafka and process them
for msg in consumer:
    data = msg.value
    investor = data['investor']
    portfolio = data['portfolio']
    date = data['date']
    evaluation = data['value']
    diff = data['diff']
    percent_diff = data['percent_diff']

    insert_portfolio_data(investor, portfolio, date, evaluation, diff, percent_diff)
    print(f"Inserted data for {investor} {portfolio}")
