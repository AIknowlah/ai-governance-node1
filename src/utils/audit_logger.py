"""
BigQuery Audit Logger
Writes governance-compliant logs to Singapore region
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

class AuditLogger:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.dataset_id = os.getenv("BIGQUERY_DATASET")
        self.table_id = os.getenv("BIGQUERY_TABLE")
        self.client = bigquery.Client(project=self.project_id)
        
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
    
    def log_node_execution(
        self,
        request_id: str,
        node_name: str,
        input_hash: str,
        output_hash: str,
        pdpa_flags: List[str],
        ai_verify_principles: List[str],
        execution_time_ms: int,
        error_message: str = None,
        metadata: Dict[str, Any] = None
    ):
        """
        Log a single node execution to BigQuery.
        
        Cost Estimate: ~0.00001 USD per log entry (Singapore region)
        """
        row = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "node_name": node_name,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "pdpa_flags": pdpa_flags,
            "ai_verify_principles": ai_verify_principles,
            "execution_time_ms": execution_time_ms,
            "error_message": error_message,
            "metadata": json.dumps(metadata or {})
        }
        
        try:
            errors = self.client.insert_rows_json(self.table_ref, [row])
            
            if errors:
                print(f"❌ BigQuery insert errors: {errors}")
            else:
                print(f"✅ Logged to BigQuery: {node_name} ({execution_time_ms}ms)")
        
        except Exception as e:
            print(f"⚠️  Audit log failed: {e}")