# UofT - DSI / Python
# Building Software Homework 1s
# Student Name: Ka Ho (Gerald) Chan

import numpy as np
import pandas as pd

# display all columns
pd.set_option("display.max_columns", None)

# Using engine='python' which is slower but more feature-complete. 
# As the default value engine='c' option would issues warning about memory use due to column 18 having mixed types.
fireIncidents = pd.read_csv('Chan_KaHo_python_assignment2_orig.csv', engine='python')

# Print out columns name
colNames = list(fireIncidents.columns.values)
print(f'The Column Names: {colNames}')

# Another way to see all the column names
fireIncidents.info()

# Another way to see all the column names
fireIncidents.info()

fireIncidents.isna().sum()

fireIncidents.shape

# The _id column is consdiered numeric but those are not data but metadata, so excluding it
numericColumns = fireIncidents.drop('_id', axis=1)

# Max value per column, rounding output to 2 decimal places
print('Max values for numeric columns\n')
numericColumns.select_dtypes(include=np.number).max().round(2)

# Min value per column, rounding output to 2 decimal places
print('Min values for numeric columns\n')
numericColumns.select_dtypes(include=np.number).min().round(2)

# Mean value per column, rounding output to 2 decimal places
print('Mean values for numeric columns\n')
numericColumns.select_dtypes(include=np.number).mean().round(2)

# Median value per column, rounding output to 2 decimal places
print('Median values for numeric columns\n')
numericColumns.select_dtypes(include=np.number).median().round(2)

# According to select_dtypes() documentation, selecting string should use 'object' type
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html
stringColumns = fireIncidents.select_dtypes(include='object')
allStrings = pd.DataFrame()

# Put all the values from all the string columns into 1 column in a new dataframe
for columnName, data in stringColumns.items():
    allStrings = pd.concat([allStrings, data],
                          axis=0,
                          ignore_index=True)

allStringValueCount = allStrings.value_counts()

# Most common value.  
# Note: value_counts() returns a series with index being the text value stored in a tuple with 1 value
# So allStringValueCount.index[0] return the first index item, allStringValueCount.index[0][0] return the first value in the tuple of the first index item which is the text we want
# The series returned by value_counts() also put the highest count as the first value in the series
print(f'The most common value is "{allStringValueCount.index[0][0]}" with count {allStringValueCount.values[0]}')

# Unique value count.  
# Number of unqiue value is large because all timestamps are still stored as string. Conversion is at question 7 of the assignment below.
# [0] is used on allStrings because the dataframe column has no name and is a 1 dimension array
print(f'Number of unique values is {allStrings[0].unique().size}') 

# Summary Statistics
fireIncidents.describe(include='all')

print('Before renaming columns\n')
fireIncidents.info()

print('After renaming columns\n')
fireIncidents = fireIncidents.rename(columns={'Fire_Alarm_System_Operation': 'Fire_Alarm_System_Operation_With_Person_Present', 'Fire_Alarm_System_Presence': 'Fire_Alarm_System_Presence_With_Person_Present'})
fireIncidents.info()

fireIncidents['Possible_Cause'].unique()

fireIncidents['Area_of_Origin'].value_counts()

print('Before dType Conversion\n')
fireIncidents.dtypes

# Convert known date time column to datetime then print out the dTypes
fireIncidents['Ext_agent_app_or_defer_time'] = pd.to_datetime(fireIncidents['Ext_agent_app_or_defer_time'])
fireIncidents['Fire_Under_Control_Time'] = pd.to_datetime(fireIncidents['Fire_Under_Control_Time'])
fireIncidents['Last_TFS_Unit_Clear_Time'] = pd.to_datetime(fireIncidents['Last_TFS_Unit_Clear_Time'])
fireIncidents['TFS_Alarm_Time'] = pd.to_datetime(fireIncidents['TFS_Alarm_Time'])
fireIncidents['TFS_Arrival_Time'] = pd.to_datetime(fireIncidents['TFS_Arrival_Time'])
print('After dType Conversion\n')
fireIncidents.dtypes

