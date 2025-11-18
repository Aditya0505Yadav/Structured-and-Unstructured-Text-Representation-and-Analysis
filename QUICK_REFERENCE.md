# 🚀 SUTRA - Quick Reference Guide

## Installation (After Publishing)
```bash
pip install sutra
```

## Complete Workflow

```python
# ============================================
# STEP 1: IMPORT
# ============================================
from sutra import SutraClient
import pandas as pd

# ============================================
# STEP 2: ENTER API KEY
# ============================================
client = SutraClient(api_key="sk-your-openai-key")

# ============================================
# STEP 3: UPLOAD DATA (Multiple Options)
# ============================================

# Option A: Upload file (any format)
client.upload_data("sales.csv")
client.upload_data("products.xlsx")
client.upload_data("customers.json")

# Option B: Upload DataFrame
df = pd.DataFrame({
    'name': ['Product A', 'Product B'],
    'price': [100, 200],
    'quantity': [50, 30]
})
client.upload_dataframe(df, table_name="inventory")

# ============================================
# STEP 4: VIEW DATABASE
# ============================================

# List all tables
tables = client.list_tables()
# Output: ['sales', 'products', 'customers', 'inventory']

# Get table details
info = client.get_table_info("sales")

# ============================================
# STEP 5: OPTION 1 - DIRECT SQL (No API)
# ============================================

# Execute SQL without NLP
result = client.execute_sql("""
    SELECT product, SUM(amount) as total
    FROM sales
    WHERE date > '2024-01-01'
    GROUP BY product
""")

# With visualization
result = client.execute_sql(
    "SELECT region, SUM(amount) FROM sales GROUP BY region",
    visualize=True
)

# ============================================
# STEP 6: OPTION 2 - NATURAL LANGUAGE QUERIES
# ============================================

# Simple queries
result = client.query("What are the total sales?")
result = client.query("How many customers do we have?")
result = client.query("Show me top 10 products by revenue")

# ============================================
# STEP 7: VISUALIZATION (Yes/No)
# ============================================

# WITH visualization (default)
result = client.query(
    "Show sales trend over the last 6 months",
    visualize=True  # This is default
)

# WITHOUT visualization
result = client.query(
    "List all customers from New York",
    visualize=False
)

# ============================================
# STEP 8: VIEW RESULTS
# ============================================

# Results are in dictionary format
if result['status'] == 'success':
    # Convert to DataFrame for better display
    df = pd.DataFrame(result['results'])
    print(df)
    
    # Check if visualization was created
    if result['visualization']:
        print("Visualization available!")

# ============================================
# BONUS: ADVANCED FEATURES
# ============================================

# See generated SQL (debugging)
result = client.query(
    "What's the average order value?",
    return_sql=True
)
print("SQL:", result['sql_query'])

# Provide feedback to improve future queries
client.provide_feedback(
    query="Show total revenue",
    generated_sql="SELECT SUM(amount) FROM sales",
    is_correct=True
)

# Get database schema
schema = client.get_schema()
print(schema)

# Clear cache
client.clear_cache()

# Close connection when done
client.close()
```

## 📝 Real-World Examples

### Example 1: Sales Analysis
```python
client = SutraClient(api_key="sk-...")

# Upload data
client.upload_data("sales_2024.csv")

# Analyze
client.query("What are total sales by month?", visualize=True)
client.query("Which region has highest revenue?")
client.query("Show top 5 sales representatives")
client.query("What's the average deal size?")
```

### Example 2: Customer Analytics
```python
# Upload customer data
client.upload_data("customers.xlsx")

# Ask questions
client.query("How many customers by country?", visualize=True)
client.query("What's the customer retention rate?")
client.query("Show customer lifetime value distribution")
```

### Example 3: Inventory Management
```python
# Upload inventory
client.upload_data("inventory.json")

# Check stock
client.query("Which products are low in stock?")
client.query("Show inventory value by category", visualize=True)
client.query("What's the inventory turnover rate?")
```

### Example 4: Financial Analysis
```python
# Upload financial data
client.upload_data("transactions.csv")

# Analyze finances
client.query("What's our monthly burn rate?")
client.query("Show revenue vs expenses", visualize=True)
client.query("Calculate profit margin by product")
```

## 🎯 Quick Tips

### Tip 1: File Formats Supported
- ✅ CSV (.csv)
- ✅ Excel (.xlsx, .xls)
- ✅ JSON (.json)
- ✅ PDF (.pdf)
- ✅ Word (.docx)
- ✅ Text (.txt)
- ✅ HTML (.html)
- ✅ Pandas DataFrames

### Tip 2: When to Use What

**Use Natural Language (`client.query()`) when:**
- You want to explore data quickly
- You're not sure of the exact SQL
- You want automatic visualization
- You're doing ad-hoc analysis

**Use Direct SQL (`client.execute_sql()`) when:**
- You know exactly what SQL you need
- You need complex joins or subqueries
- Performance is critical
- You're debugging query generation

### Tip 3: Visualization

Visualizations are automatic based on data:
- **Time series** → Line chart
- **Categories** → Bar chart
- **Distributions** → Pie chart
- **Comparisons** → Bar/column chart
- **Correlations** → Scatter plot

### Tip 4: Performance

```python
# Enable caching (default)
client = SutraClient(api_key="sk-...", use_cache=True)

# Custom database location
client = SutraClient(
    api_key="sk-...",
    db_path="my_custom_database.db"
)

# Clear cache when needed
client.clear_cache()
```

## 🐛 Troubleshooting

### Problem: "API key not found"
```python
# Solution 1: Pass directly
client = SutraClient(api_key="sk-your-key")

# Solution 2: Set environment variable
import os
os.environ['OPENAI_API_KEY'] = 'sk-your-key'
client = SutraClient()
```

### Problem: "Table not found"
```python
# Check available tables
client.list_tables()

# Upload data first
client.upload_data("your_file.csv")
```

### Problem: Query not working well
```python
# See the generated SQL
result = client.query("your question", return_sql=True)
print(result['sql_query'])

# Or use direct SQL
client.execute_sql("your SQL here")

# Provide feedback
client.provide_feedback(
    query="...",
    generated_sql="...",
    is_correct=False,
    correct_sql="..."
)
```

## 📚 Resources

- **Full Tutorial**: `examples/sutra_usage_guide.ipynb`
- **Quick Start**: `python examples/quickstart.py`
- **Documentation**: README.md
- **Tests**: `pytest tests/test_sutra.py`

## ⚡ One-Liner Examples

```python
# Quick analysis in 3 lines
from sutra import SutraClient
client = SutraClient(api_key="sk-...")
client.upload_data("data.csv"); client.query("Show me insights", visualize=True)
```

---

**That's it! You're ready to use SUTRA! 🎉**
