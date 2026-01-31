from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

# Create Spark session
def create_spark_session():
    spark_home = os.popen('brew --prefix apache-spark').read().strip() + "/libexec"
    spark = SparkSession.builder \
        .config("spark.home", spark_home) \
        .config("spark.jars", f"{spark_home}/jars/mysql-connector-j-8.0.33.jar") \
        .config("spark.driver.extraClassPath", f"{spark_home}/jars/mysql-connector-j-8.0.33.jar") \
        .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
        .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow") \
        .appName("InvestorsDB Analyzer") \
        .getOrCreate()
    return spark

# Read data from MySQL
def read_data_from_mysql(spark, investor):
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/InvestorsDB") \
        .option("user", "itc6107") \
        .option("password", "itc6107") \
        .option("query", f"""
            SELECT I.Name as inv_name, P.Name as por_name
            FROM Investors as I
            INNER JOIN Investors_Portfolios as IP ON I.Id=IP.iid
            INNER JOIN Portfolios as P ON P.Id=IP.pid
            WHERE I.Id={investor}
        """) \
        .option("driver", "com.mysql.jdbc.Driver") \
        .load()

# Generate portfolio statistics
def generate_portfolio_stats(spark, investor_id):
    investors_portfolios_df = read_data_from_mysql(spark, investor_id)

    for row in investors_portfolios_df.collect():
        inv_name, por_name = row['inv_name'], row['por_name']
        table_name = f"{inv_name}_{por_name}"
        portfolio_df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:mysql://localhost:3306/InvestorsDB") \
            .option("user", "itc6107") \
            .option("password", "itc6107") \
            .option("dbtable", table_name) \
            .option("driver", "com.mysql.jdbc.Driver") \
            .load()

        # Calculate statistics
        max_min_daily_change = portfolio_df.agg(
            round(min("Daily_Evaluation_Change"), 2).alias("min_daily_change"),
            round(max("Daily_Evaluation_Change"), 2).alias("max_daily_change"),
            round(min("Daily_Evaluation_Change_Percentage"), 2).alias("min_daily_change_pct"),
            round(max("Daily_Evaluation_Change_Percentage"), 2).alias("max_daily_change_pct")
        )

        max_min_daily_change_per_year = portfolio_df.withColumn("year", year("As_Of")).groupBy("year").agg(
            round(min("Daily_Evaluation_Change"), 2).alias("min_daily_change"),
            round(max("Daily_Evaluation_Change"), 2).alias("max_daily_change"),
            round(min("Daily_Evaluation_Change_Percentage"), 2).alias("min_daily_change_pct"),
            round(max("Daily_Evaluation_Change_Percentage"), 2).alias("max_daily_change_pct")
        ).orderBy(desc("year"))

        avg_stddev_evaluation = portfolio_df.agg(
            round(avg("Evaluation"), 2).alias("avg_evaluation"),
            round(stddev("Evaluation"), 2).alias("stddev_evaluation")
        )

        # Write results to file
        file_name = f"{inv_name}_{por_name}_stats.json"
        with open(file_name, "w") as f:
            f.write("{\n")
            f.write('"MaxMinDailyChange": ')
            max_min_daily_change.toPandas().to_json(f, orient="records", lines=False)
            f.write(",\n")

            f.write('"MaxMinDailyChangePerYear": ')
            max_min_daily_change_per_year.toPandas().to_json(f, orient="records", lines=False)
            f.write(",\n")

            f.write('"AvgStdDevEvaluation": ')
            avg_stddev_evaluation.toPandas().to_json(f, orient="records", lines=False)
            f.write("\n}")

        print(f"Generated stats file: {file_name}")

# Main execution
spark = create_spark_session()
investor_id = 1
generate_portfolio_stats(spark, investor_id)
spark.stop()