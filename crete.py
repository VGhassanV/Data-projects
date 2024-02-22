import pandas as pd 
from bs4 import BeautifulSoup 
import numpy as np 
from matplotlib import pyplot as plt 
import requests 
import re

#Reading the Dataset into a CSV file

df = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\listings.csv')

#--------------------------------------------------------------------Data Cleaning-------------------------------------------------------------
#1)Since listing Id is a unique entity, we should check for duplicates and delete them

print(df['id'].duplicated().sum())
df = df[~df['id'].duplicated()]

#2)Since a listing id is unique to a date and an apartment, it's impossibe for the the Id to appear twice on the same date, We are check that
filtered_1 = df.groupby(['listing_id','date']).size().reset_index(name='count')

duplicatess = filtered_1[filtered_1['count']>1]

df = df[~df.set_index(['listing_id', 'date']).index.isin(duplicatess.set_index(['listing_id', 'date']).index)]

#-----------------------------------------------------------------------------------------------------------------------------------------------

#Applying Equal Sampling method: taking the same number of listings from each neighbourhood
def sample_listing(group):
    return group.sample(min(25,len(group)))

sample_df = df.groupby('neighbourhood',group_keys=False).apply(sample_listing)

sampled_df = sample_df.reset_index(drop=True)

#Loading the Filtered Datafram into CSV file for preview in Excel
sampled_df.to_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\sampled_listing.csv')

#---------------------------------------------------------------Data Manipulation-------------------------------------------------------------

df = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\sampled_listing.csv')

df_edit = df.set_index('id',inplace=False)
df2 = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\reviews.csv')

df2 = df2[df2['listing_id'].isin(df_edit.index)]




df3 = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\calendar.csv')

df3 = df3[df3['listing_id'].isin(df_edit.index)]

# df3.to_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\calendar_sample.csv')

neighborhood_mapping = {
    'Αγίου Βασιλείου': 'Agios Vasileios',
    'Αγίου Νικολάου': 'Agios Nikolaos',
    'Χανίων': 'Chania',
    'Φαιστού': 'Festos',
    'Σφακίων': 'Sfakia',
    'Σητείας': 'Sitia',
    'Ρεθύμνης': 'Rethymno',
    'Πλατανιά': 'Platanias',
    'Οροπεδίου Λασιθίου': 'Lasithi Plateau',
    'Μυλοποτάμου': 'Mylopotamos',
    'Μινώα Πεδιάδας': 'Minya Pediada',
    'Μαλεβιζίου': 'Malevizi',
    'Κισσάμου': 'Kissamos',
    'Καντάνου - Σέλινου': 'Kandanos-Selinou',
    'Ιεράπετρας': 'Ierapetra',
    'Ηρακλείου': 'Heraklion',
    'Γόρτυνας': 'Gortynas',
    'Γαύδου': 'Gavdos',
    'Βιάννου': 'Viannos',
    'Αρχανών - Αστερουσίων': 'Archanes-Asterousia',
    'Αποκορώνου': 'Apokoronas',
    'Ανωγείων': 'Anogeia',
    'Αμάριου': 'Amari',
    'Χερσονήσου': 'Chersonissos'
}



df['neighbourhood'] = df['neighbourhood'].replace(neighborhood_mapping)

df.to_csv(r'C:\Users\S.C.P\OneDrive\Desktop\Crete Investor project\sampled_listing2.csv')

