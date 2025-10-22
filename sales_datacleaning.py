# step 1: clean up the data from the inventory report
import pandas as pd 
inventory = pd.read_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/Inventory_report.csv",
    encoding="latin1",
    skiprows=3, #rows 0,1,2 are metadata/notes. column headers start on row 4 
    header=0
)
print("Columns after fixing header:", inventory.columns.tolist())
print("\nInventory preview:")
print(inventory.head())

# clean column names 
inventory.columns = inventory.columns.str.strip().str.lower().str.replace(' ','_')
print("Cleaned columns:", inventory.columns.tolist())

#drop empty columns 
inventory = inventory.dropna(axis=1, how='all')

# drop empty rows
inventory = inventory.dropna(how='all')
print(inventory.head())

# converting numeric columns so the calculations work in tableau

numeric_cols = [
    'on-hand_quantity', 
    'age_:_0-30_days',
    'age_:_31-60_days',
    'age_:_61-90_days', 
    'age_:_>90_days', 
    'last_stock_inflow_(days)',
    'sales/consumption_(last_90_days)',
    'avg_price_(perpetual)'
    'pending_delivery_qty',
    'alert_quantity',
    'desired_quantity',
    'suggested_quantity'
]

for col in numeric_cols:
    if col in inventory.columns:
        inventory[col] = pd.to_numeric(inventory[col], errors='coerce').fillna(0)

# add calculated column for total inventory value

inventory['total_value'] = inventory['on-hand_quantity'] * inventory['avg_price_(perpetual)']

inventory.to_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/clean_inventory.csv",
    index=False 
)
print("Clean inventory saved as clean_inventory.csv")

# step 2: clean data for employee sales report
sales = pd.read_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/Employee_Sales.csv", 
    encoding="latin1"
)

sales.columns = sales.columns.str.strip().str.lower().str.replace(' ', '_')

# since i am going to combine the sales report + inventory report in tableau, 
# they need to have standardized names , do not want to include services, only product 
# keep only rows where item_type == 'Product'
sales_products = sales[sales['item_type'].str.lower() == 'product']

sales_products = sales_products.rename(columns={'item_name': 'product_name'})
# aggregate total wuantity sold and employee sale value by product 
sales_agg = sales_products.groupby('product_name', as_index=False).agg({
    'employee_sale_value': 'sum'
})

print(sales_agg.head())

sales_agg.to_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/clean_employee_sales.csv",
    index=False
)

# tableau will not let me do a JOIN with the current csv files so we will merge

# merging inventory + sales 
inventory_sales = pd.merge(
    inventory,
    sales_agg,
    on='product_name',
    how='left' # this keeps ALL inventory products, adds sales where available
)

# filling the NaN sales values with 0
inventory_sales['employee_sale_value'] = inventory_sales['employee_sale_value'].fillna(0)

inventory_sales.to_csv(
    "/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/inventory_sales_combined.csv",
    index=False,
    encoding="latin1" 
)
print("Inventory + Sales merged and saved as inventory_sales_combined.cvs")
print(inventory_sales.head())