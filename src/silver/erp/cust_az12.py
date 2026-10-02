from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger=get_logger(__name__)

def clean_erp_cust_az12():
  df = pd.read_parquet(settings.BRONZE_DIR / "erp_cust_az12.parquet")
  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

  stringcols=df.columns[df.dtypes=="str"]
  
  for col in stringcols:
    df[col]=df[col].str.strip()

  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} columns")

  bcid=df['CID'].str.startswith('NAS')

  bcid_cnt=bcid.sum()

  df.loc[bcid,"CID"]= df.loc[bcid,"CID"].str.removeprefix(settings.ERP_CID_PREFIX)

  logger.info(f"Made {bcid_cnt} Customer ID's consistent with  Customer ID format")

  df["BDATE"] = pd.to_datetime(df["BDATE"], format=settings.DATE_FORMAT_YMD, errors="coerce")
  
  logger.info(f"Normalized string date to Date format")

  logger.info(df['GEN'].value_counts(dropna=False))

  df['GEN']=df['GEN'].str.upper().map({"M": "Male", "F": "Female", "MALE":"Male", "FEMALE": "Female"}).fillna("Unknown")

  logger.info(df['GEN'].value_counts(dropna=False))

  df = df.rename(columns=settings.RENAME_CUST_AZ12)
  
  logger.info("Renamed columns")

  output_path = settings.SILVER_DIR / "erp_cust_az12.parquet"
  
  df.to_parquet(output_path, index=False)
    
  logger.info(f"Written {len(df)} rows to {output_path}")


if __name__ == "__main__":
  clean_erp_cust_az12()
  