"""
SUTRA - Simple Unified Tool for Relational Analysis
A single-file natural language to SQL query system with visualization.

Installation:
    pip install sutra

Usage:
    from sutra import SUTRA
    
    sutra = SUTRA(api_key="your-openai-key")
    sutra.upload("data.csv")
    result = sutra.ask("Show me total sales", viz=True)

Author: Aditya Batta
License: MIT
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Aditya Batta"
__all__ = ["SUTRA"]

import os
import sqlite3
import pandas as pd
import numpy as np
from typing import Optional, Union, Dict, Any
from pathlib import Path
import json
import hashlib
import warnings
warnings.filterwarnings('ignore')

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️  Install openai for NLP features: pip install openai")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class SUTRA:
    """
    SUTRA - Natural Language to SQL Query System
    
    A simple, powerful tool for data analysis with natural language.
    
    Examples:
        Basic usage:
        >>> sutra = SUTRA(api_key="sk-...")
        >>> sutra.upload("data.csv")
        >>> result = sutra.ask("What are total sales?")
        >>> print(result.data)
        
        With visualization:
        >>> result = sutra.ask("Show sales by region", viz=True)
        
        Direct SQL (no API cost):
        >>> result = sutra.sql("SELECT * FROM data WHERE amount > 1000")
    """
    
    def __init__(self, api_key: Optional[str] = None, db: str = "sutra.db"):
        """
        Initialize SUTRA.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            db: Database file path
        """
        print("🚀 Initializing SUTRA v0.1.0...")
        
        # Setup API
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and HAS_OPENAI else None
        
        # Setup database
        self.db_path = db
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # State
        self.current_table = None
        self.schema = {}
        self.cache = {}
        
        print(f"✅ Ready! Database: {db}")
        if not self.api_key:
            print("⚠️  No API key - use .sql() for direct queries only")
    
    # ========================================================================
    # STEP 1: UPLOAD DATA
    # ========================================================================
    
    def upload(self, data: Union[str, pd.DataFrame], name: Optional[str] = None) -> 'SUTRA':
        """
        Upload data from any source.
        
        Supports: CSV, Excel, JSON, SQL, DataFrame
        
        Args:
            data: File path or DataFrame
            name: Table name (auto-generated if None)
        
        Returns:
            self (for chaining)
        
        Examples:
            >>> sutra.upload("data.csv")
            >>> sutra.upload(df, name="sales")
            >>> sutra.upload("data.xlsx").upload("more.json")
        """
        print(f"\n📤 Uploading data...")
        
        # Handle DataFrame
        if isinstance(data, pd.DataFrame):
            name = name or "data"
            df = data
        else:
            # Load from file
            path = Path(data)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {data}")
            
            name = name or path.stem.replace(" ", "_").replace("-", "_")
            ext = path.suffix.lower()
            
            print(f"   📄 File: {path.name}")
            
            if ext == ".csv":
                df = pd.read_csv(path)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(path)
            elif ext == ".json":
                df = pd.read_json(path)
            elif ext == ".sql":
                with open(path) as f:
                    self.cursor.executescript(f.read())
                self.conn.commit()
                self._refresh_schema()
                print(f"✅ SQL executed!")
                return self
            else:
                raise ValueError(f"Unsupported format: {ext}")
        
        # Clean column names
        df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
        
        # Store in DB
        df.to_sql(name, self.conn, if_exists='replace', index=False)
        self.current_table = name
        self._refresh_schema()
        
        print(f"✅ Uploaded to table: {name}")
        print(f"   📊 {len(df)} rows × {len(df.columns)} columns")
        print(f"   🔤 Columns: {', '.join(df.columns[:5].tolist())}{' ...' if len(df.columns) > 5 else ''}")
        
        return self
    
    # ========================================================================
    # STEP 2: VIEW DATABASE
    # ========================================================================
    
    def tables(self) -> list:
        """List all tables."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [r[0] for r in self.cursor.fetchall()]
    
    def schema(self, table: Optional[str] = None):
        """
        Show database schema.
        
        Args:
            table: Specific table (shows all if None)
        """
        if not self.schema:
            self._refresh_schema()
        
        print("\n" + "="*70)
        print("📋 DATABASE SCHEMA")
        print("="*70)
        
        tables_to_show = [table] if table else self.schema.keys()
        
        for tbl in tables_to_show:
            if tbl in self.schema:
                print(f"\n📊 {tbl}")
                for col, dtype in self.schema[tbl].items():
                    print(f"   • {col:<25} {dtype}")
        
        print("="*70)
        return self
    
    def peek(self, table: Optional[str] = None, n: int = 5) -> pd.DataFrame:
        """
        View sample data.
        
        Args:
            table: Table name (uses current if None)
            n: Number of rows
        
        Returns:
            DataFrame with sample data
        """
        tbl = table or self.current_table
        if not tbl:
            print("❌ No table specified")
            return pd.DataFrame()
        
        df = pd.read_sql_query(f"SELECT * FROM {tbl} LIMIT {n}", self.conn)
        print(f"\n📊 Sample from '{tbl}' ({n} rows):")
        print(df.to_string(index=False))
        return df
    
    # ========================================================================
    # STEP 3: DIRECT SQL (NO API)
    # ========================================================================
    
    def sql(self, query: str, viz: bool = False) -> 'QueryResult':
        """
        Execute SQL directly (no API cost).
        
        Args:
            query: SQL query
            viz: Show visualization
        
        Returns:
            QueryResult object
        
        Example:
            >>> result = sutra.sql("SELECT * FROM sales WHERE amount > 1000")
            >>> print(result.data)
        """
        print(f"\n⚡ Executing SQL...")
        print(f"   {query}")
        
        try:
            df = pd.read_sql_query(query, self.conn)
            print(f"✅ Success! {len(df)} rows returned")
            
            fig = None
            if viz and not df.empty:
                fig = self._visualize(df, "SQL Query Result")
            
            return QueryResult(True, query, df, fig)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return QueryResult(False, query, pd.DataFrame(), None, str(e))
    
    # ========================================================================
    # STEP 4: NATURAL LANGUAGE QUERIES
    # ========================================================================
    
    def ask(self, question: str, viz: bool = False, table: Optional[str] = None) -> 'QueryResult':
        """
        Ask a question in natural language.
        
        Args:
            question: Your question in plain English
            viz: Show visualization (True/False)
            table: Specific table (uses current if None)
        
        Returns:
            QueryResult object
        
        Examples:
            >>> result = sutra.ask("What are total sales?")
            >>> result = sutra.ask("Show top 10 products", viz=True)
            >>> result = sutra.ask("Sales by region?", viz=True)
        """
        if not self.client:
            print("❌ No API key configured")
            return QueryResult(False, "", pd.DataFrame(), None, "No API key")
        
        print(f"\n🔍 Question: {question}")
        
        tbl = table or self.current_table
        if not tbl:
            print("❌ No table specified. Upload data first!")
            return QueryResult(False, "", pd.DataFrame(), None, "No table")
        
        # Check cache
        cache_key = hashlib.md5(f"{question}:{tbl}".encode()).hexdigest()
        if cache_key in self.cache:
            sql_query = self.cache[cache_key]
            print("   💾 From cache")
        else:
            # Generate SQL
            sql_query = self._generate_sql(question, tbl)
            self.cache[cache_key] = sql_query
        
        print(f"   📝 SQL: {sql_query}")
        
        # Execute
        try:
            df = pd.read_sql_query(sql_query, self.conn)
            print(f"✅ Success! {len(df)} rows")
            
            fig = None
            if viz and not df.empty:
                fig = self._visualize(df, question)
            
            return QueryResult(True, sql_query, df, fig)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return QueryResult(False, sql_query, pd.DataFrame(), None, str(e))
    
    # ========================================================================
    # STEP 5: INTERACTIVE QUERY (ASK USER FOR VIZ)
    # ========================================================================
    
    def interactive(self, question: str) -> 'QueryResult':
        """
        Ask question and prompt user for visualization.
        
        Args:
            question: Your question
        
        Returns:
            QueryResult object
        
        Example:
            >>> result = sutra.interactive("What are sales by region?")
            Do you want visualization? (yes/no): yes
        """
        print(f"\n🔍 Question: {question}")
        choice = input("💡 Do you want visualization? (yes/no): ").strip().lower()
        
        viz = choice in ['yes', 'y', 'yeah', 'yep', 'sure']
        return self.ask(question, viz=viz)
    
    # ========================================================================
    # UTILITIES
    # ========================================================================
    
    def export(self, data: pd.DataFrame, path: str, format: str = "csv"):
        """
        Export results to file.
        
        Args:
            data: DataFrame to export
            path: File path
            format: csv, excel, or json
        
        Example:
            >>> result = sutra.ask("Show all data")
            >>> sutra.export(result.data, "output.csv")
        """
        fmt = format.lower()
        if fmt == "csv":
            data.to_csv(path, index=False)
        elif fmt in ["excel", "xlsx"]:
            data.to_excel(path, index=False)
        elif fmt == "json":
            data.to_json(path, orient="records", indent=2)
        else:
            raise ValueError(f"Unknown format: {format}")
        
        print(f"✅ Exported to {path}")
        return self
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("✅ SUTRA closed")
    
    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================
    
    def _refresh_schema(self):
        """Update schema information."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in self.cursor.fetchall()]
        
        self.schema = {}
        for tbl in tables:
            self.cursor.execute(f"PRAGMA table_info({tbl})")
            self.schema[tbl] = {r[1]: r[2] for r in self.cursor.fetchall()}
    
    def _generate_sql(self, question: str, table: str) -> str:
        """Generate SQL using OpenAI."""
        schema_info = self.schema.get(table, {})
        schema_str = ", ".join([f"{col} ({dtype})" for col, dtype in schema_info.items()])
        
        prompt = f"""Convert this question to SQL.

