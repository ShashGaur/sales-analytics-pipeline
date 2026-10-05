from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def clean_erp_loc_a101():

  df = pd.read_parquet(settings.BRONZE_DIR / "erp_loc_a101.parquet")

  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

  stringcols=df.columns[df.dtypes=="str"]
  
  for col in stringcols:
    df[col]=df[col].str.strip()
  
  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} columns")
  
  df["CID"]=df["CID"].str.replace("-","",regex=False)

  logger.info(f"Made Customer ID's consistent with  Customer ID format")

  logger.info(df['CNTRY'].value_counts(dropna=False))

  COUNTRY_MAP = {
    "USA": "United States",
    "US":  "United States",
    "DE":  "Germany",
}
  df["CNTRY"]=df["CNTRY"].replace(COUNTRY_MAP)

  logger.info(f"Normalized country names")

  msk=(df["CNTRY"]=="") | (df["CNTRY"].isna())

  df.loc[msk, "CNTRY"]="Unknown"

  logger.info(df['CNTRY'].value_counts(dropna=False))

  df=df.rename(columns=settings.RENAME_LOC_A101)

  logger.info("Renamed columns")

  output_path=settings.SILVER_DIR/"erp_loc_a101.parquet"

  df.to_parquet(output_path, index=False)

  logger.info(f"Written {len(df)} rows to {output_path}")

if __name__ == "__main__":
  clean_erp_loc_a101()