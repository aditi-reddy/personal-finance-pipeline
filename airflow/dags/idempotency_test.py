"""
Idempotency Test DAG
Tests that the pipeline can be safely re-run without duplicating data
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2

default_args = {
    'owner': 'aditi',
    'retries': 1,
}

def test_idempotency(**context):
    """Test that re-running doesn't create duplicates"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='personal_finance_warehouse',
            user='aditireddy',
            password=''
        )
        cur = conn.cursor()
        
        print("\n" + "=" * 60)
        print("🧪 IDEMPOTENCY TEST")
        print("=" * 60)
        
        # Check for duplicate transaction IDs
        cur.execute("""
            SELECT transaction_id, COUNT(*) as count
            FROM staging_transactions
            GROUP BY transaction_id
            HAVING COUNT(*) > 1;
        """)
        
        duplicates = cur.fetchall()
        
        if duplicates:
            print(f"❌ FAILED: Found {len(duplicates)} duplicate transaction IDs!")
            for txn_id, count in duplicates[:5]:
                print(f"   {txn_id}: {count} copies")
            raise ValueError("Idempotency test failed - duplicates found")
        else:
            print("✅ PASSED: No duplicate transaction IDs found")
        
        # Check PRIMARY KEY constraint exists
        cur.execute("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'staging_transactions'
            AND constraint_type = 'PRIMARY KEY';
        """)
        
        pk_exists = cur.fetchone()
        
        if pk_exists:
            print(f"✅ PRIMARY KEY constraint exists: {pk_exists[0]}")
        else:
            print("⚠️  WARNING: No PRIMARY KEY constraint found")
        
        # Show table stats
        cur.execute("SELECT COUNT(*) FROM staging_transactions;")
        total_rows = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT transaction_id) FROM staging_transactions;")
        unique_ids = cur.fetchone()[0]
        
        print(f"\n📊 Table Statistics:")
        print(f"   Total rows: {total_rows}")
        print(f"   Unique IDs: {unique_ids}")
        print(f"   Match: {'✅ YES' if total_rows == unique_ids else '❌ NO'}")
        
        # Show pipeline run history
        try:
            cur.execute("""
                SELECT run_id, run_date, rows_loaded, total_rows_in_table, status
                FROM pipeline_runs
                ORDER BY run_date DESC
                LIMIT 5;
            """)
            
            runs = cur.fetchall()
            
            if runs:
                print(f"\n📜 Recent Pipeline Runs:")
                for run_id, run_date, loaded, total, status in runs:
                    print(f"   {run_date}: Loaded {loaded} rows, Total {total} - {status}")
        except:
            print("\nℹ️  Pipeline runs table not yet created")
        
        print("=" * 60 + "\n")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Idempotency test failed: {str(e)}")
        raise


with DAG(
    dag_id='idempotency_test',
    default_args=default_args,
    description='Tests pipeline idempotency',
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['testing', 'idempotency'],
) as dag:

    test = PythonOperator(
        task_id='test_idempotency',
        python_callable=test_idempotency,
    )