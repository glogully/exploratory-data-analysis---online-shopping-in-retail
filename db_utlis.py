import pandas as pd
import yaml
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    def __init__(self, config_file='credentials.yaml'):
        self.credentials = self._load_db_credentials(config_file)
        self.engine = self._create_engine()

    def _load_db_credentials(self, filepath) -> dict:
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

    def _create_engine(self):
        creds = self.credentials
        url = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        return create_engine(url)

    def extract_data(self, table_name: str) -> pd.DataFrame:
        try:
            query = f"SELECT * FROM {table_name};"
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"Error extracting data: {e}")
            return pd.DataFrame()

def save_data_to_csv(data_frame: pd.DataFrame, filename: str):
    if not data_frame.empty:
        data_frame.to_csv(filename, index=False)
    else:
        print("No data to save to CSV.")

if __name__ == "__main__":
    connector = RDSDatabaseConnector()
    data_frame = connector.extract_data('customer_activity')
    save_data_to_csv(data_frame, 'customer_activity.csv')
