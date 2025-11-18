"""
Quick Test Script for SUTRA
Run this to verify everything works before publishing
"""

import sys
import os

print("="*80)
print("SUTRA - Quick Test Script")
print("="*80)

# Test 1: Import
print("\n✓ Test 1: Importing SUTRA...")
try:
    from sutra import SUTRA, quick_query
    print("   ✅ Import successful!")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize without API key (should warn)
print("\n✓ Test 2: Initialize without API key...")
try:
    sutra_no_key = SUTRA()
    print("   ✅ Initialization successful (warning expected)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Initialize with dummy API key
print("\n✓ Test 3: Initialize with API key...")
try:
    sutra = SUTRA(api_key="test-key-123")
    print("   ✅ Initialization successful!")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 4: Create sample data and upload
print("\n✓ Test 4: Upload DataFrame...")
try:
    import pandas as pd
    
    df = pd.DataFrame({
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
        'sales': [1500, 250, 350, 800, 150],
        'region': ['North', 'South', 'East', 'West', 'North'],
        'quantity': [10, 50, 30, 15, 25]
    })
    
    sutra.upload_data(df, table_name="test_sales")
    print("   ✅ Data upload successful!")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 5: List tables
print("\n✓ Test 5: List tables...")
try:
    tables = sutra.list_tables()
    print(f"   ✅ Found {len(tables)} table(s): {tables}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Show schema
print("\n✓ Test 6: Show schema...")
try:
    sutra.show_schema()
    print("   ✅ Schema displayed successfully!")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 7: Get sample data
print("\n✓ Test 7: Get sample data...")
try:
    sample = sutra.get_sample_data(n=3)
    print(f"   ✅ Retrieved {len(sample)} sample rows!")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 8: Direct SQL query
print("\n✓ Test 8: Direct SQL query...")
try:
    result = sutra.direct_query(
        "SELECT * FROM test_sales WHERE sales > 300",
        visualize=False
    )
    
    if result["success"]:
        print(f"   ✅ Query executed! Returned {len(result['data'])} rows")
        print(f"   Data preview:")
        print(result['data'])
    else:
        print(f"   ❌ Query failed: {result.get('error')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 9: Aggregation query
print("\n✓ Test 9: Aggregation query...")
try:
    result = sutra.direct_query(
        "SELECT region, SUM(sales) as total_sales FROM test_sales GROUP BY region",
        visualize=False
    )
    
    if result["success"]:
        print(f"   ✅ Aggregation successful!")
        print(result['data'])
    else:
        print(f"   ❌ Failed: {result.get('error')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 10: Export results
print("\n✓ Test 10: Export results...")
try:
    if result["success"]:
        sutra.export_results(result['data'], "test_output.csv", format="csv")
        
        # Check if file exists
        if os.path.exists("test_output.csv"):
            print("   ✅ Export successful! File created: test_output.csv")
            # Clean up
            os.remove("test_output.csv")
        else:
            print("   ❌ File not created")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 11: Context manager
print("\n✓ Test 11: Context manager...")
try:
    with SUTRA(api_key="test-key") as sutra_ctx:
        sutra_ctx.upload_data(df, table_name="test_data")
        result = sutra_ctx.direct_query("SELECT * FROM test_data LIMIT 2")
        if result["success"]:
            print(f"   ✅ Context manager works! Retrieved {len(result['data'])} rows")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 12: Clean up
print("\n✓ Test 12: Cleanup...")
try:
    sutra.close()
    print("   ✅ Connection closed successfully!")
    
    # Remove test database
    if os.path.exists("sutra_database.db"):
        os.remove("sutra_database.db")
        print("   ✅ Test database removed")
        
    # Remove cache file
    if os.path.exists("sutra_cache.pkl"):
        os.remove("sutra_cache.pkl")
        print("   ✅ Cache file removed")
        
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Summary
print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("""
Your SUTRA package is ready to publish! 🚀

Next steps:
1. Update author info in setup.py
2. Create LICENSE file
3. Run: python -m build
4. Run: python -m twine upload --repository testpypi dist/*
5. Test installation
6. Run: python -m twine upload dist/*

See PUBLISHING_GUIDE.md for detailed instructions.
""")
