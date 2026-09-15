from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR    = ROOT / "data"
RAW_DIR     = DATA_DIR / "raw"
BRONZE_DIR  = DATA_DIR / "bronze"
SILVER_DIR  = DATA_DIR / "silver"
GOLD_DIR    = DATA_DIR / "gold"
REPORTS_DIR = ROOT / "outputs" / "reports"
EXPORTS_DIR = ROOT / "outputs" / "exports"

RAW_FILES = {
    "crm_cust_info":     RAW_DIR / "crm" / "cust_info.csv",
    "crm_prd_info":      RAW_DIR / "crm" / "prd_info.csv",
    "crm_sales_details": RAW_DIR / "crm" / "sales_details.csv",
    "erp_cust_az12":     RAW_DIR / "erp" / "CUST_AZ12.csv",
    "erp_loc_a101":      RAW_DIR / "erp" / "LOC_A101.csv",
    "erp_px_cat_g1v2":   RAW_DIR / "erp" / "PX_CAT_G1V2.csv",
}

RENAME_CUST_INFO = {
    "cst_id": "customer_id",
    "cst_key": "customer_number",
    "cst_firstname": "first_name",
    "cst_lastname": "last_name",
    "cst_marital_status": "marital_status",
    "cst_gndr": "gender",
    "cst_create_date": "created_date",
}

RENAME_PRD_INFO = {
    "prd_id": "product_id",
    "prd_key": "product_number",
    "prd_nm": "product_name",
    "prd_cost": "product_cost",
    "prd_line": "product_line",
    "prd_start_dt": "product_start_date",
    "prd_end_dt": "product_end_date",
}

RENAME_SALES_DETAILS= {
    "sls_ord_num": "order_number",
    "sls_prd_key": "product_number",
    "sls_cust_id": "customer_id",
    "sls_order_dt": "order_date",
    "sls_ship_dt": "ship_date",
    "sls_due_dt": "due_date",
    "sls_sales": "sales_amount",
    "sls_quantity": "quantity",
    "sls_price": "price",
}

RENAME_CUST_AZ12={
    "CID": "customer_number",
    "BDATE": "birthdate",
    "GEN": "gender",
}

RENAME_LOC_A101={
    "CID": "customer_number",
    "CNTRY": "country",
}

RENAME_PX_CAT_G1V2={
    "ID": "category_id",
    "CAT": "category",
    "SUBCAT": "subcategory",
    "MAINTENANCE": "maintenance",
}

DATE_FORMAT_DMY = "%d-%m-%Y"   # for "06-10-2025" style dates
DATE_FORMAT_YMD = "%Y%m%d"     # for "20101229" style dates
CSV_SEP = ","          