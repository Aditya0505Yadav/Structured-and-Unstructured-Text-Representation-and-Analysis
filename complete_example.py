"""
SUTRA - Complete Step-by-Step Example
Follow these steps to use SUTRA in your Jupyter notebook or script.
"""

# ============================================================================
# STEP 1: INSTALL SUTRA
# ============================================================================
# Run in terminal:
# pip install sutra

print("="*80)
print("SUTRA - Natural Language to SQL Query System")
print("Step-by-Step Complete Example")
print("="*80)

# ============================================================================
# STEP 2: IMPORT SUTRA
# ============================================================================
print("\n📦 STEP 1: Import SUTRA")
print("-"*80)

from sutra import SUTRA
import pandas as pd

print("✅ SUTRA imported successfully!")

# ============================================================================
# STEP 3: ENTER YOUR OPENAI API KEY
# ============================================================================
print("\n🔑 STEP 2: Initialize with OpenAI API Key")
print("-"*80)

# Replace with your actual API key
API_KEY = "your-openai-api-key-here"

# Initialize SUTRA
sutra = SUTRA(api_key=API_KEY)

# Alternative: Use environment variable (more secure)
# import os
# os.environ["OPENAI_API_KEY"] = "your-key"
# sutra = SUTRA()

# ============================================================================
# STEP 4: UPLOAD DATA (Multiple options supported!)
# ============================================================================
print("\n📤 STEP 3: Upload Data")
print("-"*80)

# Option A: Upload from CSV file
sutra.upload_data("sales_data.csv")

# Option B: Upload from Excel
# sutra.upload_data("sales_data.xlsx")

# Option C: Upload from JSON
# sutra.upload_data("sales_data.json")

# Option D: Upload from SQL file
# sutra.upload_data("database.sql")

# Option E: Upload from DataFrame
# df = pd.DataFrame({
#     'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
#     'sales': [1500, 250, 350, 800, 150],
#     'region': ['North', 'South', 'East', 'West', 'North'],
#     'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
# })
# sutra.upload_data(df, table_name="my_sales")

# ============================================================================
# STEP 5: EXPLORE YOUR DATABASE
# ============================================================================
print("\n🔍 STEP 4: Explore Database")
print("-"*80)

# List all tables
print("\n📊 Available Tables:")
tables = sutra.list_tables()
for i, table in enumerate(tables, 1):
    print(f"   {i}. {table}")

# Show database schema
print("\n📋 Database Schema:")
sutra.show_schema()

# Get sample data
print("\n👀 Sample Data:")
sample = sutra.get_sample_data(n=5)

# ============================================================================
# STEP 6: DIRECT SQL QUERY (No API Required!)
# ============================================================================
print("\n⚡ STEP 5: Direct SQL Query (No API Cost)")
print("-"*80)
print("You can run SQL directly without using the API!")

# Example: Get all records
result1 = sutra.direct_query(
    sql="SELECT * FROM sales_data LIMIT 10",
    visualize=False
)

if result1["success"]:
    print("\n✅ Query Result:")
    print(result1["data"])

# Example: Aggregation query
result2 = sutra.direct_query(
    sql="SELECT region, SUM(sales) as total_sales FROM sales_data GROUP BY region",
    visualize=False
)

if result2["success"]:
    print("\n✅ Aggregated Result:")
    print(result2["data"])

# ============================================================================
# STEP 7: NATURAL LANGUAGE QUERIES (Without Visualization)
# ============================================================================
print("\n🗣️  STEP 6: Natural Language Queries")
print("-"*80)

# Example 1: Simple query
print("\n📝 Query 1: Simple Selection")
result = sutra.query(
    "Show me all products with sales greater than 500",
    visualize=False
)

if result["success"]:
    print(f"   Generated SQL: {result['sql']}")
    print(f"\n   Results ({len(result['data'])} rows):")
    print(result["data"])

# Example 2: Aggregation
print("\n📝 Query 2: Aggregation")
result = sutra.query(
    "What is the total sales by region?",
    visualize=False
)

if result["success"]:
    print(f"   Generated SQL: {result['sql']}")
    print(f"\n   Results:")
    print(result["data"])

# Example 3: Top N query
print("\n📝 Query 3: Top Products")
result = sutra.query(
    "Show me the top 5 products by sales",
    visualize=False
)

if result["success"]:
    print(f"   Generated SQL: {result['sql']}")
    print(f"\n   Results:")
    print(result["data"])

# Example 4: Statistical query
print("\n📝 Query 4: Statistics")
result = sutra.query(
    "What is the average sales per region?",
    visualize=False
)

if result["success"]:
    print(f"   Generated SQL: {result['sql']}")
    print(f"\n   Results:")
    print(result["data"])

# ============================================================================
# STEP 8: QUERIES WITH VISUALIZATION
# ============================================================================
print("\n📊 STEP 7: Queries with Automatic Visualization")
print("-"*80)

