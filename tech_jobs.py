import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt 
import seaborn as sns 
from collections import Counter
from matplotlib.ticker import FuncFormatter
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import matplotlib.patches as mpatches




df = pd.read_csv(r'C:\Users\S.C.P\OneDrive\Desktop\py_projects\Capstone\survey_results_public.csv')

pd.set_option('display.max_columns',None)
df2 = df.drop(['Q120','Knowledge_1', 'Knowledge_2', 'Knowledge_3', 'Knowledge_4',
       'Knowledge_5', 'Knowledge_6', 'Knowledge_7', 'Knowledge_8',
       'Frequency_1', 'Frequency_2', 'Frequency_3'],axis=1)

#------------------------------------------------------DATA CLEANING--------------------------------------------------------

#Checking if there is duplicated values in a unique value column (Id's are unique)
# print(df2['ResponseId'].duplicated().sum())

#Drop the duplicated in Id columns
# df2.drop_duplicates(inplace = True)

#Find how many null values in Id's
# print(df2['ResponseId'].isnull().sum())

#First respondent was Null for all of the values
df2.drop(df2.index[0],inplace=True)
print(df2['Employment'].unique())
print(df2['Employment'].isnull().sum()) #Find hpow many null values in Employment section 
print(df2[df2['Employment'].isnull()]['YearsCodePro'].isnull().sum()) 
# 1257 of those who didn't answer the Eployment section, didn't asnwer Years of professional code section as well.




# print (df2.info())
#Drop 1257 respondents whom had not answered Employments and didn't have any professional coding experience
df3 = df2[(df2['Employment'].isnull()) & (df2['YearsCodePro'].isnull())].index
df2 = df2.drop(df3,axis = 0) 
#or: df2 = df2.dropna(subset=['Employment','YearsCodePro'],how='all',inplace = True)


#We want to exlude data of respondents who had null values in LearnCode, YearsCode, and YearscodePro. since their data is not benifitial in our Analysis 
# print(((df2[df2['LearnCode'].isnull()]['YearsCode'].isnull()) & (df2[df2['LearnCode'].isnull()]['YearsCodePro'].isnull())).sum()) #103
df_useless_data = ((df2[df2['LearnCode'].isnull()]['YearsCode'].isnull()) & (df2[df2['LearnCode'].isnull()]['YearsCodePro'].isnull()))
df2 = df2.drop(df_useless_data.index,axis=0)

# the columns CodeActivities and EdLeven has values that have special characters by mistake, let's Identify them using regex
# special_regex = r'[\w\s\d;/\(\)]'
# mask = df['CodingActivities'].str.contains(special_regex, regex = True, na = False)



df2['MainBranch'] = df2['MainBranch'].replace({
       'I am a developer by profession':"Professional",
       'I code primarily as a hobby':'Hobbyist',
       'I am learning to code':'Learner',
       'I am not primarily a developer, but I write code sometimes as part of my work/studies':'Occasional',
       'I used to be a developer by profession, but no longer am':'Former'})
# done to ease the visualization process 


pd.set_option('display.max_row',None)
pd.set_option('display.max_column',None)

df2['DevPro'] = df2['DevType'].replace({
'Senior Executive (C-Suite, VP, etc.)' :"Other",
'Developer, back-end':'Developer jobs',
'Developer, front-end':'Developer jobs',
'Developer, full-stack':'Developer jobs',
'System administrator':"Other",
'Developer, desktop or enterprise applications':'Developer jobs',
'Developer, QA or test':'Developer jobs',
'Designer':"Other",
'Data scientist or machine learning specialist':'Data Jobs',
'Data or business analyst':'Data Jobs',
'Security professional':"Other",
'Educator':"Education and Research",
'Research & Development role':"Education and Research",
'Other (please specify):':"Other",
'Developer, mobile' :'Developer jobs',
'Database administrator':'Data Jobs',
'Developer, embedded applications or devices':"Developer jobs",
'Student':"Student",
'Engineer, data':'Data Jobs',
'Hardware Engineer':"Other",
'Product manager':"Other",
'Academic researcher':"Education and Research",
'Developer, game or graphics':'Developer jobs',
'Cloud infrastructure engineer':"Other",
'Engineering manager':"Other",
'Developer Experience':"Other",
'Project manager':"Other",
'DevOps specialist':"Other",
'Engineer, site reliability':"Other",
'Blockchain':"Other",
'Developer Advocate':"Other",
'Scientist':"Other",
'Marketing or sales professional':"Other"})
#---------------------------------------------------ANALYSIS 1-------------------------------------------------------------
df2['EducationGroup'] = df2['EdLevel'].replace({
 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':'Degree',
 'Some college/university study without earning a degree':'No Degree',
 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':'Degree',
 'Primary/elementary school':'No Degree',
 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':'Degree',
 'Associate degree (A.A., A.S., etc.)':'Degree',
 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':'No Degree',
 'Something else':'No Degree'})

