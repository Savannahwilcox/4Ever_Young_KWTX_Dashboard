import pandas as pd

# Load CSV
kpi = pd.read_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/Employee_KPIs.csv",
    encoding="latin1",
    skiprows=3
)

# Standardize column names
kpi.columns = (
    kpi.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
    .str.replace('%', '_pct', regex=False)
    .str.replace('/', '_', regex=False)
)

# Drop fully empty rows/columns
kpi = kpi.dropna(axis=1, how='all')
kpi = kpi.dropna(how='all')

# Strip text fields
text_cols = ['work_center', 'employee_code', 'employee_name', 'job']
for col in text_cols:
    if col in kpi.columns:
        kpi[col] = kpi[col].astype(str).str.strip()

# Numeric columns (automatically detect if column exists)
numeric_cols = [col for col in kpi.columns if col not in text_cols]

# Remove commas, $ signs, and convert to numeric, filling NaNs with 0
for col in numeric_cols:
    kpi[col] = (
        kpi[col]
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace('$', '', regex=False)
        .str.replace(' ', '', regex=False)
    )
    kpi[col] = pd.to_numeric(kpi[col], errors='coerce').fillna(0)

# Final clean DataFrame
kpi_clean = kpi[text_cols + numeric_cols]

# Save clean CSV
kpi_clean.to_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/clean_employee_kpi.csv",
    index=False
)

print("Cleaned Employee KPI CSV saved successfully!")
print(kpi_clean.head())