# Original file format is CSV, so writing it out to JSON
fireIncidents.to_json('Chan_KaHo_python_assignment2_proc.json')
# Also writing the data out into CSV because of the submission instructions 
# that required a 'LASTNAME_FIRSTNAME_python_assignment2_proc.csv' file:
# Submit assignment via your Google Drive. Upload your 
# (1) code file (LASTNAME_FIRSTNAME_python_assignment2_code.ipynb), 
# (2) original data file (LASTNAME_FIRSTNAME_python_assignment2_orig.csv), and 
# (3) processed DataFrame file (LASTNAME_FIRSTNAME_python_assignment2_proc.csv) 
fireIncidents.to_csv('Chan_KaHo_python_assignment2_proc.csv')

fireIncidents['TFS_Alarm_Month'] = fireIncidents['TFS_Alarm_Time'].dt.month
# Verify new column is created and counts its content
fireIncidents['TFS_Alarm_Month'].value_counts().sort_index()

print('Before removing column')
fireIncidents.info()

print('After remove column')
# Removing 'Incident_Number' column as it is meta data to link to internal fire depearment records and not actual data releated to the fires
fireIncidents = fireIncidents.drop(columns='Incident_Number') # 'Incident_Number' is number 17 at info() printout before being removed
fireIncidents.info()

# Meteorological Summer is month 6 (June), 7 (July), 8 (August)
summerFireIncidents = fireIncidents.query('6 <= TFS_Alarm_Month <= 8')[['Area_of_Origin', 'Ignition_Source',
                                                                      'Business_Impact', 'Estimated_Dollar_Loss',
                                                                      'Latitude', 'Longitude', 
                                                                      'TFS_Alarm_Month','TFS_Alarm_Time']]
summerFireIncidents.head()

withBusinessImpactDataIncidents = (fireIncidents.loc[fireIncidents['Business_Impact'].notna(),
                                             ['Area_of_Origin', 'Ignition_Source',
                                              'Business_Impact', 'Estimated_Dollar_Loss',
                                              'Latitude', 'Longitude', 
                                              'TFS_Alarm_Month','TFS_Alarm_Time']])
withBusinessImpactDataIncidents.head()

nanAnyCol = fireIncidents.loc[fireIncidents['Building_Status'].isna()]
nanAnyCol.describe(include='all')

nanSubsetCol = (fireIncidents.loc[fireIncidents['Intersection'].isna(),
                                 ['Estimated_Dollar_Loss',
                                  'Latitude', 'Longitude']])
nanSubsetCol.describe(include='all')

# Only 2 records with no 'Intersection' in the entire data set.  Latitude and Latitude were not aviliable in that 2 records as well.
fireIncidents = fireIncidents.dropna(subset=['Intersection']) 

fireIncidentsByMonth = fireIncidents.groupby('TFS_Alarm_Month')
fireIncidentsByMonth.size()

fire_summary = (fireIncidents.groupby('TFS_Alarm_Month')
                .agg(num_of_fire_Incidents=('_id', 'count'), 
                     total_persons_rescued=('Count_of_Persons_Rescued', 'sum'), 
                     max_persons_rescued_per_incident=('Count_of_Persons_Rescued', 'max'),
                     mean_persons_displaced=('Estimated_Number_Of_Persons_Displaced', 'mean'),                    
                     mean_responding_personnel=('Number_of_responding_personnel', 'mean'),
                     median_estimated_dollar_loss=('Estimated_Dollar_Loss', 'median')))

fire_summary.head(12)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Setting Title, Labels and Grid
ax.set_title('Persons affected by Fire Incidents')
ax.set_xlabel('Month')
ax.set_ylabel('Persons')
ax.set_axisbelow(True)
ax.set_xticks(np.arange(0, 13, step=1),['', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'])
ax.grid(alpha=0.3)

# Creating chart
maxRecusedPerIncident = ax.scatter(fire_summary.index, fire_summary['max_persons_rescued_per_incident'])
meanPersonsDisplaced = ax.scatter(fire_summary.index, fire_summary['mean_persons_displaced'])
meanRespondingPersonnel = ax.scatter(fire_summary.index, fire_summary['mean_responding_personnel'])

# Creating legend
ax.legend([maxRecusedPerIncident, meanPersonsDisplaced, meanRespondingPersonnel],
          ['Max Persons Recused Per Incident', 'Mean Persons Displaced', 'Mean Responding Personnel'],
          bbox_to_anchor=(1, 1),
          loc='upper left')

fig.savefig('Building_Software_Homework1.png')