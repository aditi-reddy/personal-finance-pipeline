"""
Data Quality Monitoring DAG
Runs daily quality checks on the data warehouse
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import pandas as pd
from data_quality_checks import DataQualityValidator

default_args = {
    'owner': 'aditi',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

def check_warehouse_quality(**context):
    """Run quality checks on warehouse data"""
    
    print("🔍 Checking data warehouse quality...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='personal_finance_warehouse',
            user='aditireddy',
            password=''
        )
        
        # Read data from warehouse
        query = "SELECT * FROM staging_transactions;"
        df = pd.read_sql(query, conn)
        conn.close()
        
        print(f"📊 Loaded {len(df)} rows from warehouse")
        
        # Run quality checks
        validator = DataQualityValidator(df)
        all_passed, issues, warnings, metrics = validator.run_all_checks()
        
        # Log results
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_rows': len(df),
            'issues': len(issues),
            'warnings': len(warnings),
            'status': 'PASSED' if all_passed else 'FAILED'
        }
        
        # Save results to log file
        import json
        log_file = '/tmp/data_quality_log.json'
        
        try:
            with open(log_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append(results)
        
        # Keep only last 30 days
        if len(history) > 30:
            history = history[-30:]
        
        with open(log_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"✅ Quality results saved to {log_file}")
        
        # Push to XCom
        context['ti'].xcom_push(key='quality_results', value=results)
        
        if not all_passed:
            raise ValueError(f"Quality checks failed with {len(issues)} issues")
        
        return results
        
    except Exception as e:
        print(f"❌ Warehouse quality check failed: {str(e)}")
        raise


def generate_quality_report(**context):
    """Generate a quality trend report"""
    
    import json
    log_file = '/tmp/data_quality_log.json'
    
    try:
        with open(log_file, 'r') as f:
            history = json.load(f)
        
        print("\n" + "=" * 60)
        print("📈 DATA QUALITY TREND REPORT")
        print("=" * 60)
        
        if len(history) > 0:
            print(f"Total Checks: {len(history)}")
            
            passed = sum(1 for h in history if h['status'] == 'PASSED')
            failed = len(history) - passed
            
            print(f"Passed: {passed} ({passed/len(history)*100:.1f}%)")
            print(f"Failed: {failed} ({failed/len(history)*100:.1f}%)")
            
            # Show recent results
            print("\nRecent Checks:")
            for record in history[-5:]:
                status_icon = "✅" if record['status'] == 'PASSED' else "❌"
                print(f"  {status_icon} {record['timestamp']}: {record['total_rows']} rows, {record['issues']} issues, {record['warnings']} warnings")
        
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"⚠️  Could not generate trend report: {str(e)}")


with DAG(
    dag_id='data_quality_monitoring',
    default_args=default_args,
    description='Daily data quality monitoring',
    schedule='0 3 * * *',  # Daily at 3 AM (after ETL runs at 2 AM)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['quality', 'monitoring'],
) as dag:

    check_quality = PythonOperator(
        task_id='check_warehouse_quality',
        python_callable=check_warehouse_quality,
    )

    generate_report = PythonOperator(
        task_id='generate_quality_report',
        python_callable=generate_quality_report,
    )

    check_quality >> generate_report