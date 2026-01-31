# Distributed Financial Data Processing Network (Kafka + Spark + MySQL)

End-to-end data engineering project simulating stock exchanges and institutional investors using Apache Kafka, MySQL, and Apache Spark.

The system streams daily stock prices, evaluates multiple investor portfolios in real time, persists results in a relational database, and performs historical analytics using Spark.

This project demonstrates practical streaming architectures, distributed processing, and analytics pipelines.

---

## Architecture Overview

Pipeline:

Stock Exchanges → Kafka (StockExchange topic) → Investors → Kafka (portfolios topic) → MySQL → Spark Analytics

### Components

1. Two Stock Exchange servers generate daily stock prices and publish them to Kafka.
2. Three Institutional Investors consume stock prices, evaluate portfolios, and publish portfolio valuations.
3. A database application initializes MySQL and creates investor/portfolio tables.
4. A Kafka consumer ingests portfolio evaluations into MySQL.
5. A Spark application reads MySQL tables and generates portfolio statistics.

---

## Repository Structure

├── se1_server.py # Stock Exchange Server 1 (first 12 stocks)
├── se2_server.py # Stock Exchange Server 2 (remaining stocks)
├── inv1.py # Investor 1 (P11, P12)
├── inv2.py # Investor 2 (P21, P22)
├── inv3.py # Investor 3 (P31, P32)
├── investorsDB.py # MySQL database initialization
├── app1.py # Kafka → MySQL ingestion (portfolio results)
├── app2.py # Spark analytics + statistics generation
├── Inv1_P11_stats.json # Example Spark output
├── Inv1_P12_stats.json
└── README.md


---

## Technologies Used

- Apache Kafka – real-time streaming
- Apache Spark – distributed analytics
- MySQL – persistent storage
- Python – orchestration and processing

---

## What the System Does

### Stock Exchanges

`se1_server.py` and `se2_server.py` simulate daily trading starting from January 1, 2000.  
Each trading day emits JSON messages to Kafka topic `StockExchange` with:

- Ticker symbol
- Closing price
- Date

Trading days exclude weekends and holidays, with a 2-second delay per simulated day.

---

### Institutional Investors

`inv1.py`, `inv2.py`, and `inv3.py`:

- Consume stock prices from Kafka
- Maintain two portfolios per investor
- Evaluate portfolios once all required stock prices for a day are received
- Compute:
  - Portfolio value
  - Daily change
  - Percentage change
- Publish results to Kafka topic `portfolios`

---

### Database Initialization

`investorsDB.py`:

- Creates MySQL database `InvestorsDB`
- Creates Investors, Portfolios, and mapping tables
- Creates per-portfolio tables (e.g., Inv1_P11, Inv2_P22)
- Initializes investors and portfolio relationships

---

### Portfolio Persistence

`app1.py`:

- Consumes from Kafka topic `portfolios`
- Inserts portfolio evaluations into corresponding MySQL tables

---

### Spark Analytics

`app2.py`:

- Reads portfolio tables from MySQL
- Computes:
  - Global max/min daily change and percentage
  - Yearly max/min statistics
  - Average portfolio value
  - Standard deviation of portfolio value
- Outputs results to JSON files such as `Inv1_P11_stats.json`

---

## How to Run

### Prerequisites

- Python 3.8+
- Apache Kafka (running on localhost:9092)
- Apache Spark
- MySQL Server
- MySQL Connector JAR for Spark

---

### Start Kafka

Start Zookeeper and Kafka, then create topics:

```bash
kafka-topics.sh --create --topic StockExchange --bootstrap-server localhost:9092
kafka-topics.sh --create --topic portfolios --bootstrap-server localhost:9092

```

## How to Run the System (6 Steps)
## Step 1 – Start Kafka and Create Topics

Make sure Zookeeper and Kafka are running, then create the required topics:

kafka-topics.sh --create --topic StockExchange --bootstrap-server localhost:9092
kafka-topics.sh --create --topic portfolios --bootstrap-server localhost:9092

## Step 2 – Initialize the MySQL Database

This creates InvestorsDB, all core tables, and the per-portfolio tables:

python investorsDB.py

## Step 3 – Start Portfolio Ingestion (Kafka → MySQL)

This service listens to the portfolios topic and continuously writes results into MySQL:

python app1.py


Leave this running.

## Step 4 – Start the Institutional Investors

Each investor consumes stock prices and publishes portfolio evaluations.

Run each in a separate terminal:

python inv1.py
python inv2.py
python inv3.py

## Step 5 – Start the Stock Exchange Servers

These simulate historical trading and publish stock prices to Kafka.

Run both in separate terminals:

python se1_server.py
python se2_server.py


At this point, data starts flowing through the full pipeline.

## Step 6 – Run Spark Analytics

After portfolio data has accumulated in MySQL, generate historical statistics:

spark-submit app2.py


This produces JSON files such as Inv1_P11_stats.json and Inv1_P12_stats.json with portfolio analytics.