degree_count = df2['EducationGroup'].value_counts()

#--------------------------------------------------PIE: EDUCATION_LEVEL_TECH------------------------------------------------
colors=['orchid', 'cornflowerblue']

plt.figure(figsize=(6,12))

plt.pie(degree_count,labels = df2['EducationGroup'].unique(),colors = colors, autopct = '%1.1f%%')
plt.tight_layout()
plt.legend()
plt.title('Education level of developers',loc='center')
plt.show()

#-----------------------------------------------------------------------------------------------------------------------------

no_degree = df2[df2['EducationGroup'] == 'No Degree']
with_degree = df2[df2['EducationGroup'] == 'Degree']
employment_nodegree = df2[df2['EducationGroup'] == 'No Degree']['Employment'].value_counts()
profession_nodegree = df2[df2['EducationGroup'] == 'No Degree']['MainBranch'].value_counts()
profession_degree = df2[df2['EducationGroup'] == 'Degree']['MainBranch'].value_counts()


# profession_nodegree = df2[(df2['EducationGroup'] == 'No Degree') & (df2['Age'] != 'Under 18 years old')]['MainBranch'].value_counts()
#SEE SECTION 1.2 THE EFFECT OF AGE ON MOTIVE 


#-------------------------------------------------Analysis 1 end---------------------------------------------------------

#-------------------------------------------------PIE/bar: NO DEGREE MAIN BRANCH----------------------------------------------------
plt.pie(profession_nodegree,labels=profession_nodegree.index, autopct = '%1.1f%%')
plt.title('The Main Branch of no degree holders in the tech industry')

plt.show()


Assuming you have already calculated profession_nodegree and profession_degree as described in your code

Plotting a grouped horizontal bar chart
fig, ax = plt.subplots()

bar_width = 0.35
bar_positions_no_degree = range(len(profession_nodegree))
bar_positions_degree = [pos + bar_width for pos in bar_positions_no_degree]

bars_no_degree = ax.barh(bar_positions_no_degree, profession_nodegree, height=bar_width, label='No Degree')
bars_degree = ax.barh(bar_positions_degree, profession_degree, height=bar_width, label='Degree')

# Adding labels and title
plt.xlabel('Number of Participants')
plt.ylabel('Main Branch')
plt.title('Distribution of Main Branch for No Degree and Degree Holders in the Tech Industry')

# Display the percentage on each bar 
for bars, positions, total in [(bars_no_degree, bar_positions_no_degree, sum(profession_nodegree)),
                               (bars_degree, bar_positions_degree, sum(profession_degree))]:
    for bar, position in zip(bars, positions):
        value = bar.get_width()
        ax.text(value, position + bar_width/2, f'{value/total*100:.1f}%', va='center')
plt.yticks(bar_positions_no_degree, profession_nodegree.index)

ax.legend()
plt.tight_layout()
plt.show()


#-----------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Data Cleaning: exclude non professionals------------------------------------------------------------------
df2 = df2[~df2['MainBranch'].isin(['Hobbyist','Learner'])]
#---------------------------------------------------------------------------------------------------------------------------------------


nodegree_dev = no_degree[no_degree['MainBranch'] == 'Professional' ]['DevPro'].value_counts()
withdegree_dev = with_degree[with_degree['MainBranch'] == 'Professional' ]['DevPro'].value_counts()


#--------------------------------------    Section 1.3 Online Certificates among education groups ------------------------

#1.3.1---------counting the platforms---------- 
coursera_counter = 0
udemy_counter = 0
edx_counter = 0 
plural_counter = 0 
codec_counter = 0
other_counter = 0
skl_counter = 0
udacity_counter = 0
for course in no_degree['LearnCodeCoursesCert']: #Do the same for no_degree for platform analysis
    if pd.notna(course):
        course = [platform.strip() for platform in course.split(";")]
        if "Coursera" in course:
            coursera_counter += 1
        if "Udemy" in course: 
            udemy_counter += 1
        if "edX" in course: 
            edx_counter += 1
        if "Pluralsight" in course:
            plural_counter += 1 
        if "Codecademy" in course: 
            codec_counter += 1
        if "Skillsoft" in course:
            skl_counter += 1
        if "Udacity" in course: 
            udacity_counter += 1
        if "Other" in course: 
            other_counter += 1
        

#1.3.2 ------null responde analysis------------
            
print(coursera_counter,udemy_counter,edx_counter,plural_counter,codec_counter,other_counter,with_degree['LearnCodeCoursesCert'].isnull().sum())
print(with_degree.info()) 
NO DEGREE
: total respondents = 23897, null: 14886
percentage of no answer: 62%
WITH DEGREE:
total respondents 63728
null 35674
percentage: 56%
no colclusions
            

