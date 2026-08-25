# Libraries and Packages
from pathlib import Path
import os
import pandas as pd
import pyodbc

# Load Data
BASE_DIR = Path(__file__).resolve().parents[2]
processed_dir = BASE_DIR / "data" / "processed"
demographic_df = pd.read_csv(processed_dir / "demographic.csv")
location_df = pd.read_csv(processed_dir / "location.csv")
account_df = pd.read_csv(processed_dir / "account.csv")

# Create connection
driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
server = os.getenv("SQL_SERVER", "127.0.0.1,1433")
database = os.getenv("SQL_DATABASE", "BankChurn")
trusted_connection = os.getenv("SQL_TRUSTED_CONNECTION", "false").lower() == "true"

connection_parts = [
    f"Driver={{{driver}}}",
    f"Server={server}",
    f"Database={database}",
    "Encrypt=yes",
    "TrustServerCertificate=yes",
]

if trusted_connection:
    connection_parts.append("Trusted_Connection=yes")
else:
    username = os.getenv("SQL_USERNAME", "sa")
    password = os.getenv("SQL_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "Set SQL_USERNAME and SQL_PASSWORD, or set "
            "SQL_TRUSTED_CONNECTION=true on a Windows SQL Server client."
        )
    connection_parts.extend([f"UID={username}", f"PWD={password}"])

conn = pyodbc.connect(";".join(connection_parts) + ";", timeout=10)

cursor = conn.cursor()



# Push demographic to database
cursor.execute("SET IDENTITY_INSERT demographic ON")
conn.commit()

for _, row in demographic_df.iterrows():
    cursor.execute("""
        INSERT INTO demographic (
            CustomerId,
            Gender,
            Age,
            Salary,
            LocationId,
            Churned
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    int(row.CustomerId),
    row.Gender,
    int(row.Age),
    float(row.Salary),
    int(row.LocationId),
    int(row.Churned)
    )

conn.commit()
cursor.execute("SET IDENTITY_INSERT demographic OFF")
conn.commit()
print("Data inserted successfully")




# Push location to database
cursor.execute("SET IDENTITY_INSERT location ON")
conn.commit()

for _, row in location_df.iterrows():
    cursor.execute("""
        INSERT INTO location (
            LocationId,
            Geography
        )
        VALUES (?, ?)
    """,
    int(row.LocationId),
    row.Geography
    )

conn.commit()
cursor.execute("SET IDENTITY_INSERT location OFF")
conn.commit()
print("Data inserted successfully")




# Push Account to database
for _, row in account_df.iterrows():
    cursor.execute("""
        INSERT INTO account (
            CustomerId,
            Tenure, 
            Balance,     
            NumProducts,
            HasCreditCard,
            IsActive
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    int(row.CustomerId),
    int(row.Tenure),
    None if pd.isna(row.Balance) else float(row.Balance),
    int(row.NumProducts),
    int(row.HasCreditCard),
    int(row.IsActive),
    )

conn.commit()
print("Data inserted successfully")