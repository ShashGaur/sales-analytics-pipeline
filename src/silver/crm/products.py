from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger=get_logger(__name__)

def clean_crm_products():
  df=pd.read_parquet(settings.BRONZE_DIR/"crm_prd_info.parquet")

  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

  stringcols=df.columns[df.dtypes=="str"]

  for col in stringcols:
    df[col]=df[col].str.strip()
  
  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} columns")

  df["prd_start_dt"] = pd.to_datetime(df["prd_start_dt"], format=settings.DATE_FORMAT_YMD, errors="coerce")

  df["prd_end_dt"] = pd.to_datetime(df["prd_end_dt"], format=settings.DATE_FORMAT_YMD, errors="coerce")

  logger.info(f"Normalized string dates to Date format")

  numn=df['prd_cost'].isna().sum()

  df['prd_cost']=df['prd_cost'].fillna(0)

  logger.info(f"Replaced {numn} null costs with 0")

  counts = df["prd_line"].value_counts(dropna=False)

  logger.info(f"prd_line raw values: {counts}")

  PRD_LINE_MAP={"R": "Road", "M": "Mountain", "S": "Sport","T": "Touring"}

  df["prd_line"] = df["prd_line"].str.upper().map( PRD_LINE_MAP).fillna("Unknown")
  
  logger.info(f"Normalized product line names")

  start_after_end = ((df["prd_start_dt"].notna()) & (df["prd_end_dt"].notna()) & (df["prd_start_dt"] >= df["prd_end_dt"])).sum()

  both_missing = (df["prd_start_dt"].isna() & df["prd_end_dt"].isna()).sum()

  start_missing=(df["prd_start_dt"].isna()).sum()

  end_missing=(df["prd_end_dt"].isna()).sum()

  if start_after_end:
    logger.warning(f"{start_after_end} rows have start_date >= end_date")

  if both_missing:
    logger.warning(f"{both_missing} rows have both start and end dates missing")

  if start_missing:
    logger.warning(f"{start_missing} rows have missing start dates")

  if end_missing:
    logger.info(f"{end_missing} rows have missing end date")

  df = df.rename(columns=settings.RENAME_PRD_INFO)
  
  logger.info("Renamed columns")

  output_path=settings.SILVER_DIR/"crm_products.parquet"

  df.to_parquet(output_path, index=False)

  logger.info(f"Written {len(df)} rows to {output_path}")

if __name__ == "__main__":
  clean_crm_products()