#1.3.3-------------Visualizations : Platform_popularity donut------------------
            
platforms = ['Coursera', 'Udemy', 'Pluralsight', 'edX', 'Codecademy', 'Skillsoft', 'Udacity', 'Other']
platform_counts = [coursera_counter, udemy_counter, plural_counter, edx_counter, codec_counter, skl_counter, udacity_counter, other_counter]
colors = ['#FF7F50', '#40E0D0', '#9370DB', '#FFD700', '#90EE90', '#FF6347', '#20B2AA', '#D3D3D3']

plt.figure(figsize=(8, 8))
plt.pie(platform_counts, labels=platforms, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))

# Draw a circle in the center to create a donut chart
centre_circle = plt.Circle((0, 0), 0.6, color='white', fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.title('Popularity of Learning Platforms', pad=20, loc='center')
plt.show()

#------------------------------------------------------Section 1.3 end-----------------------------------------------


#-----------------------------------------------Section 2 Job market analysis-----------------------------------------

# 2.1 -------------------------------------------------Job Distribution------------------------------------------------

#2.1.1-------------------------------Visualization: Distribution of professional roles in the tech industry----------------------------------
profession_count = df2['DevPro'].value_counts()

plt.figure(figsize=(10, 6))
bar_colors = sns.color_palette("husl", len(profession_count))
sns.barplot(x=profession_count.values, y=profession_count.index, palette=bar_colors)

plt.xlabel('Number of Respondents')
plt.ylabel('Professional Roles')
plt.yticks(rotation = 45)
plt.title('Distribution of Professional Roles in Tech Industry')
plt.show()
#-------------------------------------------------------------------------------------------------------------

#-2.2----------------------------------language popularity Analysis: different Tech roles------------------

dev_lang = df2[df2['DevPro'] =='Developer jobs']['LanguageHaveWorkedWith']
data_lang = df2[df2['DevPro'] =='Data Jobs']['LanguageHaveWorkedWith']
full_lang = df2[df2['DevType']=='Developer, full-stack']['LanguageHaveWorkedWith']
front_lang =df2[df2['DevType']=='Developer, front-end']['LanguageHaveWorkedWith']
back_lang = df2[df2['DevType']=='Developer, back-end']['LanguageHaveWorkedWith']

language_devpopularity_counter = Counter()

for skillset in data_lang: #do this for data_lang & dev_lang
    if pd.notna(skillset):
        skillset_list = [language.strip() for language in skillset.split(";") ] 
        for language in skillset_list:
            language_devpopularity_counter [language] += 1

most_common = language_devpopularity_counter.most_common(10)

languages, counts = zip(*most_common)

# 2.2.1-----------------------------------------Bar plot: Top 10 popular languages for Dev -----------------------------------------

colors = plt.cm.viridis(np.linspace(0, 1, len(languages)))

plt.figure(figsize=(12, 12))
bars = plt.bar(languages, counts, edgecolor='black', color=colors)

plt.legend(bars, languages, title='Languages', loc='upper right', bbox_to_anchor=(1.2, 1.0))
plt.xticks(rotation=45, ha='right')
plt.ylabel("Occurrences in Data Jobs")
plt.xlabel('Languages')
plt.title('Top 10 Programming Languages: Data Job Popularity')
plt.show()

#2.2.2 ------------------------------------------Bubble plot: Top 10 popular languages for Data------------------------------------

colors = plt.cm.viridis(np.linspace(0, 1, len(languages)))

plt.figure(figsize=(12, 12))
scatter = plt.scatter(languages, counts, s=[count * 0.1 for count in counts], c=colors, edgecolor='black')

plt.xticks(rotation=45, ha='right')
plt.ylabel("Occurrences in Developing Jobs")
plt.xlabel('Languages')
plt.title('Top 10 Programming Languages: Developer Job Popularity')
plt.show()


#2.3-----------------------------------------------------Skillset Diversity vs Proficiency:---------------------------------------------------

#2.3.1--------------------------------------------------Perparing the Data for Normalization----------------------------------------------

dev_sum = df2[df2['DevPro'] =='Developer jobs'].shape[0]
front_sum = df2[df2['DevType']=='Developer, front-end'].shape[0]
back_sum = df2[df2['DevType']=='Developer, back-end'].shape[0]
full_sum = df2[df2['DevType']=='Developer, full-stack'].shape[0]
data_sum = df2[df2['DevPro'] =='Data Jobs'].shape[0]

#The reason we want the sum of rows of each profession, is to be able to manipulate the data later without the influence of Job count 

#------Note: Will add (*) next to the sections where data will be normalized for ease of reading


#2.3.2--------------------------------------Calculating job opportunities based on skillset diversity---------------------------------------


one_lang = 0
two_lang = 0
three_lang = 0 
four_lang = 0 
five_lang = 0
alot_lang = 0 
six_lang = 0
seven_lang = 0
eight_lang = 0
nine_lang = 0

one_lang_counter = Counter()
two_lang_counter = Counter()
three_lang_counter = Counter()
four_lang_counter = Counter()
five_lang_counter = Counter()

for skillset in front_lang: 
    if pd.notna(skillset):
    # skillset = [language.strip() for language in skillset.split(";")]

        if len(skillset.split(';')) ==1:
            one_lang += 1
            one_lang_counter [skillset] += 1
        elif len(skillset.split(';'))==2:
            two_lang += 1
            two_lang_counter [skillset] += 1
        elif len(skillset.split(';')) ==3:
            three_lang +=1
            three_lang_counter[skillset] +=1

        elif len(skillset.split(';')) == 4:
            four_lang += 1
            four_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 5: 
            five_lang +=1
            five_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 6:
            six_lang +=1 
        elif len(skillset.split(';')) == 7:
            seven_lang += 1
        elif len(skillset.split(';')) == 8: 
            eight_lang += 1
        elif len(skillset.split(';')) == 9:
            nine_lang += 1
        elif len(skillset.split(';')) > 9:
            alot_lang +=1

front_counter = [one_lang,two_lang,three_lang,four_lang,five_lang,six_lang,seven_lang,eight_lang,nine_lang]
front_norm = (np.array(front_counter)/front_sum) * 100 # (** Normalization line)
front_label = ['one_language','two_language','three_language','four_language','five_language','six_language','seven_language','eight_language','nine_language',]
# print(five_lang_counter)





one_lang = 0
two_lang = 0
three_lang = 0 
four_lang = 0 
five_lang = 0
alot_lang = 0 
six_lang = 0
seven_lang = 0
eight_lang = 0
nine_lang = 0

one_lang_counter = Counter()
two_lang_counter = Counter()
three_lang_counter = Counter()
four_lang_counter = Counter()
five_lang_counter = Counter()

for skillset in data_lang: 
    if pd.notna(skillset):
    # skillset = [language.strip() for language in skillset.split(";")]

        if len(skillset.split(';')) ==1:
            one_lang += 1
            one_lang_counter [skillset] += 1
        elif len(skillset.split(';'))==2:
            two_lang += 1
            two_lang_counter [skillset] += 1
        elif len(skillset.split(';')) ==3:
            three_lang +=1
            three_lang_counter[skillset] +=1

        elif len(skillset.split(';')) == 4:
            four_lang += 1
            four_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 5: 
            five_lang +=1
            five_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 6:
            six_lang +=1 
        elif len(skillset.split(';')) == 7:
            seven_lang += 1
        elif len(skillset.split(';')) == 8: 
            eight_lang += 1
        elif len(skillset.split(';')) == 9:
            nine_lang += 1
        elif len(skillset.split(';')) > 9:
            alot_lang +=1



data_counter = [one_lang,two_lang,three_lang,four_lang,five_lang,six_lang,seven_lang,eight_lang,nine_lang]
data_norm = (np.array(data_counter)/ data_sum) * 100 #(** Normalization line)
data_label = ['one_language','two_language','three_language','four_language','five_language','six_language','seven_language','eight_language','nine_language',]

most1 = one_lang_counter.most_common(5)
most2 = two_lang_counter.most_common(5)
most3 = three_lang_counter.most_common(5)
most4 = four_lang_counter.most_common(5)

print(most1,most2,most3,most4)



one_lang = 0
two_lang = 0
three_lang = 0 
four_lang = 0 
five_lang = 0
alot_lang = 0 
six_lang = 0
seven_lang = 0
eight_lang = 0
nine_lang = 0

one_lang_counter = Counter()
two_lang_counter = Counter()
three_lang_counter = Counter()
four_lang_counter = Counter()
five_lang_counter = Counter()

for skillset in full_lang: 
    if pd.notna(skillset):

        if len(skillset.split(';')) ==1:
            one_lang += 1
            one_lang_counter [skillset] += 1
        elif len(skillset.split(';'))==2:
            two_lang += 1
            two_lang_counter [skillset] += 1
        elif len(skillset.split(';')) ==3:
            three_lang +=1
            three_lang_counter[skillset] +=1

        elif len(skillset.split(';')) == 4:
            four_lang += 1
            four_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 5: 
            five_lang +=1
            five_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 6:
            six_lang +=1 
        elif len(skillset.split(';')) == 7:
            seven_lang += 1
        elif len(skillset.split(';')) == 8: 
            eight_lang += 1
        elif len(skillset.split(';')) == 9:
            nine_lang += 1
        elif len(skillset.split(';')) > 9:
            alot_lang +=1

full_counter = [one_lang,two_lang,three_lang,four_lang,five_lang,six_lang,seven_lang,eight_lang,nine_lang]
full_norm = (np.array(full_counter)/full_sum) * 100
full_label = ['one_language','two_language','three_language','four_language','five_language','six_language','seven_language','eight_language','nine_language',]





one_lang = 0
two_lang = 0
three_lang = 0 
four_lang = 0 
five_lang = 0
alot_lang = 0 
six_lang = 0
seven_lang = 0
eight_lang = 0
nine_lang = 0

one_lang_counter = Counter()
two_lang_counter = Counter()
three_lang_counter = Counter()
four_lang_counter = Counter()
five_lang_counter = Counter()

for skillset in back_lang: 
    if pd.notna(skillset):
    # skillset = [language.strip() for language in skillset.split(";")]

        if len(skillset.split(';')) ==1:
            one_lang += 1
            one_lang_counter [skillset] += 1
        elif len(skillset.split(';'))==2:
            two_lang += 1
            two_lang_counter [skillset] += 1
        elif len(skillset.split(';')) ==3:
            three_lang +=1
            three_lang_counter[skillset] +=1

        elif len(skillset.split(';')) == 4:
            four_lang += 1
            four_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 5: 
            five_lang +=1
            five_lang_counter[skillset] += 1
        elif len(skillset.split(';')) == 6:
            six_lang +=1 
        elif len(skillset.split(';')) == 7:
            seven_lang += 1
        elif len(skillset.split(';')) == 8: 
            eight_lang += 1
        elif len(skillset.split(';')) == 9:
            nine_lang += 1
        elif len(skillset.split(';')) > 9:
            alot_lang +=1

back_counter = [one_lang,two_lang,three_lang,four_lang,five_lang,six_lang,seven_lang,eight_lang,nine_lang]
back_norm = (np.array(back_counter)/back_sum) * 100 #(**Normalization line)
back_label = ['one_language','two_language','three_language','four_language','five_language','six_language','seven_language','eight_language','nine_language',]




#2.3.3-----------------------------------Visualization skillset diversity for each profession---------------------------------------


data_max_index = np.argmax(data_counter)
full_max_index = np.argmax(full_counter)
front_max_index = np.argmax(front_counter)
back_max_index = np.argmax(back_counter)


plt.figure(figsize=(12,8))
plt.plot(data_label,data_norm,label = 'Data job')
plt.plot(full_label,full_norm,label = 'full stack developer job')
plt.plot(front_label,front_norm,label = 'Front developer job')
plt.plot(back_label,back_norm,label = 'Back end developer job')

# Add markers for the first and max values
plt.scatter(data_label[0], data_norm[0], color='purple', marker='*', s=200, label='First Value (Data Job)')
plt.scatter(full_label[0], full_norm[0], color='purple', marker='*', s=200, label='First Value (Full Stack)')
plt.scatter(front_label[0], front_norm[0], color='purple', marker='*', s=200, label='First Value (Front End)')
plt.scatter(back_label[0], back_norm[0], color='purple', marker='*', s=200, label='First Value (Back End)')

plt.scatter(data_label[data_max_index], data_norm[data_max_index], color='red', marker='s', s=100, label='Max Value (Data Job)')
plt.scatter(full_label[full_max_index], full_norm[full_max_index], color='red', marker='s', s=100, label='Max Value (Full Stack)')
plt.scatter(front_label[front_max_index], front_norm[front_max_index], color='red', marker='s', s=100, label='Max Value (Front End)')
plt.scatter(back_label[back_max_index], back_norm[back_max_index], color='red', marker='s', s=100, label='Max Value (Back End)')


def to_percentage(y, _):
    return f"{y / 100:.0%}"


plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))

