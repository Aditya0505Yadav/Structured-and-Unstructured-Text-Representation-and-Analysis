"""SQLite to MySQL Import"""
import sqlite3, mysql.connector, pandas as pd

# CHANGE THIS to your new database file
SQLITE_DB = r"C:\Users\ADITYA BATTA\Downloads\emp1_data.db"

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "emp1"

print("SQLite to MySQL Import")

sqlite_conn = sqlite3.connect(SQLITE_DB)
cursor = sqlite_conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

if not tables:
    print("ERROR: Empty!")
    exit()

print(f"Found {len(tables)} tables:")
for t in tables:
    cnt = pd.read_sql_query(f"SELECT COUNT(*) FROM {t}", sqlite_conn).iloc[0, 0]
    print(f"  {t}: {cnt} rows")

temp_conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
temp_cursor = temp_conn.cursor()
temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`")
temp_cursor.close()
temp_conn.close()

mysql_conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)
mysql_cursor = mysql_conn.cursor()

print(f"Importing to '{MYSQL_DATABASE}'...")

for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
    mysql_cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cols = [f"`{col}` {'INT' if df[col].dtype == 'int64' else 'FLOAT' if df[col].dtype == 'float64' else 'TEXT'}" for col in df.columns]
    mysql_cursor.execute(f"CREATE TABLE {table} ({', '.join(cols)})")
    
    if len(df) > 0:
        placeholders = ', '.join(['%s'] * len(df.columns))
        for _, row in df.iterrows():
            vals = [None if pd.isna(v) else v for v in row.values]
            mysql_cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", vals)
    mysql_conn.commit()
    print(f"  {table}: {len(df)} rows")

sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()

print(f"\nSUCCESS! Data in MySQL database '{MYSQL_DATABASE}'")
