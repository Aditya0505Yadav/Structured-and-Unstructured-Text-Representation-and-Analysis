"""
SUTRA - Quick Start Demo
Run this to see SUTRA in action!
"""

print("="*80)
print("🚀 SUTRA - Quick Start Demo")
print("="*80)

# Step 1: Import
print("\n📦 Step 1: Import SUTRA")
from sutra import SUTRA
import pandas as pd
print("✅ Imported successfully!")

# Step 2: Initialize (with dummy key for demo)
print("\n🔑 Step 2: Initialize")
sutra = SUTRA(api_key="demo-key")

# Step 3: Create sample data
print("\n📊 Step 3: Create Sample Data")
df = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam', 'Headphones'],
    'sales': [1500, 250, 350, 800, 150, 200],
    'region': ['North', 'South', 'East', 'West', 'North', 'South'],
    'quantity': [10, 50, 30, 15, 25, 40]
})
print(df)

# Step 4: Upload data
print("\n📤 Step 4: Upload Data")
sutra.upload(df, name="demo_sales")

# Step 5: View database
print("\n🔍 Step 5: View Database")
print("\nTables:", sutra.tables())
sutra.schema()

# Step 6: Preview data
print("\n👀 Step 6: Preview Data")
sutra.peek(n=3)

# Step 7: Direct SQL (No API needed!)
print("\n⚡ Step 7: Direct SQL Query (FREE - No API cost)")
result = sutra.sql("SELECT * FROM demo_sales WHERE sales > 300")
if result.success:
    print("\n✅ Results:")
    print(result.data)

# Step 8: Aggregation query
print("\n📊 Step 8: Aggregation Query")
result = sutra.sql("""
    SELECT region, 
           SUM(sales) as total_sales,
           AVG(sales) as avg_sales,
           COUNT(*) as count
    FROM demo_sales 
    GROUP BY region
    ORDER BY total_sales DESC
""")
if result.success:
    print("\n✅ Results:")
    print(result.data)

# Step 9: Export results
print("\n💾 Step 9: Export Results")
if result.success:
    sutra.export(result.data, "demo_output.csv")
    print("✅ Exported to demo_output.csv")

# Step 10: Clean up
print("\n🧹 Step 10: Cleanup")
sutra.close()

import os
if os.path.exists("demo_output.csv"):
    os.remove("demo_output.csv")
if os.path.exists("sutra.db"):
    os.remove("sutra.db")

print("\n" + "="*80)
print("✅ DEMO COMPLETE!")
print("="*80)
print("""
📚 Next Steps:
   1. Open SUTRA_Complete_Guide.ipynb for full tutorial
   2. Add your OpenAI API key to use natural language queries
   3. Try: result = sutra.ask("What are total sales?", viz=True)

🚀 To publish to PyPI:
   1. Run: python -m build
   2. Run: python -m twine upload dist/*
   
See FINAL_SUMMARY.md for complete instructions!
""")