plt.ylabel('Percentage of jobs')
plt.xticks(rotation = 45)
plt.tight_layout()
# plt.title("Jobs abundance for Language Variance in Tech Roles",fontsize = 16,y=1)
plt.legend()
plt.show()


#------------------------------------------------------------------------------------------------------------------------------------------

#2.3.4------------------------------------------Correlation between Education and compitition------------------------------------------

#----------------------------------------------------Data preperation & filtering---------------------------------------------------


df2['LanguagesNumber'] = df2['LanguageHaveWorkedWith'].apply(lambda skillset: len(str(skillset).split(";")) if pd.notna(skillset) else 1)

df2['LanguagesNumber'] = pd.to_numeric(df2['LanguagesNumber'], errors='coerce')

df_analysis3 = df2[df2['EducationGroup'] == 'No Degree']['LanguagesNumber'].value_counts()
df_analysis4 = df2[df2['EducationGroup'] == 'Degree']['LanguagesNumber'].value_counts()


analysis3_norm = (df_analysis3/ df2[df2['EducationGroup'] == 'No Degree']['LanguagesNumber'].shape[0]) * 100
analysis3_norm = analysis3_norm.sort_index(ascending = True)
analysis4_norm = (df_analysis4/ df2[df2['EducationGroup'] == 'Degree']['LanguagesNumber'].shape[0]) * 100
analysis4_norm = analysis4_norm.sort_index(ascending = True)