Table: {table}
Columns: {schema_str}
Question: {question}

Return ONLY the SQL query. No explanations. Use SQLite syntax."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Return only SQL queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        sql = response.choices[0].message.content.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql
    
    def _visualize(self, df: pd.DataFrame, title: str):
        """Create visualization."""
        if not HAS_PLOTLY and not HAS_MATPLOTLIB:
            print("⚠️  Install plotly or matplotlib for visualizations")
            return None
        
        print("📊 Creating visualization...")
        
        if HAS_PLOTLY:
            return self._plotly_viz(df, title)
        else:
            return self._matplotlib_viz(df, title)
    
    def _plotly_viz(self, df: pd.DataFrame, title: str):
        """Create Plotly chart."""
        try:
            numeric = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical = df.select_dtypes(include=['object']).columns.tolist()
            
            if len(df) == 1 or not numeric:
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(df.columns)),
                    cells=dict(values=[df[c] for c in df.columns])
                )])
            elif categorical and numeric:
                fig = px.bar(df, x=categorical[0], y=numeric[0], title=title)
            elif len(numeric) >= 2:
                fig = px.line(df, y=numeric[0], title=title)
            else:
                fig = px.bar(df, y=df.columns[0], title=title)
            
            fig.show()
            print("✅ Chart displayed")
            return fig
        except Exception as e:
            print(f"⚠️  Viz error: {e}")
            return None
    
    def _matplotlib_viz(self, df: pd.DataFrame, title: str):
        """Create Matplotlib chart."""
        try:
            plt.figure(figsize=(10, 6))
            numeric = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric) > 0:
                df[numeric[0]].plot(kind='bar')
            else:
                df.iloc[:, 0].value_counts().plot(kind='bar')
            
            plt.title(title)
            plt.tight_layout()
            plt.show()
            print("✅ Chart displayed")
            return plt.gcf()
        except Exception as e:
            print(f"⚠️  Viz error: {e}")
            return None
    
    # Context manager
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def __repr__(self):
        return f"SUTRA(tables={len(self.schema)}, current='{self.current_table}')"


