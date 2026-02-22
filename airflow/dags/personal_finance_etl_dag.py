"""
Personal Finance ETL DAG
Automates: S3 Download → Transform → Load to PostgreSQL
Author: Aditi Reddy
Schedule: Daily at 2:00 AM
Enhanced with: Monitoring, Alerts, Quality Checks, Performance Optimization, Idempotency
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import logging
import time
from data_quality_checks import DataQualityValidator

# ========================================
# CONFIGURATION
# ========================================

# AWS Configuration
AWS_BUCKET = 'aditi-finance-bronze-raw-2025'
AWS_KEY = 'transactions/year=2023/month=01/transactions.csv'
LOCAL_FILE = '/tmp/airflow_transactions.csv'
TRANSFORMED_FILE = '/tmp/airflow_transactions_transformed.csv'

# PostgreSQL Configuration
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'personal_finance_warehouse',
    'user': 'aditireddy',
    'password': ''  # Empty if no password
}

# Default arguments for all tasks
default_args = {
    'owner': 'aditi',
    'depends_on_past': False,
    'email': ['aditi.reddy@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,  # Retry 3 times before failing
    'retry_delay': timedelta(minutes=2),  # Wait 2 minutes between retries
    'retry_exponential_backoff': True,  # Increase wait time exponentially
    'max_retry_delay': timedelta(minutes=10),  # Max wait time
    'execution_timeout': timedelta(minutes=30),  # Fail if task runs > 30 min
}

# ========================================
# CALLBACK FUNCTIONS
# ========================================

def task_failure_alert(context):
    """
    Called when a task fails
    """
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    exception = context.get('exception')
    
    print("\n" + "=" * 60)
    print("🚨 TASK FAILURE ALERT")
    print("=" * 60)
    print(f"DAG: {dag_id}")
    print(f"Task: {task_id}")
    print(f"Error: {exception}")
    print(f"Try Number: {task_instance.try_number}")
    print("=" * 60)
    print("📧 In production, this would send an email/Slack notification")
    print("=" * 60 + "\n")


def task_success_callback(context):
    """
    Called when a task succeeds
    """
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    
    print(f"✅ Task {task_id} completed successfully!")


def dag_success_callback(context):
    """
    Called when entire DAG succeeds
    """
    dag_run = context['dag_run']
    
    print("\n" + "=" * 60)
    print("🎉 ENTIRE PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"DAG: {dag_run.dag_id}")
    print(f"Run ID: {dag_run.run_id}")
    print("=" * 60)
    print("📧 In production, this would send a success notification")
    print("=" * 60 + "\n")


# ========================================
# TASK FUNCTIONS
# ========================================

def download_from_s3(**context):
    """
    Task 1: Download transactions.csv from S3
    """
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("TASK: Download from S3")
    logger.info("=" * 60)
    logger.info(f"📥 Bucket: {AWS_BUCKET}")
    logger.info(f"📄 File: {AWS_KEY}")
    logger.info(f"💾 Destination: {LOCAL_FILE}")
    
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        logger.info("✅ S3 client initialized")
        
        # Download file
        logger.info("⬇️  Starting download...")
        s3_client.download_file(AWS_BUCKET, AWS_KEY, LOCAL_FILE)
        
        # Verify download
        if not os.path.exists(LOCAL_FILE):
            raise FileNotFoundError(f"Failed to download file to {LOCAL_FILE}")
        
        file_size = os.path.getsize(LOCAL_FILE)
        logger.info(f"✅ Download successful!")
        logger.info(f"📊 File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        
        # Quick preview
        df = pd.read_csv(LOCAL_FILE)
        logger.info(f"📊 Total rows: {len(df):,}")
        logger.info(f"📊 Columns: {', '.join(df.columns)}")
        
        # Push metadata to XCom
        context['ti'].xcom_push(key='row_count', value=len(df))
        context['ti'].xcom_push(key='file_path', value=LOCAL_FILE)
        context['ti'].xcom_push(key='file_size_bytes', value=file_size)
        
        logger.info("=" * 60)
        logger.info("✅ TASK COMPLETED")
        logger.info("=" * 60)
        
        return LOCAL_FILE
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ TASK FAILED")
        logger.error("=" * 60)
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error("=" * 60)
        raise


def validate_data(**context):
    """
    Task 2: Validate data quality with comprehensive checks
    """
    print("🔍 Starting comprehensive data quality validation...")
    
    try:
        # Read the file
        df = pd.read_csv(LOCAL_FILE)
        
        # Run comprehensive quality checks
        validator = DataQualityValidator(df)
        all_passed, issues, warnings, metrics = validator.run_all_checks()
        
        # Prepare results summary
        results = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'issues_count': len(issues),
            'warnings_count': len(warnings),
            'checks_passed': all_passed,
            'issues': issues,
            'warnings': warnings,
            'metrics': metrics
        }
        
        # Push results to XCom
        context['ti'].xcom_push(key='validation_results', value=results)
        
        # Fail if critical issues found
        if not all_passed:
            error_msg = f"Data quality validation failed with {len(issues)} critical issues"
            print(f"\n❌ {error_msg}")
            raise ValueError(error_msg)
        
        # Warn if warnings found but continue
        if warnings:
            print(f"\n⚠️  Pipeline continuing with {len(warnings)} warnings")
        
        print("\n✅ Data quality validation passed!")
        
        return results
        
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        raise


def transform_data(**context):
    """
    Task 3: Transform data for warehouse
    """
    print("🔄 Starting data transformation...")
    
    try:
        # Read the file
        df = pd.read_csv(LOCAL_FILE)
        print(f"📊 Loaded {len(df)} rows for transformation")
        
        # Add derived columns
        df['transaction_date'] = pd.to_datetime(df['date'])
        df['year'] = df['transaction_date'].dt.year
        df['month'] = df['transaction_date'].dt.month
        df['day_of_week'] = df['transaction_date'].dt.dayofweek
        df['week_of_year'] = df['transaction_date'].dt.isocalendar().week
        
        # Add transaction metadata
        df['processed_timestamp'] = datetime.now()
        
        print("✅ Transformations applied:")
        print("  - transaction_date (parsed)")
        print("  - year, month, day_of_week")
        print("  - week_of_year")
        print("  - processed_timestamp")
        
        # Save transformed data
        df.to_csv(TRANSFORMED_FILE, index=False)
        print(f"💾 Transformed data saved to: {TRANSFORMED_FILE}")
        
        # Preview
        print("\n📊 Sample of transformed data:")
        print(df.head(3).to_string())
        
        # Push metadata
        context['ti'].xcom_push(key='transformed_file', value=TRANSFORMED_FILE)
        context['ti'].xcom_push(key='transformed_rows', value=len(df))
        
        return TRANSFORMED_FILE
        
    except Exception as e:
        print(f"❌ Transformation failed: {str(e)}")
        raise


def load_to_postgres(**context):
    """
    Task 4: Load data into PostgreSQL warehouse (OPTIMIZED & IDEMPOTENT)
    """
    print("📤 Starting PostgreSQL load (OPTIMIZED & IDEMPOTENT)...")
    
    start_time = time.time()
    
    try:
        # Read transformed data
        df = pd.read_csv(TRANSFORMED_FILE)
        print(f"📊 Loading {len(df)} rows to PostgreSQL")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'staging_transactions'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if table_exists:
            # Get existing transaction IDs to avoid duplicates
            cur.execute("SELECT transaction_id FROM staging_transactions;")
            existing_ids = set(row[0] for row in cur.fetchall())
            initial_count = len(existing_ids)
            
            print(f"ℹ️  Table exists with {initial_count} existing rows")
            print("🔄 Running in IDEMPOTENT mode - will skip duplicates")
            
            # Filter out duplicates
            df_new = df[~df['transaction_id'].isin(existing_ids)]
            
            if len(df_new) == 0:
                print("✅ All transactions already loaded - nothing to do")
                print(f"📊 Total rows in table: {initial_count}")
                
                context['ti'].xcom_push(key='rows_loaded', value=0)
                context['ti'].xcom_push(key='rows_skipped', value=len(df))
                context['ti'].xcom_push(key='total_rows', value=initial_count)
                
                return initial_count
            
            print(f"📊 Found {len(df_new)} new transactions (skipping {len(df) - len(df_new)} duplicates)")
            df = df_new
        else:
            # Create table if it doesn't exist
            print("🗄️  Creating staging table (first run)...")
            create_table_sql = """
            CREATE TABLE staging_transactions (
                transaction_id VARCHAR(50) PRIMARY KEY,
                date DATE,
                merchant VARCHAR(100),
                category VARCHAR(50),
                amount DECIMAL(10,2),
                payment_method VARCHAR(50),
                transaction_date TIMESTAMP,
                year INT,
                month INT,
                day_of_week INT,
                week_of_year INT,
                processed_timestamp TIMESTAMP
            );
            """
            cur.execute(create_table_sql)
            print("✅ Staging table created with PRIMARY KEY constraint")
        
        # OPTIMIZED: Batch insert using execute_values
        print("📥 Inserting data using BATCH INSERT (optimized)...")
        insert_start = time.time()
        
        # Prepare data as list of tuples
        data_tuples = [
            (
                row['transaction_id'],
                row['date'],
                row['merchant'],
                row['category'],
                row['amount'],
                row['payment_method'],
                row['transaction_date'],
                row['year'],
                row['month'],
                row['day_of_week'],
                row['week_of_year'],
                row['processed_timestamp']
            )
            for _, row in df.iterrows()
        ]
        
        # Batch insert with ON CONFLICT DO NOTHING (idempotent)
        insert_query = """
            INSERT INTO staging_transactions 
            (transaction_id, date, merchant, category, amount, payment_method,
             transaction_date, year, month, day_of_week, week_of_year, processed_timestamp)
            VALUES %s
            ON CONFLICT (transaction_id) DO NOTHING
        """
        
        execute_values(cur, insert_query, data_tuples, page_size=100)
        
        insert_duration = time.time() - insert_start
        
        # Commit transaction
        conn.commit()
        
        # Verify load
        cur.execute("SELECT COUNT(*) FROM staging_transactions;")
        total_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        total_duration = time.time() - start_time
        
        rows_inserted = len(df)
        
        print(f"✅ Successfully loaded {rows_inserted} NEW rows to staging_transactions")
        print(f"📊 Total rows in table: {total_count}")
        print(f"⚡ Insert duration: {insert_duration:.2f} seconds")
        print(f"⚡ Total load duration: {total_duration:.2f} seconds")
        
        if rows_inserted > 0:
            print(f"📊 Throughput: {rows_inserted/total_duration:.0f} rows/second")
        
        # Push performance metrics
        context['ti'].xcom_push(key='rows_loaded', value=rows_inserted)
        context['ti'].xcom_push(key='total_rows', value=total_count)
        context['ti'].xcom_push(key='load_duration', value=total_duration)
        context['ti'].xcom_push(key='insert_duration', value=insert_duration)
        
        if rows_inserted > 0:
            context['ti'].xcom_push(key='throughput', value=rows_inserted/total_duration)
        
        return total_count
        
    except Exception as e:
        print(f"❌ PostgreSQL load failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise


def cleanup_temp_files(**context):
    """
    Task 5: Clean up temporary files
    """
    print("🧹 Cleaning up temporary files...")
    
    files_to_delete = [LOCAL_FILE, TRANSFORMED_FILE]
    deleted_count = 0
    
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️  Deleted: {file_path}")
                deleted_count += 1
            else:
                print(f"⏭️  Skipped (not found): {file_path}")
        except Exception as e:
            print(f"⚠️  Failed to delete {file_path}: {str(e)}")
    
    print(f"✅ Cleanup complete! Deleted {deleted_count} files")
    
    return deleted_count


def print_pipeline_summary(**context):
    """
    Task 6: Print pipeline execution summary (ENHANCED with performance metrics)
    """
    print("\n" + "=" * 60)
    print("📊 PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    
    # Get data from previous tasks via XCom
    ti = context['ti']
    
    row_count = ti.xcom_pull(task_ids='download_from_s3', key='row_count')
    validation = ti.xcom_pull(task_ids='validate_data', key='validation_results')
    rows_loaded = ti.xcom_pull(task_ids='load_to_postgres', key='rows_loaded')
    total_rows = ti.xcom_pull(task_ids='load_to_postgres', key='total_rows')
    load_duration = ti.xcom_pull(task_ids='load_to_postgres', key='load_duration')
    throughput = ti.xcom_pull(task_ids='load_to_postgres', key='throughput')
    
    # Get scheduling info
    dag_run = context['dag_run']
    is_scheduled = dag_run.run_type == 'scheduled'
    
    print(f"🔄 Run Type: {'SCHEDULED' if is_scheduled else 'MANUAL'}")
    print(f"📥 Downloaded Rows: {row_count}")
    print(f"✅ Validation: PASSED")
    
    if validation:
        issues = validation.get('issues_count', 0)
        warnings = validation.get('warnings_count', 0)
        print(f"   - Issues: {issues}")
        print(f"   - Warnings: {warnings}")
    
    print(f"🔄 Transformed: {row_count} rows")
    print(f"📤 Loaded to PostgreSQL: {rows_loaded} NEW rows")
    print(f"📊 Total rows in table: {total_rows}")
    
    # Performance metrics
    if load_duration and throughput:
        print(f"⚡ Load Duration: {load_duration:.2f} seconds")
        print(f"⚡ Throughput: {throughput:.0f} rows/second")
    
    print(f"⏱️  Pipeline Run ID: {dag_run.run_id}")
    print(f"📅 Run Date: {dag_run.start_date}")
    print(f"⏰ Schedule: Daily at 2:00 AM")
    print("=" * 60)
    print("✅ ETL PIPELINE COMPLETED SUCCESSFULLY! 🎉")
    print("=" * 60 + "\n")


def benchmark_performance(**context):
    """
    Task 7: Benchmark and report pipeline performance
    """
    ti = context['ti']
    
    # Get performance metrics from tasks
    load_duration = ti.xcom_pull(task_ids='load_to_postgres', key='load_duration')
    throughput = ti.xcom_pull(task_ids='load_to_postgres', key='throughput')
    rows_loaded = ti.xcom_pull(task_ids='load_to_postgres', key='rows_loaded')
    
    print("\n" + "=" * 60)
    print("⚡ PERFORMANCE BENCHMARK REPORT")
    print("=" * 60)
    
    if load_duration:
        print(f"Database Load Duration: {load_duration:.2f} seconds")
        print(f"Rows Loaded: {rows_loaded:,} NEW rows")
        
        if throughput and rows_loaded > 0:
            print(f"Throughput: {throughput:.0f} rows/second")
            
            # Performance benchmarks
            if throughput > 400:
                print("🚀 EXCELLENT performance (>400 rows/sec)")
            elif throughput > 200:
                print("✅ GOOD performance (>200 rows/sec)")
            elif throughput > 100:
                print("⚠️  ACCEPTABLE performance (>100 rows/sec)")
            else:
                print("❌ SLOW performance (<100 rows/sec) - needs optimization")
        else:
            print("ℹ️  No new rows to load (idempotent re-run)")
    
    # Get DAG run duration
    dag_run = context['dag_run']
    if dag_run.start_date:
        current_time = datetime.now(dag_run.start_date.tzinfo)
        dag_duration = (current_time - dag_run.start_date).total_seconds()
        print(f"\nTotal Pipeline Duration: {dag_duration:.2f} seconds")
    
    print("=" * 60 + "\n")
    
    # Save benchmark to file (only if rows were loaded)
    if rows_loaded and rows_loaded > 0:
        import json
        
        benchmark_data = {
            'timestamp': datetime.now().isoformat(),
            'rows': rows_loaded,
            'load_duration': load_duration,
            'throughput': throughput,
        }
        
        benchmark_file = '/tmp/pipeline_benchmarks.json'
        try:
            with open(benchmark_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append(benchmark_data)
        
        # Keep last 30 runs
        if len(history) > 30:
            history = history[-30:]
        
        with open(benchmark_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"📊 Benchmark saved to {benchmark_file}")


def track_pipeline_run(**context):
    """
    Task 8: Track pipeline run metadata in database
    """
    print("📝 Tracking pipeline run metadata...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        
        # Create pipeline_runs table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id VARCHAR(100) PRIMARY KEY,
                run_date TIMESTAMP,
                run_type VARCHAR(20),
                rows_processed INT,
                rows_loaded INT,
                total_rows_in_table INT,
                load_duration DECIMAL(10,2),
                throughput DECIMAL(10,2),
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Get metrics from XCom
        ti = context['ti']
        dag_run = context['dag_run']
        
        rows_processed = ti.xcom_pull(task_ids='download_from_s3', key='row_count')
        rows_loaded = ti.xcom_pull(task_ids='load_to_postgres', key='rows_loaded')
        total_rows = ti.xcom_pull(task_ids='load_to_postgres', key='total_rows')
        load_duration = ti.xcom_pull(task_ids='load_to_postgres', key='load_duration')
        throughput = ti.xcom_pull(task_ids='load_to_postgres', key='throughput')
        
        # Insert run metadata
        cur.execute("""
            INSERT INTO pipeline_runs 
            (run_id, run_date, run_type, rows_processed, rows_loaded, 
             total_rows_in_table, load_duration, throughput, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (run_id) DO UPDATE SET
                status = EXCLUDED.status,
                rows_loaded = EXCLUDED.rows_loaded,
                total_rows_in_table = EXCLUDED.total_rows_in_table
        """, (
            dag_run.run_id,
            dag_run.start_date,
            dag_run.run_type,
            rows_processed,
            rows_loaded,
            total_rows,
            load_duration,
            throughput,
            'success'
        ))
        
        conn.commit()
        
        print(f"✅ Pipeline run tracked: {dag_run.run_id}")
        print(f"   Rows processed: {rows_processed}")
        print(f"   Rows loaded: {rows_loaded}")
        print(f"   Total in table: {total_rows}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️  Failed to track pipeline run: {str(e)}")
        # Don't fail the pipeline if metadata tracking fails


# ========================================
# DAG DEFINITION
# ========================================

with DAG(
    dag_id='personal_finance_etl',
    default_args=default_args,
    description='ETL Pipeline: S3 → Transform → PostgreSQL - Runs Daily at 2 AM',
    schedule='0 2 * * *',  # Daily at 2:00 AM (cron format)
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Don't run for past dates
    max_active_runs=1,  # Only 1 pipeline run at a time
    tags=['etl', 'personal-finance', 'production', 'scheduled', 'optimized', 'idempotent'],
    on_success_callback=dag_success_callback,  # Called when DAG succeeds
    on_failure_callback=task_failure_alert,  # Called when DAG fails
    dagrun_timeout=timedelta(hours=1),  # Fail entire DAG if it runs > 1 hour
) as dag:

    # Task 1: Download from S3
    task_download = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        on_failure_callback=task_failure_alert,
        sla=timedelta(minutes=5),
    )

    # Task 2: Validate data quality
    task_validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        on_failure_callback=task_failure_alert,
        sla=timedelta(minutes=2),
    )

    # Task 3: Transform data
    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        on_failure_callback=task_failure_alert,
        sla=timedelta(minutes=3),
    )

    # Task 4: Load to PostgreSQL (OPTIMIZED & IDEMPOTENT)
    task_load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres,
        on_failure_callback=task_failure_alert,
        on_success_callback=task_success_callback,
        sla=timedelta(minutes=10),
    )

    # Task 5: Cleanup temporary files
    task_cleanup = PythonOperator(
        task_id='cleanup_temp_files',
        python_callable=cleanup_temp_files,
        on_failure_callback=task_failure_alert,
        sla=timedelta(minutes=1),
    )

    # Task 6: Print summary
    task_summary = PythonOperator(
        task_id='print_summary',
        python_callable=print_pipeline_summary,
        on_failure_callback=task_failure_alert,
        on_success_callback=task_success_callback,
        sla=timedelta(minutes=1),
    )

    # Task 7: Benchmark performance
    task_benchmark = PythonOperator(
        task_id='benchmark_performance',
        python_callable=benchmark_performance,
        sla=timedelta(minutes=1),
    )

    # Task 8: Track pipeline run
    task_track = PythonOperator(
        task_id='track_pipeline_run',
        python_callable=track_pipeline_run,
        sla=timedelta(minutes=1),
    )

    # Define pipeline flow (8 tasks)
    task_download >> task_validate >> task_transform >> task_load >> task_cleanup >> task_summary >> task_benchmark >> task_track