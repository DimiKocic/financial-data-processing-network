# Distributed Financial Data Processing Network (Kafka + Spark + MySQL)

End-to-end data engineering system simulating stock exchanges and institutional investors using Apache Kafka, MySQL, and Apache Spark.

The project demonstrates a full streaming analytics workflow:

- real-time market data ingestion  
- distributed portfolio evaluation  
- persistent storage in relational databases  
- historical analytics using Spark  

It models realistic financial data pipelines and multi-service architectures.

---

## Problem Statement

Financial systems require continuous ingestion of market data, near–real-time portfolio evaluation, and historical analytics.

This project simulates such an environment by building a distributed network of:

- stock exchanges  
- institutional investors  
- streaming infrastructure  
- persistent databases  
- analytics engines  

The goal is to demonstrate how raw market events flow through Kafka, are processed by multiple consumers, stored in MySQL, and analyzed with Spark.

---

## System Overview

The pipeline operates as:

Stock Exchanges → Kafka (`StockExchange`) → Investors → Kafka (`portfolios`) → MySQL → Spark Analytics

---

### 1. Stock Exchange Simulation (`se1_server.py`, `se2_server.py`)

Two independent stock exchange servers simulate historical trading starting from January 1, 2000.

Features:

- emit daily closing prices for multiple stocks  
- skip weekends and holidays  
- simulate passage of time (2-second delay per trading day)  
- publish JSON messages to Kafka topic `StockExchange`  

These services act as the data producers driving the system.

---

### 2. Institutional Investors (`inv1.py`, `inv2.py`, `inv3.py`)

Three investor services consume market data and evaluate portfolios in real time.

Each investor:

- manages two portfolios  
- waits until all required stock prices for a given day are received  
- computes:
  - portfolio value  
  - daily change  
  - percentage change  
- publishes results to Kafka topic `portfolios`  

This layer represents distributed business logic operating on streaming data.

---

### 3. Database Initialization (`investorsDB.py`)

Initializes the persistent storage layer by:

- creating MySQL database `InvestorsDB`  
- creating Investors and Portfolios tables  
- establishing investor–portfolio mappings  
- generating individual tables per portfolio (e.g., `Inv1_P11`)  

This prepares the schema for downstream ingestion and analytics.

---

### 4. Portfolio Persistence (`app1.py`)

Consumes portfolio evaluations from Kafka and inserts them into MySQL.

Responsibilities:

- listens to topic `portfolios`  
- routes each record to the appropriate portfolio table  
- continuously persists streaming results  

This component bridges streaming data with relational storage.

---

### 5. Spark Analytics (`app2.py`)

Reads portfolio tables from MySQL and generates historical statistics.

Computed metrics include:

- global max/min daily changes  
- yearly max/min changes  
- average portfolio values  
- standard deviation of evaluations  

Results are exported as JSON files (e.g., `Inv1_P11_stats.json`) for inspection.

---

## Project Structure

```text
financial-data-processing-network/
├── se1_server.py        # Stock Exchange Server 1
├── se2_server.py        # Stock Exchange Server 2
├── inv1.py              # Investor 1 (P11, P12)
├── inv2.py              # Investor 2 (P21, P22)
├── inv3.py              # Investor 3 (P31, P32)
├── investorsDB.py       # MySQL schema initialization
├── app1.py              # Kafka → MySQL ingestion
├── app2.py              # Spark analytics
├── Inv1_P11_stats.json  # Example analytics output
├── Inv1_P12_stats.json
└── README.md
```

## How to Run

The system runs as a coordinated set of services. Each component depends on the previous one, so follow the steps below in order.

---

### Step 1 – Kafka Infrastructure Setup

Start Zookeeper and Kafka locally, then create two topics:

- `StockExchange` – receives market data from stock exchanges  
- `portfolios` – receives evaluated portfolio results from investors  

```bash
kafka-topics.sh --create --topic StockExchange --bootstrap-server localhost:9092
kafka-topics.sh --create --topic portfolios --bootstrap-server localhost:9092
```

## Step 2 – Initialize the Database

- Run the database initialization script to create InvestorsDB, all schema tables, investor–portfolio mappings, and individual portfolio tables:
  
```bash
python investorsDB.py
```

This prepares the persistent storage layer.

## Step 3 – Start Portfolio Persistence Service

- Launch the Kafka consumer that listens to portfolio evaluations and inserts them into MySQL:

```bash
python app1.py
```

Leave this service running.

## Step 4 – Start Institutional Investors

Run each investor in a separate terminal. These services consume stock prices and publish portfolio valuations:

```bash
python inv1.py
python inv2.py
python inv3.py
```

## Step 5 – Start Stock Exchange Simulators

Run both stock exchange servers in separate terminals. These simulate historical trading and stream daily stock prices:

```bash
python se1_server.py
python se2_server.py
```

At this point, data begins flowing through the full pipeline.

## Step 6 – Run Spark Analytics

After portfolio data has accumulated in MySQL, execute the Spark analytics job to generate historical statistics:

```bash
spark-submit app2.py
```

This produces JSON output files such as Inv1_P11_stats.json and Inv1_P12_stats.json containing portfolio analytics.