class QueryResult:
    """Result from a query."""
    
    def __init__(self, success: bool, sql: str, data: pd.DataFrame, viz, error: str = None):
        self.success = success
        self.sql = sql
        self.data = data
        self.viz = viz
        self.error = error
    
    def __repr__(self):
        if self.success:
            return f"QueryResult(rows={len(self.data)}, cols={len(self.data.columns)})"
        return f"QueryResult(error='{self.error}')"
    
    def show(self):
        """Display the data."""
        if self.success:
            print(self.data)
        else:
            print(f"Error: {self.error}")
        return self


# ============================================================================
# QUICK START FUNCTION
# ============================================================================

def quick_start(api_key: str, data_path: str, question: str, viz: bool = False):
    """
    One-liner for quick queries.
    
    Args:
        api_key: OpenAI API key
        data_path: Path to data file
        question: Your question
        viz: Show visualization
    
    Returns:
        QueryResult
    
    Example:
        >>> from sutra import quick_start
        >>> result = quick_start("sk-...", "data.csv", "Show total sales", viz=True)
    """
    with SUTRA(api_key=api_key) as sutra:
        sutra.upload(data_path)
        return sutra.ask(question, viz=viz)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                      SUTRA v0.1.0                            ║
║          Simple Unified Tool for Relational Analysis         ║
╚══════════════════════════════════════════════════════════════╝

Quick Start:
    pip install sutra
    
    from sutra import SUTRA
    
    sutra = SUTRA(api_key="your-key")
    sutra.upload("data.csv")
    result = sutra.ask("Show me total sales", viz=True)

Documentation: See example notebook for complete guide
""")
