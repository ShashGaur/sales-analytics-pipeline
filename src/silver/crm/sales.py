from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger=get_logger(__name__)

def clean_crm_sales():
  df=pd.read_parquet(settings.BRONZE_DIR/"crm_sales_details.parquet")
  
  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
  
  stringcols=df.columns[df.dtypes=="str"]
  
  for col in stringcols:
    df[col]=df[col].str.strip()
    
  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} columns")

  df["sls_order_dt"] = pd.to_datetime(df["sls_order_dt"].astype(str), format="%Y%m%d", errors="coerce")

  df["sls_ship_dt"] = pd.to_datetime(df["sls_ship_dt"].astype(str), format="%Y%m%d", errors="coerce")

  df["sls_due_dt"] = pd.to_datetime(df["sls_due_dt"].astype(str), format="%Y%m%d", errors="coerce")

  logger.info(f"Normalized string dates to Date format")

  bad_sales=(df["sls_sales"].isna()) | (df["sls_sales"]<=0)

  bad_sales_count=bad_sales.sum()

  bad_price=(df["sls_price"].isna()) | (df["sls_price"] <= 0)

  bad_price_count=bad_price.sum()

  df.loc[bad_sales, "sls_sales"]=df.loc[bad_sales, "sls_quantity"] * df.loc[bad_sales, "sls_price"].abs()

  logger.info(f"Fixed {bad_sales_count} bad sales amounts")

  df.loc[bad_price, "sls_price"]=(df.loc[bad_price, "sls_sales"] / df.loc[bad_price, "sls_quantity"]).abs()

  logger.info(f"Fixed {bad_price_count} bad prices")

  bad_sales_cn2=((df["sls_sales"].isna()) | (df["sls_sales"]<=0)).sum()

  logger.info(f"Remaining {bad_sales_cn2} bad sales")

  bad_price_cn2=((df["sls_price"].isna()) | (df["sls_price"] <= 0)).sum()

  logger.info(f"Remaining {bad_price_cn2} bad prices")

  mismatch = (df["sls_sales"] != df["sls_quantity"] * df["sls_price"])

  logger.info(f"Business rule mismatches after fix: {mismatch.sum()}")

  logger.warning(f"Deferred mismatches (sample):\n{df.loc[mismatch, ['sls_ord_num','sls_quantity','sls_sales','sls_price']].head(10).to_string()}")

  df = df.rename(columns=settings.RENAME_SALES_DETAILS)

  logger.info("Renamed columns")

  output_path = settings.SILVER_DIR / "crm_sales.parquet"

  df.to_parquet(output_path, index=False)
  
  logger.info(f"Written {len(df)} rows to {output_path}")


if __name__ == "__main__":
  clean_crm_sales()