#We normalized the data here to to mitigate the impact of varying job counts
# df_analysis5 = df2[(df2['EducationGroup'] == 'No Degree') & (df2['LanguagesNumber']==)].copy()
df_analysis5 = df2[df2['EducationGroup'] == 'No Degree'] .copy()

df_analysis5['YearsCode'] = df_analysis5['YearsCode'].replace('Less than 1 year',0.5)
df_analysis5 = df_analysis5[df_analysis5['YearsCode'] != 'More than 50 years']
df_analysis5 = df_analysis5.dropna(subset=['YearsCode'])
df_analysis5['YearsCode'] = pd.to_numeric(df_analysis5['YearsCode'], errors='coerce')  # Convert to numeric

print(df_analysis5['YearsCode'].std())

print(df_analysis4)
width= 0.25
plt.bar(analysis3_norm.head(10).index,analysis3_norm.head(10),width=width,label="No Degree",color=(0.2, 0.4, 0.6, 0.8))
plt.bar(analysis4_norm.head(10).index + width, analysis4_norm.head(10),width= width,edgecolor='none', label = "Degree",color=(0.8, 0.4, 0.2, 0.8))
plt.xlabel('Number of languages')
plt.ylabel("percentage of jobs")
def to_percentage(y, _):
    return f"{y / 100:.0%}"

