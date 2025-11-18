# 🎉 QuerySUTRA v0.1.2 - Ready to Upload!

## ✅ What's New in v0.1.2

### 🆕 Database Export Features:

1. **Export to MySQL** (Local or Cloud)
2. **Export to PostgreSQL** (Local or Cloud)  
3. **Export Database** (SQLite, SQL, JSON, Excel)
4. **Save Schema** (SQL, JSON, Markdown)
5. **Complete Backup** (All formats at once)

---

## 🚀 Upload New Version

### Step 1: Get NEW PyPI Token
Your old token expired. Create a new one:
1. Go to: https://pypi.org/manage/account/token/
2. Delete old "Aditya" or "QuerySUTRA-Upload" token
3. Create NEW token:
   - Name: `QuerySUTRA-v0.1.2`
   - Scope: **Project: QuerySUTRA** (more secure!)
4. **COPY THE TOKEN**

### Step 2: Build and Upload

```powershell
# Clean old builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build v0.1.2
python -m build

# Upload with YOUR NEW TOKEN
python -m twine upload dist/* -u __token__ -p YOUR_NEW_TOKEN_HERE
```

---

## 📖 New Features Usage

### 1. Export to MySQL

```python
from sutra import SUTRA

sutra = SUTRA(api_key="...")
sutra.upload("data.csv")

# Local MySQL
sutra.save_to_mysql("localhost", "root", "password", "mydb")

# Cloud MySQL (AWS RDS, Google Cloud SQL, etc.)
sutra.save_to_mysql(
    host="mydb.us-east-1.rds.amazonaws.com",
    user="admin",
    password="cloudpass",
    database="production"
)
```

### 2. Export to PostgreSQL

```python
# Local PostgreSQL
sutra.save_to_postgres("localhost", "postgres", "password", "mydb")

# Heroku PostgreSQL
sutra.save_to_postgres(
    host="ec2-xxx.compute-1.amazonaws.com",
    user="user",
    password="pass",
    database="dbname"
)
```

### 3. Export Database

```python
# SQLite backup
sutra.export_db("backup.db", format="sqlite")

# SQL dump
sutra.export_db("schema.sql", format="sql")

# JSON export
sutra.export_db("data.json", format="json")

# Excel (all tables as sheets)
sutra.export_db("data.xlsx", format="excel")
```

### 4. Save Schema Only

```python
# SQL format
sutra.save_schema("schema.sql", format="sql")

# JSON format
sutra.save_schema("schema.json", format="json")

# Markdown documentation
sutra.save_schema("schema.md", format="markdown")
```

### 5. Complete Backup

```python
# Creates 3 files: .db, .sql, .json
sutra.backup()

# Or specify location
sutra.backup("/backups")
```

---

## 📊 Complete Example

```python
from sutra import SUTRA

# Initialize
sutra = SUTRA(api_key="your-openai-key")

# Upload data
sutra.upload("sales.csv")

# Analyze
result = sutra.ask("What are top products?", viz=True)
print(result.data)

# Export to multiple destinations
sutra.save_to_mysql("localhost", "root", "pass", "sales_db")
sutra.save_to_postgres("pg-host", "user", "pass", "analytics")
sutra.export_db("backup.db", format="sqlite")
sutra.backup()

print("✅ Data saved to MySQL, PostgreSQL, and backed up!")
```

---

## 🎯 After Upload

Users will install:
```bash
pip install --upgrade QuerySUTRA
```

Or with database support:
```bash
# With MySQL support
pip install QuerySUTRA[mysql]

# With PostgreSQL support  
pip install QuerySUTRA[postgres]

# With both
pip install QuerySUTRA[all]
```

---

## ✨ Features Summary

| Feature | Command |
|---------|---------|
| Upload | `.upload("file.csv")` |
| Query | `.ask("question", viz=True)` |
| Direct SQL | `.sql("SELECT ...")` |
| Export MySQL | `.save_to_mysql(...)` |
| Export PostgreSQL | `.save_to_postgres(...)` |
| Export DB | `.export_db("file.db")` |
| Save Schema | `.save_schema("schema.sql")` |
| Backup All | `.backup()` |

---

## 🔥 Ready to Publish!

Run these commands NOW:

```powershell
# 1. Clean
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# 2. Build
python -m build

# 3. Get new token from PyPI

# 4. Upload
python -m twine upload dist/* -u __token__ -p YOUR_NEW_TOKEN
```

**Your package will be LIVE with all the new features!** 🎉
