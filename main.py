#!/usr/bin/env python3
"""Main entry point for NLP to SQL converter"""

import argparse
import sys
from pathlib import Path
from sutra.data_loader import UnstructuredDataLoader
from sutra.schema_generator import SchemaGenerator
from sutra.database_manager import DatabaseManager
from sutra.nlp_processor import NLPProcessor
from sutra.visualizer import DataVisualizer
import config
from sutra.direct_query import list_databases

def main():
    parser = argparse.ArgumentParser(description='Convert unstructured data to SQL database')
    parser.add_argument('--input', type=str, help='Input file path')
    parser.add_argument('--sample', action='store_true', help='Use sample data')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--visualize', action='store_true', help='Enable visualization')
    
    args = parser.parse_args()
    
    print("="*60)
    print("NLP TO SQL CONVERTER")
    print("="*60)
    
    # Choose mode: Use existing or create new
    if config.DB_TYPE == 'mysql':
        databases = list_databases()
        
        print("\n📂 Options:")
        print("  0. Create NEW database (uses API)")
        for i, db_name in enumerate(databases, 1):
            print(f"  {i}. Use existing: {db_name} (no API)")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '0':
            # CREATE NEW DATABASE
            if args.input:
                input_path = Path(args.input)
                db_name = input_path.stem.lower().replace(' ', '_').replace('-', '_')
                config.MYSQL_DATABASE = f"{db_name}_db"
            else:
                config.MYSQL_DATABASE = "sample_data_db"
            
            print(f"\n✅ Creating new database: {config.MYSQL_DATABASE}")
            
            # Load data and generate schema
            loader = UnstructuredDataLoader()
            if args.sample:
                data = loader.load_sample()
            elif args.input:
                data = loader.auto_load(args.input)
            else:
                data = loader.load_sample()
            
            if not data:
                print("❌ No data loaded.")
                return 1
            
            # Generate schema with API
            print("\n📄 Generating SQL Schema...")
            generator = SchemaGenerator(config.OPENAI_API_KEY, config.MODEL_NAME)
            schema_sql = generator.generate_schema(data)
            
            # Create database
            db = DatabaseManager(config.DB_PATH if not config.IN_MEMORY_DB else ':memory:', db_type=config.DB_TYPE)
            db.execute_schema(schema_sql)
            db.display_tables()
            
        else:
            # USE EXISTING DATABASE - NO API CALL!
            config.MYSQL_DATABASE = databases[int(choice) - 1]
            print(f"\n✅ Using existing database: {config.MYSQL_DATABASE}")
            
            # Just connect to existing database
            db = DatabaseManager(config.DB_PATH if not config.IN_MEMORY_DB else ':memory:', db_type=config.DB_TYPE)
            db.display_tables()
    
    # Interactive mode works with either new or existing database
    if args.interactive:
        print("\n💬 Starting Interactive Mode...")
        processor = NLPProcessor(db, None)
        visualizer = DataVisualizer() if args.visualize else None
        
        while True:
            print("\n" + "="*60)
            question = input("❓ Enter your question (or 'exit' to quit): ").strip()
            
            if question.lower() == 'exit':
                break
            
            if question:
                result_df, sql_query = processor.process_question(question)
                
                if result_df is not None and not result_df.empty:
                    print(f"\n📊 Results ({len(result_df)} rows):")
                    processor.display_results(result_df)
                    
                    if visualizer and args.visualize and len(result_df) > 1:
                        visualizer.visualize(result_df, question)
    
    print("\n✅ Process completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())