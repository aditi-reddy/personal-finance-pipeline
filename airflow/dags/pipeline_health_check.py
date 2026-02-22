"""
Pipeline Health Check DAG
Monitors the health of the ETL pipeline
Runs every hour
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2

default_args = {
    'owner': 'aditi',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def check_database_connection(**context):
    """Check if PostgreSQL is accessible"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='personal_finance_warehouse',
            user='aditireddy',
            password=''
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        print("✅ Database connection: OK")
        return True
    except Exception as e:
        print(f"❌ Database connection: FAILED - {str(e)}")
        raise


def check_latest_data(**context):
    """Check when data was last loaded"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='personal_finance_warehouse',
            user='aditireddy',
            password=''
        )
        cur = conn.cursor()
        
        # Check if table exists and has data
        cur.execute("""
            SELECT 
                COUNT(*) as total_rows,
                MAX(processed_timestamp) as last_load
            FROM staging_transactions;
        """)
        
        result = cur.fetchone()
        total_rows = result[0]
        last_load = result[1]
        
        cur.close()
        conn.close()
        
        print("=" * 60)
        print("📊 DATA HEALTH CHECK")
        print("=" * 60)
        print(f"Total Rows: {total_rows:,}")
        print(f"Last Load: {last_load}")
        
        # Alert if no data loaded in last 48 hours
        if last_load:
            from datetime import datetime
            hours_since_load = (datetime.now() - last_load.replace(tzinfo=None)).total_seconds() / 3600
            print(f"Hours Since Last Load: {hours_since_load:.1f}")
            
            if hours_since_load > 48:
                print("⚠️  WARNING: No data loaded in last 48 hours!")
            else:
                print("✅ Data is fresh")
        
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Data health check failed: {str(e)}")
        raise


def check_airflow_health(**context):
    """Check Airflow system health"""
    import os
    
    print("=" * 60)
    print("🏥 AIRFLOW HEALTH CHECK")
    print("=" * 60)
    
    # Check disk space
    stat = os.statvfs('/tmp')
    free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    print(f"Free Disk Space: {free_space_gb:.2f} GB")
    
    if free_space_gb < 1:
        print("⚠️  WARNING: Low disk space!")
    else:
        print("✅ Disk space: OK")
    
    # Check log file size
    log_dir = os.path.expanduser('~/Desktop/personal-finance-pipeline/personal-finance-pipeline/airflow/logs')
    if os.path.exists(log_dir):
        total_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, dirnames, filenames in os.walk(log_dir)
            for filename in filenames
        )
        total_size_mb = total_size / (1024**2)
        print(f"Log Directory Size: {total_size_mb:.2f} MB")
        
        if total_size_mb > 1000:
            print("⚠️  WARNING: Large log directory! Consider cleanup.")
        else:
            print("✅ Log size: OK")
    
    print("=" * 60)
    
    return True


with DAG(
    dag_id='pipeline_health_check',
    default_args=default_args,
    description='Monitors ETL pipeline health - Runs hourly',
    schedule='0 * * * *',  # Every hour
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['monitoring', 'health-check'],
) as dag:

    check_db = PythonOperator(
        task_id='check_database',
        python_callable=check_database_connection,
    )

    check_data = PythonOperator(
        task_id='check_latest_data',
        python_callable=check_latest_data,
    )

    check_system = PythonOperator(
        task_id='check_airflow_health',
        python_callable=check_airflow_health,
    )

    # Run all checks in parallel
    [check_db, check_data, check_system]