"""
SUTRA - Complete Usage Example
This script demonstrates all features of SUTRA library step by step.
"""

# ============================================================================
# STEP 1: INSTALL AND IMPORT
# ============================================================================
# First, install the library:
# pip install sutra

from sutra import SUTRA
import pandas as pd

print("=" * 80)
print("SUTRA - Natural Language to SQL Query System")
print("=" * 80)

# ============================================================================
# STEP 2: INITIALIZE WITH OPENAI API KEY
# ============================================================================
print("\n📌 STEP 1: Initialize SUTRA with OpenAI API Key")
print("-" * 80)

# Option 1: Pass API key directly
sutra = SUTRA(api_key="your-openai-api-key-here")

# Option 2: Use environment variable (recommended for security)
# import os
# os.environ["OPENAI_API_KEY"] = "your-key-here"
# sutra = SUTRA()

# ============================================================================
# STEP 3: UPLOAD DATA (Multiple Options)
# ============================================================================
print("\n📌 STEP 2: Upload Data")
print("-" * 80)

# Option A: Upload from CSV file
sutra.upload_data("sales_data.csv")

# Option B: Upload from Excel file
# sutra.upload_data("sales_data.xlsx")

# Option C: Upload from JSON file
# sutra.upload_data("sales_data.json")

# Option D: Upload from DataFrame
# df = pd.DataFrame({
#     'product': ['A', 'B', 'C'],
#     'sales': [100, 200, 150],
#     'region': ['North', 'South', 'East']
# })
# sutra.upload_data(df, table_name="my_sales_data")

# Option E: Upload from SQL file
# sutra.upload_data("database_dump.sql")

# Option F: Upload from PDF or DOCX (extracts tables)
# sutra.upload_data("report.pdf")

# ============================================================================
# STEP 4: VIEW DATABASE AND SCHEMA
# ============================================================================
print("\n📌 STEP 3: Explore Database")
print("-" * 80)

# List all tables
print("\n🗂️ Available tables:")
tables = sutra.list_tables()
for table in tables:
    print(f"  - {table}")

# Show schema
sutra.show_schema()

# Get sample data
print("\n📊 Sample Data:")
sample = sutra.get_sample_data(n=5)

# ============================================================================
# STEP 5: OPTION TO ACCESS DB DIRECTLY (Without API)
# ============================================================================
print("\n📌 STEP 4: Direct SQL Query (No API Required)")
print("-" * 80)

# Execute SQL directly without using OpenAI API
direct_result = sutra.direct_query(
    sql="SELECT * FROM sales_data WHERE sales > 1000",
    visualize=False
)

if direct_result["success"]:
    print("\n✓ Direct Query Results:")
    print(direct_result["data"])

# ============================================================================
# STEP 6: NATURAL LANGUAGE QUERIES
# ============================================================================
print("\n📌 STEP 5: Natural Language Queries")
print("-" * 80)

# Example queries
queries = [
    "Show me all products with sales greater than 1000",
    "What is the total sales by region?",
    "Show me the top 5 products by revenue",
    "Which region has the highest average sales?",
    "List all sales in 2024"
]

for i, question in enumerate(queries, 1):
    print(f"\n🔍 Query {i}: {question}")
    print("-" * 80)
    
    # Execute query without visualization
    result = sutra.query(question, visualize=False)
    
    if result["success"]:
        print(f"\n✓ Generated SQL: {result['sql']}")
        print(f"\n✓ Results ({len(result['data'])} rows):")
        print(result["data"].head())
    else:
        print(f"\n✗ Error: {result.get('error', 'Unknown error')}")

# ============================================================================
# STEP 7: QUERIES WITH VISUALIZATION
# ============================================================================
print("\n📌 STEP 6: Queries with Visualization")
print("-" * 80)

# Queries that benefit from visualization
viz_queries = [
    "Show me total sales by product category",
    "What is the sales trend over time?",
    "Compare sales across different regions"
]

for i, question in enumerate(viz_queries, 1):
    print(f"\n📊 Visualization Query {i}: {question}")
    print("-" * 80)
    
    # Execute query WITH visualization
    result = sutra.query(question, visualize=True)
    
    if result["success"]:
        print(f"\n✓ Generated SQL: {result['sql']}")
        print(f"✓ Results: {len(result['data'])} rows")
        print(f"✓ Visualization: {'Created' if result['visualization'] else 'Not created'}")
        
        # The visualization will open in your browser automatically
        # You can also save it:
        # if result['visualization']:
        #     result['visualization'].write_html("chart.html")

# ============================================================================
# STEP 8: ASK USER IF THEY WANT VISUALIZATION
# ============================================================================
print("\n📌 STEP 7: Interactive Query with User Choice")
print("-" * 80)

question = "What are the total sales by region?"
print(f"\n🔍 Question: {question}")

# Simulate user choice
user_wants_viz = input("Do you want visualization? (yes/no): ").strip().lower()

if user_wants_viz in ['yes', 'y']:
    result = sutra.query(question, visualize=True)
    print("✓ Query executed with visualization")
else:
    result = sutra.query(question, visualize=False)
    print("✓ Query executed without visualization")

if result["success"]:
    print(f"\n✓ Results:")
    print(result["data"])

# ============================================================================
# STEP 9: EXPORT RESULTS
# ============================================================================
print("\n📌 STEP 8: Export Results")
print("-" * 80)

if result["success"]:
    # Export to CSV
    sutra.export_results(result["data"], "query_results.csv", format="csv")
    
    # Export to Excel
    sutra.export_results(result["data"], "query_results.xlsx", format="excel")
    
    # Export to JSON
    sutra.export_results(result["data"], "query_results.json", format="json")

# ============================================================================
# STEP 10: PROVIDE FEEDBACK (Optional)
# ============================================================================
print("\n📌 STEP 9: Provide Feedback (Optional)")
print("-" * 80)

# If the query was correct
sutra.provide_feedback(
    question="Show me sales greater than 1000",
    sql="SELECT * FROM sales_data WHERE sales > 1000",
    is_correct=True
)

# If the query was incorrect, provide correct version
# sutra.provide_feedback(
#     question="Show me all products",
#     sql="SELECT name FROM products",  # Wrong
#     is_correct=False,
#     correct_sql="SELECT * FROM products"  # Correct
# )

# ============================================================================
# STEP 11: CLOSE CONNECTION
# ============================================================================
print("\n📌 STEP 10: Close SUTRA")
print("-" * 80)

sutra.close()

# ============================================================================
# ALTERNATIVE: USE CONTEXT MANAGER (RECOMMENDED)
# ============================================================================
print("\n📌 BONUS: Using Context Manager (Recommended)")
print("-" * 80)

# This automatically handles initialization and cleanup
with SUTRA(api_key="your-openai-api-key") as sutra:
    # Upload data
    sutra.upload_data("data.csv")
    
    # Query
    result = sutra.query("Show me all data", visualize=True)
    
    # Results automatically saved and connection closed when done

print("\n" + "=" * 80)
print("✓ SUTRA Example Complete!")
print("=" * 80)
