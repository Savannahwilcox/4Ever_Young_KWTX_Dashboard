import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
# no uuid needed here bc no PHI included 
df_sales = pd.read_csv("Employee_Sales.csv", encoding='latin1')

# removing employee last names for privacy
def anonymize_name(name):
    parts = name.split()
    first_name = parts[0]
    credentials = ''
    if ',' in name:
        credentials = name.split(',')[1].strip()
        return f"{first_name} ({credentials})"
    else:
        return first_name 
        
df_sales['Employee Name'] = df_sales ['Employee Name'].apply(anonymize_name)
print("Employee names anonymized:")
print(df_sales['Employee Name'].unique())


# again cleaning column names 
df_sales.columns = df_sales.columns.str.strip().str.replace('"', '').str.replace('ï»¿', '')

# convert date columns txt into py datetime
# to groupby mo, wkday, etc
df_sales['Sale Date'] = pd.to_datetime(df_sales['Sale Date'], errors='coerce')

#making xtra columns to help w groupby 
df_sales['Month'] = df_sales['Sale Date'].dt.to_period('M') #monthly period
df_sales['DayOfWeek'] = df_sales['Sale Date'].dt.day_name() #wkday name
print("Dates converted.")
print(df_sales[['Sale Date', 'Month', 'DayOfWeek']].head())

#total revenue per employee 
revenue_per_employee = df_sales.groupby('Employee Name')['Sales'].sum().sort_values(ascending=False)
print("Revenue per employee:")
print(revenue_per_employee)
# i will want to eventually make a pie chart or something to show % of sales per employee
# so im gonna calculate % of total sales first
sales_percent = (revenue_per_employee / revenue_per_employee.sum()) * 100
sales_percent = sales_percent.sort_values(ascending=False).round(2) # sorts descending
print(sales_percent)

#pie chart for rev per employee 
plt.figure(figsize=(8,8))
plt.pie(sales_percent, labels=sales_percent.index, autopct='%1.1f%%', startangle=140)
plt.title('Percentage of Total Sales by Employee', fontsize=14)
plt.tight_layout()
plt.show()

# revenue per weekday 
revenue_per_weekday = df_sales.groupby('DayOfWeek')['Sales'].sum().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])
print("Revenue per weekday:")
print(revenue_per_weekday)

# revenue per month
revenue_per_month = df_sales.groupby('Month')['Sales'].sum()
print("Revenue per month:")
print(revenue_per_month)
