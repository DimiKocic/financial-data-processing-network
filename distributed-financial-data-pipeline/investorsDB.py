import mysql.connector

# Establish database connection
connection = mysql.connector.connect(
    host="localhost",
    user="itc6107",
    password="itc6107",
)

cursor = connection.cursor()

# Drop and create database
cursor.execute("DROP DATABASE IF EXISTS InvestorsDB")
cursor.execute("CREATE DATABASE InvestorsDB")
cursor.execute("USE InvestorsDB")

# Create tables
cursor.execute("""
    CREATE TABLE Investors (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        City VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE Portfolios (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        Cumulative BOOLEAN
    )
""")

cursor.execute("""
    CREATE TABLE Investors_Portfolios (
        iid INT,
        pid INT,
        FOREIGN KEY (iid) REFERENCES Investors (Id),
        FOREIGN KEY (pid) REFERENCES Portfolios (Id)
    )
""")

# Populate into Investors table
investors_data = [
    (1, 'Inv1', 'London'),
    (2, 'Inv2', 'New York'),
    (3, 'Inv3', 'Paris')
]

for investor in investors_data:
    cursor.execute("INSERT INTO Investors (Id, Name, City) VALUES (%s, %s, %s)", investor)

# Populate Portfolios table
portfolios_data = [
    (1, 'P11', True),
    (2, 'P12', True),
    (3, 'P21', True),
    (4, 'P22', True),
    (5, 'P31', True),
    (6, 'P32', True)
]

for portfolio in portfolios_data:
    cursor.execute("INSERT INTO Portfolios (Id, Name, Cumulative) VALUES (%s, %s, %s)", portfolio)

# Populate Investors_Portfolios table
investors_portfolios_data = [
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 6)
]

for ip in investors_portfolios_data:
    cursor.execute("INSERT INTO Investors_Portfolios (iid, pid) VALUES (%s, %s)", ip)

# Create individual portfolio tables
cursor.execute("""
    SELECT CONVERT(I.id, CHAR) AS iid, SUBSTRING(P.Name, 2, 2) AS pid
    FROM Investors AS I
    INNER JOIN Investors_Portfolios AS IP ON I.Id = IP.iid
    INNER JOIN Portfolios AS P ON P.Id = IP.pid
""")

investors_portfolios = cursor.fetchall()

for investor, portfolio in investors_portfolios:
    table_name = f"Inv{investor}_P{portfolio}"
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            As_Of DATE,
            Evaluation DOUBLE,
            Daily_Evaluation_Change DOUBLE,
            Daily_Evaluation_Change_Percentage DOUBLE
        )
    """)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()