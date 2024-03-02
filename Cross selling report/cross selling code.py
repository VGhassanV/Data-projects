import pandas as pd 
import numpy as np 
import re


# I downloaded the task file as csv to my machine, then used the read_csv method of Pandas library in python
df = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Data Projects\blue-monkies\cross-selling-report.csv')

# defining the Month column as the posting date of the Sale transaction
df['Month'] = pd.to_datetime(df['Posting Date'], format="%d/%m/%Y", errors='coerce').dt.to_period('M')

# Exclude rows with 'SHIPMENT' in 'Item No.'
data = df[df['Item No.'] != 'SHIPMENT']


# Group by Month and Item Number
grouped_data = data.groupby(['Month', 'Item No.']).size().reset_index(name='Count')

# Extract Category Code 1 and Category Code 2 using regex in grouped_data
grouped_data['Category Code 1'] = grouped_data['Item No.'].apply(lambda x: re.match(r'^([A-Za-z]+-\d+)', x).group(1) if re.match(r'^([A-Za-z]+-\d+)', x) else "No match")
grouped_data['Category Code 2'] = grouped_data['Item No.'].apply(lambda x: re.sub(r'^[A-Za-z]+-\d+-', '', x) if re.match(r'^[A-Za-z]+-\d+', x) else "No match")


# #Using the regular expression lambda function, when the Item no consisted only of parent SKU
#the lambda function tended to category code 1 = category code 2 ,For example, first entry was "Tool-17", in both category code, it was the same.
#in the next line we are filtering out the data consisting of only parent 

grouped_data = grouped_data[grouped_data['Category Code 1'] != grouped_data['Category Code 2']]



# Rank the items within each month
grouped_data['Rank'] = grouped_data.groupby('Month')['Count'].rank(ascending=False, method='first')

# Convert 'Month' to month names
grouped_data['Month'] = grouped_data['Month'].dt.strftime('%B')

# Sort the DataFrame by 'Month' and 'Rank' in ascending order
grouped_data = grouped_data.sort_values(by=['Month', 'Rank'], ascending=[False, True])


# Select the Top 13 Items for Each Month
top_items = grouped_data[grouped_data['Rank'] <= 13]

# Display the result
print(top_items.reset_index()[['Month', 'Item No.','Category Code 1','Category Code 2', 'Rank', 'Count']])

#Thank you for giving me the opportunity to work on this project, I hope you don't mind adding it on my portfolio website ! 
