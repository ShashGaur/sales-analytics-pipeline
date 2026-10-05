from config import settings
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def clean_erp_px_cat_g1v2():
  df = pd.read_parquet(settings.BRONZE_DIR / "erp_px_cat_g1v2.parquet")

  logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

  stringcols=df.columns[df.dtypes=="str"]
    
  for col in stringcols:
    df[col]=df[col].str.strip()
    
  logger.info(f"Trimmed unnecessary whitespaces from {len(stringcols)} columns")

  logger.info(df['CAT'].value_counts(dropna=False))

  logger.info(df['SUBCAT'].value_counts(dropna=False))

  logger.info(df['MAINTENANCE'].value_counts(dropna=False))

  df['MAINTENANCE']=df['MAINTENANCE'].str.upper().map({'YES': 'Yes', 'NO': 'No'}).fillna('Unknown')

  logger.info(f"Normalized Maintenance column")

  df=df.rename(columns=settings.RENAME_PX_CAT_G1V2)

  logger.info("Renamed columns")

  output_path=settings.SILVER_DIR/"erp_px_cat_g1v2.parquet"
  
  df.to_parquet(output_path, index=False)
  
  logger.info(f"Written {len(df)} rows to {output_path}")


if __name__ == "__main__":
  clean_erp_px_cat_g1v2()