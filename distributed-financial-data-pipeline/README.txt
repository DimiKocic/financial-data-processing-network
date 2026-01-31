1. Open a terminal window and:
	
	1.1 Start Zookeeper
	First, start the Zookeeper service. Zookeeper is required for managing Kafka brokers. To do this, open a terminal window and execute the following command:
	sudo systemctl start zookeeper

	1.2 Start Kafka
	Once Zookeeper is up and running, start Kafka by executing the command:
	sudo systemctl start kafka

	1.3 Create Kafka Topic for Stock Data
	Next, you need to create a Kafka topic where the stock data will be published. This topic is called StockExchange. To create the topic, use the following command:
	kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic StockExchange

	1.4 Create Kafka Topic for Portfolio Evaluations
	Similarly, create another Kafka topic where the portfolio evaluation results will be sent. This topic is called portfolios. You can create this topic with the following command:
	kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic portfolios

2. Run the Python Scripts
	Once Kafka and Zookeeper are set up, it’s time to run the various Python scripts that simulate stock data generation, portfolio evaluation, and data processing.

	2.1 Open Multiple Terminal Windows
	Open seven terminal windows and navigate (cd) to the directory where the Python scripts are stored. Then, in each terminal window, run the following commands for the respective scripts:

	In Tab 1, run the first stock data generator script by executing:
	python3 se1_server.py
	In Tab 2, run the second stock data generator script by executing:
	python3 se2_server.py
	In Tab 3, run the first investor evaluation script by executing:
	python3 inv1.py
	In Tab 4, run the second investor evaluation script by executing:
	python3 inv2.py
	In Tab 5, run the third investor evaluation script by executing:
	python3 inv3.py
	In Tab 6, run the database insertion script. This script handles storing the portfolio evaluation data in the database. To execute it, run:
	python investorsDB.py
	In Tab 7, run the application that monitors and processes the stock data and portfolio evaluations by executing:
	python3 app1.py

3. Wait for Data to Be Transferred
	After starting the scripts, it is important to wait until all portfolio evaluation results are transferred to the database. This might take some time, depending on the amount of data being processed and transferred.

	3.1 Open an Additional Terminal for Report Generation
	Once you are confident that the data has been fully transferred to the database, open an 8th terminal window. In this window, run the following command to generate reports:
	python3 app2.py
	This script will generate two JSON files that contain the portfolio statistics for investor 1. The generated files will be: Inv1_P11_stats.json and Inv1_P12_stats.json. These files will be saved in the same directory where the Python scripts are located.

	If you want to generate reports for other investors (such as investor 2 or investor 3), you can easily modify the app2.py script. In the script, locate line 122 and change the investor ID to one of the following values:
	1 for Investor 1
	2 for Investor 2
	3 for Investor 3