plt.xticks(analysis3_norm.head(6).index)  # Set x-ticks to start from 1


print(analysis3_norm.head(10))
plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percentage))
plt.legend()
plt.show() 

#--------------------------------------------------------------------------------------------------------------
print(df2[['LanguagesNumber','LanguageHaveWorkedWith']].head(50))
print(analysis3_norm.sort_values(ascending = True).head(6).index)

# print(df_analysis3)
job_types = ['Front End', 'Back End', 'Full Stack', 'Data']
languages = ['HTML/CSS;JavaScript;TypeScript', 'Java', 'HTML/CSS;JavaScript;TypeScript', 'Python;SQL']
max_jobs = [829, 317, 437, 240]

# Create a grouped bar plot
bar_width = 0.2
index = np.arange(len(job_types))

fig, ax = plt.subplots()
for i, language in enumerate(set(languages)):
    language_jobs = [max_jobs[j] if languages[j] == language else 0 for j in range(len(languages))]
    ax.bar(index + i * bar_width, language_jobs, bar_width, label=language)

ax.set_title('Maximum Job Counts by Job Type and Language Combinations')
ax.set_xlabel('Job Type')
ax.set_ylabel('Maximum Job Count')
ax.set_xticks(index + bar_width * (len(set(languages)) - 1) / 2)
ax.set_xticklabels(job_types)
ax.legend(title='Language Combination')

# plt.show()

language_devpopularity_counter = Counter()
language_devpopularity_counterd = Counter()


for skillset in back_lang:
    if pd.notna(skillset):
        skillset_list = [language.strip() for language in skillset.split(";") ] 
        for language in skillset_list:
            language_devpopularity_counter [language] += 1

most_common_back = language_devpopularity_counter.most_common(10)
most_common_back = sorted(most_common_back, key = lambda x:x[0])

languages_back, counts_back = zip(*most_common_back)

for skillset in data_lang:
    if pd.notna(skillset):
        skillset_list = [language.strip() for language in skillset.split(";") ] 
        for language in skillset_list:
            language_devpopularity_counterd [language] += 1

most_common_data = language_devpopularity_counterd.most_common(10)
most_common_data = sorted(most_common_data, key = lambda x:x[0])

languages_data, counts_data = zip(*most_common_data)

common_data_sum = sum(counts_data)
common_back_sum = sum(counts_back)

# print(most_common_back)
# print(most_common_data)

norm_counts_data = (np.array(counts_data)/common_data_sum) * 100
norm_counts_back = (np.array(counts_back)/common_back_sum) * 100





width=0.25

# x_positions_data = np.array(list(languages_data)) + width * np.ones_like(list(languages_data), dtype=np.float64)
x_positions_data = np.arange(len(languages_data))
x_positions_back = x_positions_data + width


plt.bar(x_positions_data, norm_counts_data,width = width, label = 'Data Jobs' )
plt.bar(x_positions_back , norm_counts_back, width=width, label = 'Back End Developer')

plt.legend()
plt.xticks(x_positions_data + width / 2, languages_data, rotation=15)

plt.show()
print(common_data_sum)
print(df_back.shape[0])
plt.figure(figsize=(12,12))
plt.bar(languages, counts,edgecolor = 'black')
plt.xticks(rotation = 45,ha='right')
plt.xlabel('Languages')
plt.ylabel('"Top 10 Programming Languages: Developer Job Popularity"')
# plt.show()
#--------------------------------------------------------------------------------------------------------------------------
#2.3.1-----------------------------------Proficiency correlation to compitition------------------------------------------

