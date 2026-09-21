from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger=get_logger(__name__)

def clean_crm_customers():
  df=pd.read_parquet(settings.BRONZE_DIR/"crm_cust_info.parquet")

  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

  stringcols=df.columns[df.dtypes=="str"]

  for col in stringcols:
    df[col]=df[col].str.strip()

  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} colums")

  nullcst_id=len(df[df['cst_id'].isna()])

  df=df.dropna(subset=['cst_id'])

  logger.info(f"Dropped {nullcst_id} rows with null Customer ID")

  df["cst_id"] = df["cst_id"].astype("int64")

  df["cst_gndr"] = df["cst_gndr"].str.upper().map({"M": "Male", "F": "Female"}).fillna("n/a")

  logger.info(f"Normalized Gender from M to Male and F to Female")

  df["cst_marital_status"] = df["cst_marital_status"].str.upper().map({"S": "Single", "M": "Married"}).fillna("n/a")

  logger.info(f"Normalized Marital Status from S to Single and M to Married")

  df["cst_create_date"] = pd.to_datetime(df["cst_create_date"], format=settings.DATE_FORMAT_DMY, errors="coerce")

  logger.info(f"Normalized string date to Date format")
  
  dup_rows = df.duplicated().sum()
  logger.info(f"Full row duplicates found: {dup_rows}")

  dup_keys = df.duplicated(subset=["cst_id"]).sum()
  logger.info(f"Duplicate Customer ID values found: {dup_keys}")

  if(dup_rows):
    df=df.drop_duplicates()

  if dup_keys > 0:
    dups = df[df.duplicated(subset=["cst_id"], keep=False)].sort_values("cst_id")
    logger.warning(f"Duplicate rows:\n{dups.to_string()}")

  if dup_rows == 0:
    logger.info("No full row duplicates found")
  else:
    logger.info(f'Dropped {dup_rows} full row duplicate rows')

  df = df.rename(columns=settings.RENAME_CUST_INFO)

  logger.info("Renamed columns")

  df.to_parquet(settings.SILVER_DIR/"crm_customers.parquet", index=False)

  logger.info(f"Written {len(df)} rows to {settings.SILVER_DIR/"crm_customers.parquet"}")


if __name__=="__main__":
  clean_crm_customers()