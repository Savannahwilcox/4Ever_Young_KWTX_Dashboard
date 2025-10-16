import sys # loads py system module
print(sys.executable)
import pandas as pd # dataframes
import matplotlib.pyplot as plt # graphs / charts 
import uuid # used to make unique IDs for pt names. HIPAA!!
import seaborn as sns # plotting library on matplotlib for heatmap

# here im loading the appts report 
# df: dataframe : pandas main object for storing tables 
# encoding= 'latin1': fixes the character issue in zenoti CSV files 
df = pd.read_csv("/Users/savannahwilcox/Desktop/Cursor/learning.py/4Ever_young_dashboard/Appointments.csv", encoding='latin1')


# had to go back and clean up column names bc they had weird characterds
#df.columns is a list of all column names 
# .str.strip() : removes xtra spaces at start or end of names 
# .str.replace(' ', '') remoces xtra spaces inside the names 
# "Patients Name" --> "PatientsName"
df.columns = df.columns.str.replace('ï»¿', '', regex=False) \
                        .str.replace('"', '', regex=False) \
                        .str.strip() \
                        .str.replace(' ', '', regex=False)

# for hipaa purposes im gonna replace pt names with an ID 
df['PatientsName'] = [str(uuid.uuid4()) for _ in range(len(df))]


df.to_csv("appointments_anonymized.csv", index=False)
print("Patient names anonymized and saved to appointments_anonymized.csv") 

#converts the AppointmentDate column from txt to python date format 
# pd.to_datetime - converts str dates from CSV into py datetime objects 
# errors = coerce: replaces invalid dates w NaT for missing value
# creates new column w/ weekday names 
# len(df) : total appts , 
df['AppointmentDate'] = pd.to_datetime(df['AppointmentDate'], errors='coerce')
df['DayOfWeek'] = df['AppointmentDate'].dt.day_name()
print("Total appointments:", len(df))

# finding appts per status-- so closed, canceled, no show, etc)
# selects Status Column, .value_counts() counts how many times each unique value (complete, cancel, noshow, etc.) appears in the Status column 
status_counts = df['Status'].value_counts()
print("Appointments per status:")
print(status_counts)

# finding appts per SERVICE 
# finding top 5 most popular services via .head(5)
# will use this to see which services are in most demand and identify gaps 
service_counts = df['ServiceName'].value_counts().head(5)
print("Top 5 booked services:")
print(service_counts)

#finding appts per DAY -- identifies busy or slow datys
appointments_per_day = df.groupby('AppointmentDate').size()
print("Appointments per day:")
print(appointments_per_day)
## NOTETOSELF: come back and make this part more useful
##why is range only 1/25 , 10/25?????? fix this later 

# finding appts per weekday
#gives really good data: .value_counts() counts how many appts fall on each wkday 
# .reindex([...]) : makes days in CALENDAR order, NOT alphabetical!!
appointments_per_weekday = df['DayOfWeek'].value_counts().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])
print(appointments_per_weekday)

# now gonna try to visualize the weekday trends via barchart

appointments_per_weekday.plot(kind='bar', figsize=(8,5), color='pink', title='Appointments per day of week'
)
plt.ylabel('Number of Appointments')
plt.xlabel('Day of Week')
plt.grid(axis='y')
plt.show()

# monthly trends 
df['Month'] = df['AppointmentDate'].dt.to_period('M')
appointments_per_month = df.groupby('Month').size()
appointments_per_month.plot(kind='bar', figsize=(10,5), color='hotpink', title='Appointments per Month')
plt.ylabel('Number of Appts')
plt.show()

busiest_month = appointments_per_month.idxmax()
slowest_month = appointments_per_month.idxmin()
print(f"Busiest month: {busiest_month} ({appointments_per_month.max()} appointments)")
print(f"Slowest month: {slowest_month} ({appointments_per_month.min()} appointments)")

# wkday patterns and monthly trends via pivot table
df['MonthName'] = df['AppointmentDate'].dt.month_name()
weekday_month = df.pivot_table(index='DayOfWeek', columns='MonthName', values='PatientsName', aggfunc='count').reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])

plt.figure(figsize=(12,6))
sns.heatmap(weekday_month, annot=True, fmt='g', cmap='pink')
plt.title('Appts Heatmap- weekday v month')
plt.show()

# lets see who are the most active providers 
top_providers = df['Provider'].value_counts().head(5)
top_providers.plot(kind='bar', color='lightblue', title='Top Providers')
plt.show()
# NOTETOSELF: ^^this is not helpful. includes staff no longer there. fix this