#-------------------------------------------Data preperation & manipulation---------------------------------------------

df_years = df2['YearsCode'].value_counts().reset_index()
df_years['YearsCode'] = df_years['YearsCode'].replace('Less than 1 year',0.5)
df_years = df_years[df_years['YearsCode'] != 'More than 50 years']
df_years = df_years.dropna(subset=['YearsCode'])
df_years['YearsCode'] = pd.to_numeric(df_years['YearsCode'], errors='coerce')  # Convert to numeric
df_years.sort_values(by='YearsCode', ascending=True, inplace=True)  # Sort in-place
df_years.reset_index(drop=True, inplace=True) 
df_years = df_years.head(7)

#----------------------------------------------Profissional experience :Comes at a later section----------------------------------------
df_years1 = df2['YearsCodePro'].value_counts().reset_index()
df_years1['YearsCodePro'] = df_years1['YearsCodePro'].replace('Less than 1 year',0.5)
df_years1 = df_years1[df_years1['YearsCodePro'] != 'More than 50 years']
df_years1 = df_years1.dropna(subset=['YearsCodePro'])
df_years1['YearsCodePro'] = pd.to_numeric(df_years1['YearsCodePro'], errors='coerce')  # Convert to numeric
df_years1.sort_values(by='YearsCodePro', ascending=True, inplace=True)  # Sort in-place
df_years1.reset_index(drop=True, inplace=True) 
df_years1 = df_years1.head(7)




#--------------------------------Data Visualization: Proficiency line plot/advantage of profissional proficiency--------------------------

plt.figure(figsize=(10, 6))
colors = sns.color_palette("YlGnBu_d", len(df_years))
sns.lineplot(data=df_years, x='YearsCode', y='count', marker='o', color=colors[1],label ='Total Coding Experience')  
sns.lineplot(data=df_years1, x='YearsCodePro', y='count', marker='o', color='red',label='Professional Coding Experience')



plt.grid(True, linestyle='--', alpha=0.7)

plt.fill_between(df_years['YearsCode'], df_years['count'], df_years1['count'], color='orange', alpha=0.5)


plt.xlabel('Years of Code')
plt.ylabel('Number of Jobs')
plt.title('Advantage of Professional experience')
plt.show()

#----------------------------------------------------------------------------------------------------------------
# 2.3.2---------------------------------------Proficiency vs Diversity vs Compitition----------------------------------------------
#-----------------------------------------------Data Manipulation & Preperation-----------------------------------------------

#Note:Will take care of redundency later
df_corr = df2.groupby(['YearsCode', 'LanguagesNumber']).size().reset_index(name='Count')
df_corr.columns = ['Years of Code', 'Number of languages', 'Job count']
df_corr = df_corr[df_corr['Years of Code'] != "More than 50 years"]
df_corr['Years of Code'] = df_corr['Years of Code'].replace('Less than 1 year', 0.5)
df_corr['Years of Code'] = df_corr['Years of Code'].astype(float)

df_corr = df_corr[df_corr['Years of Code'] <= 5]
df_corr = df_corr[df_corr['Number of languages'] <= 5]

total_jobs_per_language = df_corr.groupby('Number of languages')['Job count'].sum()
df_corr['Job percentage'] = (df_corr['Job count'] / df_corr['Number of languages'].map(total_jobs_per_language)) * 100


# --------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------Visualization Heatmap: Proficiency vs Diversity vs Compition---------------------------------------

plt.figure(figsize=(12, 8))
heatmap_data = df_corr.pivot_table(index='Years of Code', columns='Number of languages', values='Job count', aggfunc='sum')
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='g', cbar_kws={'label': 'Counts'})

plt.title('Correlation between Years of Code, Number of Languages, and Job count')
plt.xlabel('Number of Languages')
plt.ylabel('Years of Code')

plt.show()

# ---------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------Visualization: Bar plot Proficiency vs Diversity vs Compition-----------------------------
max_counts = df_corr.groupby('Years of Code')['Job count'].transform('max')

df_corr['Normalized Job count'] = df_corr['Job count'] / max_counts


plt.figure(figsize=(14, 10))
ax = sns.barplot(x='Years of Code', y='Normalized Job count', hue='Number of languages', data=df_corr, palette='viridis',dodge = True)



# max_counts_per_year = df_corr.groupby('Years of Code')['Job count'].max().reset_index()


plt.title('Correlation between Years of Code, Number of Languages, and Job count')
plt.xlabel('Years of Code')
plt.ylabel('Normalized Job Count')
ax.legend(title='Number of Languages', bbox_to_anchor=(1.05, 1), loc='center')

plt.show()

