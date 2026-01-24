"""
Load CSV data into SQLite database for SQL analysis
Author: [Your Name]
"""

import pandas as pd
import sqlite3
import os

def create_database():
    """Create SQLite database and load transaction data"""
    
    # Check if CSV exists
    if not os.path.exists('creditcard.csv'):
        print("Error: creditcard.csv not found!")
        print("Please download the dataset first.")
        return
    
    print("Loading CSV data...")
    df = pd.read_csv('creditcard.csv')
    
    print(f"Data loaded: {len(df)} transactions")
    
    # Connect to SQLite database (creates it if doesn't exist)
    print("\nConnecting to SQLite database...")
    conn = sqlite3.connect('fraud_detection.db')
    
    # Prepare data for SQL
    df_sql = df.copy()
    df_sql.columns = df_sql.columns.str.lower()  # lowercase column names
    
    # Rename columns for SQL compatibility
    column_mapping = {
        'time': 'time_seconds',
        'class': 'is_fraud'
    }
    df_sql = df_sql.rename(columns=column_mapping)
    
    # Add transaction_id
    df_sql.insert(0, 'transaction_id', range(1, len(df_sql) + 1))
    
    # Load data into SQLite
    print("Loading data into SQLite...")
    df_sql.to_sql('transactions', conn, if_exists='replace', index=False)
    
    # Create indexes
    print("Creating indexes...")
    cursor = conn.cursor()
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fraud ON transactions(is_fraud)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_amount ON transactions(amount)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_time ON transactions(time_seconds)')
    conn.commit()
    
    print("\n" + "="*50)
    print("DATABASE CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"Database: fraud_detection.db")
    print(f"Table: transactions")
    print(f"Records: {len(df_sql)}")
    
    # Run a sample query
    print("\nSample Query - Fraud Statistics:")
    query = """
    SELECT 
        is_fraud,
        COUNT(*) as count,
        ROUND(AVG(amount), 2) as avg_amount
    FROM transactions
    GROUP BY is_fraud
    """
    
    result = pd.read_sql_query(query, conn)
    print(result)
    
    conn.close()
    print("\nYou can now run SQL queries using fraud_detection.db")


def run_sql_analysis():
    """Run SQL analysis queries"""
    
    if not os.path.exists('fraud_detection.db'):
        print("Database not found! Run create_database() first.")
        return
    
    conn = sqlite3.connect('fraud_detection.db')
    
    print("="*50)
    print("SQL ANALYSIS RESULTS")
    print("="*50)
    
    # Query 1: Basic Statistics
    print("\n1. TRANSACTION OVERVIEW")
    print("-" * 40)
    query1 = """
    SELECT 
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_transactions,
        ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_percentage
    FROM transactions
    """
    print(pd.read_sql_query(query1, conn))
    
    # Query 2: Amount Analysis
    print("\n2. AMOUNT STATISTICS BY FRAUD STATUS")
    print("-" * 40)
    query2 = """
    SELECT 
        is_fraud,
        COUNT(*) as count,
        ROUND(MIN(amount), 2) as min_amount,
        ROUND(AVG(amount), 2) as avg_amount,
        ROUND(MAX(amount), 2) as max_amount,
        ROUND(SUM(amount), 2) as total_amount
    FROM transactions
    GROUP BY is_fraud
    """
    print(pd.read_sql_query(query2, conn))
    
    # Query 3: High-risk transactions
    print("\n3. TOP 10 HIGH-VALUE FRAUD TRANSACTIONS")
    print("-" * 40)
    query3 = """
    SELECT 
        transaction_id,
        ROUND(amount, 2) as amount,
        ROUND(time_seconds / 3600, 2) as hour
    FROM transactions
    WHERE is_fraud = 1
    ORDER BY amount DESC
    LIMIT 10
    """
    print(pd.read_sql_query(query3, conn))
    
    # Query 4: Time-based patterns
    print("\n4. PEAK FRAUD HOURS")
    print("-" * 40)
    query4 = """
    SELECT 
        (time_seconds / 3600) as hour,
        COUNT(*) as total_transactions,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_rate
    FROM transactions
    GROUP BY hour
    HAVING fraud_count > 0
    ORDER BY fraud_rate DESC
    LIMIT 5
    """
    print(pd.read_sql_query(query4, conn))
    
    # Query 5: Amount ranges
    print("\n5. FRAUD DISTRIBUTION BY AMOUNT RANGE")
    print("-" * 40)
    query5 = """
    SELECT 
        CASE 
            WHEN amount < 10 THEN '0-10'
            WHEN amount < 50 THEN '10-50'
            WHEN amount < 100 THEN '50-100'
            WHEN amount < 500 THEN '100-500'
            ELSE '500+'
        END as amount_range,
        COUNT(*) as total_count,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
        ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_percentage
    FROM transactions
    GROUP BY amount_range
    """
    print(pd.read_sql_query(query5, conn))
    
    conn.close()


if __name__ == "__main__":
    # Step 1: Create database
    create_database()
    
    # Step 2: Run analysis
    print("\n")
    run_sql_analysis()