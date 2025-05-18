from supabase import create_client, Client
from app.config import settings
import logging

class DatabaseService:
    def __init__(self):
        try:
            self.client: Client = create_client(settings.supabase_url, settings.supabase_key)
        except Exception as e:
            logging.error(f"Failed to initialize Supabase client: {e}")
            raise

    def insert_record(self, table: str, data: dict):
        try:
            response = self.client.table(table).insert(data).execute()
            return response
        except Exception as e:
            logging.error(f"Insert error: {e}")
            raise

    def get_records(self, table: str, filters: dict = None):
        try:
            query = self.client.table(table).select("*")
            if filters:
                for k, v in filters.items():
                    query = query.eq(k, v)
            response = query.execute()
            return response
        except Exception as e:
            logging.error(f"Query error: {e}")
            raise

# 单例实例

try:
    db_service = DatabaseService()
except Exception as e:
    db_service = None
    logging.error("Supabase client not initialized.")