#--------------------------------------------------------------------------------------------------







df_corr2 = df2.copy()

df_corr2 = df_corr2[['YearsCode','LanguagesNumber','ConvertedCompYearly']]
df_corr2['YearsCode'] = df_corr2['YearsCode'].replace('Less than 1 year',0.5)
df_corr2 = df_corr2[df_corr2['YearsCode'] != "More than 50 years"]
df_corr2['YearsCode'] = df_corr2['YearsCode'].astype(float)

df_corr2 = df_corr2.dropna(subset=['ConvertedCompYearly'])
df_corr2['ConvertedCompYearly'] = df_corr2['ConvertedCompYearly'].astype(float)

df_corr2 = df_corr2[df_corr2['ConvertedCompYearly'] >= 5000]
df_corr2 = df_corr2[(df_corr2['YearsCode'] <=5) & (df_corr2['LanguagesNumber']<=5)]

df_corr3 = df_corr2.groupby(['YearsCode', 'LanguagesNumber']).mean()['ConvertedCompYearly'].reset_index(name='MeanSalary')
df_corr3['LanguagesNumber'] = df_corr3['LanguagesNumber'].astype(float)




# Calculate mean converted yearly for each group
mean_comp = df2.groupby(['YearsCode', 'LanguagesNumber'])['ConvertedCompYearly'].mean().reset_index(name='MeanSalary')

# Merge the two dataframes
# result = pd.merge(df_corr, mean_comp, left_on=['Years of Code', 'Number of languages'], right_on=['YearsCode', 'LanguagesNumber'])




# print(result.head(10) )
fig = plt.figure()

print(df_corr.head(10))
# fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# ax.scatter(df_corr['Years of Code'], df_corr['Number of languages'], df_corr['Counts'])

ax.set_xlabel('Years of Code')
ax.set_ylabel('Number of Languages')
ax.set_zlabel('Counts')
ax.set_title('Correlation between Years of Code, Number of Languages, and Counts')

# plt.show()






# info_list= []
# for row in df_corr.values:
#     info_list.append(row)

# df_corr3['Counts']= None
# for arr in info_list: 
#     arr[0]
#     arr[1]
#     for 
# df_corr_reset = df_corr.reset_index(drop=True)
# df_corr3_reset = df_corr3.reset_index(drop=True)

# df_dj = df_corr.sort_values(by=['Years of Code', 'Number of languages'], ascending=True,ignore_index=True)
# df_corr3 = pd.concat([df_corr3_reset, df_dj['Job count']], axis=1)

# df_corr3 = df_corr3[df_corr3['MeanSalary']<=400000]
# scatter = plt.scatter(df_corr3['MeanSalary'],df_corr3['Job count'], c = df_corr3['LanguagesNumber'],s = df_corr3['YearsCode']*100,cmap='viridis')


# cbar = plt.colorbar(scatter, orientation='vertical', label='Number of Languages')
# cbar.set_label('Number of Languages')

# for size in [1, 2, 3, 4, 5]:
#     plt.scatter([], [], s=size*100, label=f'YearsCode={size}')

# Show the legend
# plt.legend()


# plt.legend()
# plt.show()


df2['EducationGroup'] = df2['EdLevel'].replace({
 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':'Bachelors',
 'Some college/university study without earning a degree':'No Degree',
 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':'Masters',
 'Primary/elementary school':'No Degree',
 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':'Ph.d',
 'Associate degree (A.A., A.S., etc.)':'Associate',
 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':'No Degree',
 'Something else':'No Degree'})

df2['YearsCode'] = df2['YearsCode'].replace('Less than 1 year',0.5)
df2 = df2[df2['YearsCode'] != "More than 50 years"]
df2['YearsCode'] = df2['YearsCode'].astype(float)
df_analysis5 = df2.groupby(['EducationGroup'])['ConvertedCompYearly'].mean().reset_index('EducationGroup')
df_analysis6 = df2.groupby(['EducationGroup'])['YearsCode'].mean().reset_index('EducationGroup')

df_analysis7 = pd.concat([df_analysis6,df_analysis5['ConvertedCompYearly']],axis=1)

scaler =MinMaxScaler()
toscale_data = df_analysis7[['YearsCode','ConvertedCompYearly']]
scaled_data = scaler.fit_transform(toscale_data)
df_analysis7[['YearsCode','ConvertedCompYearly']] = scaled_data
# label_encoder = LabelEncoder()
# df_analysis7['EducationGroup'] = label_encoder.fit_transform(df_analysis7['EducationGroup'])

# sns.lineplot(x='EducationGroup', y='ConvertedCompYearly', data=df_analysis7, marker='o')
# plt.xlabel('Education Group')
# plt.ylabel('Normalized ConvertedCompYearly')
# plt.title('Line Plot of Normalized Salary by Education Group')
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
# plt.show()

