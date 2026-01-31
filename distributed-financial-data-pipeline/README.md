# Kafka Stock Exchange Simulation — Setup & Execution Guide

# 1. Start Required Services

- Open a terminal window and run the following commands.

## 1.1 Start Zookeeper

- Zookeeper is required for managing Kafka brokers:

```bash
sudo systemctl start zookeeper
```

## 1.2 Start Kafka
- Once Zookeeper is running, start Kafka:

```bash
sudo systemctl start kafka
```

## 1.3 Create Kafka Topic for Stock Data

- Create the StockExchange topic:
```bash
kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic StockExchange
```

## 1.4 Create Kafka Topic for Portfolio Evaluations

- Create the portfolios topic:

```bash
kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic portfolios
```

# 2. Run the Python Scripts

- After Kafka and Zookeeper are running, open seven terminal tabs/windows.
- In each tab, navigate to the directory containing the Python scripts:

```bash
cd /path/to/your/scripts
```

- Then run the following:

Tab 1 — Stock Exchange Server 1
```bash
python3 se1_server.py
```

Tab 2 — Stock Exchange Server 2
```bash
python3 se2_server.py
```

Tab 3 — Investor 1 Evaluation
```bash
python3 inv1.py
```

Tab 4 — Investor 2 Evaluation

```bash
python3 inv2.py
```

Tab 5 — Investor 3 Evaluation
```bash
python3 inv3.py
```

Tab 6 — Database Insertion Service
- Stores portfolio evaluation results in the database:
```bash
python investorsDB.py
```

Tab 7 — Main Processing Application
- Monitors and processes stock data and portfolio evaluations:

```bash
python3 app1.py
```

# 3. Wait for Data Transfer
- Allow sufficient time for all portfolio evaluation results to be processed and written to the database.
- This duration depends on data volume and system performance.

# 4. Generate Reports
- Once data transfer is complete, open an 8th terminal window and run:
```bash
python3 app2.py
```
- This generates two JSON files for Investor 1:
  Inv1_P11_stats.json
  Inv1_P12_stats.json

- These files are saved in the same directory as the Python scripts.

# 5. Generating Reports for Other Investors

- To generate reports for different investors:

Open app2.py
Locate line 122

- Change the investor ID to one of the following:

1 → Investor 1

2 → Investor 2

3 → Investor 3

- Save the file and rerun:
```bash
python3 app2.py
```