# Query 1: Sales by region (bar chart)
print("\n📊 Visualization 1: Sales by Region")
result = sutra.query(
    "What are the total sales by region?",
    visualize=True
)

if result["success"]:
    print(f"   ✅ Generated SQL: {result['sql']}")
    print(f"   ✅ Chart created and displayed")
    # The visualization will open automatically in your browser

# Query 2: Top products
print("\n📊 Visualization 2: Top Products")
result = sutra.query(
    "Show me the top 10 products by sales",
    visualize=True
)

if result["success"]:
    print(f"   ✅ Generated SQL: {result['sql']}")
    print(f"   ✅ Chart created and displayed")

# ============================================================================
# STEP 9: INTERACTIVE - ASK USER IF THEY WANT VISUALIZATION
# ============================================================================
print("\n❓ STEP 8: Interactive Query with User Choice")
print("-"*80)

question = "What are the sales trends over time?"
print(f"\n🔍 Question: {question}")

# Simulate user input (in Jupyter, use actual input())
user_choice = input("Do you want to visualize the results? (yes/no): ").strip().lower()

if user_choice in ['yes', 'y', 'yeah', 'yep']:
    print("\n📊 Creating visualization...")
    result = sutra.query(question, visualize=True)
else:
    print("\n📄 Showing table only...")
    result = sutra.query(question, visualize=False)

if result["success"]:
    print(f"\n✅ Generated SQL: {result['sql']}")
    print(f"\n📊 Results:")
    print(result["data"])

# ============================================================================
# STEP 10: MULTIPLE QUERIES WITH CHOICE
# ============================================================================
print("\n🔄 STEP 9: Multiple Queries with Visualization Choice")
print("-"*80)

queries = [
    "What is the total sales by product?",
    "Which region has the highest average sales?",
    "Show me sales distribution across all regions"
]

for i, q in enumerate(queries, 1):
    print(f"\n{'='*80}")
    print(f"Query {i}: {q}")
    print('='*80)
    
    # Ask user
    viz_choice = input(f"Visualize this query? (yes/no): ").strip().lower()
    
    result = sutra.query(q, visualize=(viz_choice in ['yes', 'y']))
    
    if result["success"]:
        print(f"\n✅ SQL: {result['sql']}")
        print(f"✅ Rows returned: {len(result['data'])}")
        print(f"\n📊 Data Preview:")
        print(result["data"].head())
    else:
        print(f"\n❌ Error: {result.get('error')}")

# ============================================================================
# STEP 11: EXPORT RESULTS
# ============================================================================
print("\n💾 STEP 10: Export Results")
print("-"*80)

# Run a query
result = sutra.query("SELECT * FROM sales_data")

if result["success"]:
    # Export to CSV
    sutra.export_results(result["data"], "query_results.csv", format="csv")
    
    # Export to Excel
    sutra.export_results(result["data"], "query_results.xlsx", format="excel")
    
    # Export to JSON
    sutra.export_results(result["data"], "query_results.json", format="json")
    
    print("\n✅ Results exported to multiple formats!")

# ============================================================================
# STEP 12: ADVANCED USAGE - CONTEXT MANAGER
# ============================================================================
print("\n🎯 BONUS: Using Context Manager (Recommended)")
print("-"*80)

with SUTRA(api_key=API_KEY) as sutra_instance:
    # Upload data
    sutra_instance.upload_data("data.csv")
    
    # Query
    result = sutra_instance.query("Show me all data", visualize=False)
    
    # Print results
    if result["success"]:
        print(result["data"])

# Connection automatically closed after 'with' block
print("✅ Connection closed automatically!")

# ============================================================================
# STEP 13: ONE-LINER FOR QUICK QUERIES
# ============================================================================
print("\n⚡ BONUS: One-Liner Quick Query")
print("-"*80)

from sutra import quick_query

# One line to rule them all!
result = quick_query(
    api_key=API_KEY,
    data_path="sales_data.csv",
    question="What are total sales by region?",
    visualize=True
)

if result["success"]:
    print("✅ Quick query complete!")
    print(result["data"])

# ============================================================================
# CLEANUP
# ============================================================================
print("\n🧹 STEP 11: Cleanup")
print("-"*80)

# Close connection
sutra.close()

print("\n" + "="*80)
print("✅ SUTRA TUTORIAL COMPLETE!")
print("="*80)
print("""
📚 Key Takeaways:
   1. pip install sutra
   2. from sutra import SUTRA
   3. sutra = SUTRA(api_key="your-key")
   4. sutra.upload_data("file.csv")  # Supports CSV, Excel, JSON, SQL, DataFrame
   5. sutra.direct_query("SELECT ...") # SQL without API
   6. sutra.query("natural language question")  # With API
   7. sutra.query("question", visualize=True)  # With auto-visualization
   8. Choose visualization interactively
   9. Export results to CSV/Excel/JSON

🚀 You're now ready to use SUTRA in your projects!
""")
