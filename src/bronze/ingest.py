from config import settings
from src.utils.logger import get_logger
import pandas as pd


logger=get_logger(__name__)

def ingest_one(name,path):
  logger.info(f"Reading {name} from {path}")
  df=pd.read_csv(path, sep=settings.CSV_SEP)
  logger.info(f"Rows: {len(df)}, Columns: {len(df.columns)}")
  output_path=settings.BRONZE_DIR/f"{name}.parquet"
  df.to_parquet(output_path, index=False)
  logger.info(f"Written to {output_path}")

def run():
  logger.info("Starting Bronze ingestion")
  for name, path in settings.RAW_FILES.items():
    ingest_one(name,path)
  logger.info("Bronze ingestion complete")

if __name__=="__main__":
  run()