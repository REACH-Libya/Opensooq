#!/usr/bin/python3
# coding: utf-8

# In[1]:


import pickle
import pandas as pd
import codecs
from json import dumps
import json
import pymysql
from datetime import datetime, date, timedelta
import sqlalchemy


# In[2]:


def correctDates(df):
    dates= df['date']
    for i in range(len(dates)):
        #print(str(dates[i]).find("ago")>=0)
        if (str(dates[i]).find("ago")>=0 or str(dates[i]).find("Now")>=0):
            dates[i] = datetime.today().strftime('%d-%m-%Y')
        elif (str(dates[i]).find("Yesterday")>=0):
            yesterday = date.today() - timedelta(days=1)
            dates[i] = yesterday.strftime('%d-%m-%Y')
            
    df['date'] = dates    
        
    return(df)


# In[3]:


with open('/home/ubuntu/reach/rentPricesMonitoring/jobs/all_offers.obj', 'rb') as f:
    listArticle = pickle.load(f)

with open('/home/ubuntu/reach/rentPricesMonitoring/jobs/output.json', 'w') as fout:
    json.dump(listArticle , fout)


# In[4]:


df = pd.read_json(r'/home/ubuntu/reach/rentPricesMonitoring/jobs/output.json')
count_row = df.shape[0]
count_row


# In[5]:


df.rename(columns={'Neighborhood': 'neighborhood',
                   'Experience Level': 'experience_level',
                   'Job type' : 'job_type',
                   'Education Level' : 'education_level',
                   'Job Role' : 'job_role',
                   'Gender' : 'gender',
                   'Driver License' : 'driver_license',
                   'Specialty' : 'specialty'
                  }, inplace=True)


# In[6]:


df.tail(10)


# In[7]:


cols = "`,`".join([str(i) for i in df.columns.tolist()])
cols


# In[8]:


pd.set_option('mode.chained_assignment', None)
df = correctDates(df)
df['date'] = pd.to_datetime(df['date'])


# In[9]:


database_username = 'assil'
database_password = 'sK/r<SR/6Pea/q*$'
database_ip       = '37.59.233.104'
database_name     = 'reach'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))


# In[10]:


connection = pymysql.connect(host='37.59.233.104',
                             user='assil',
                             password='sK/r<SR/6Pea/q*$',
                             db='reach')


# In[11]:


cursor = connection.cursor()


# In[12]:


added_rows = 0
count_row = df.shape[0]
for i in range(count_row):
    cursor.execute(
        "SELECT id FROM job_seekers WHERE id = %s",
        (str(df.iloc[[i]]['id'].values[0]))
    )
    row_count = cursor.rowcount
    if (cursor.rowcount==0):
        #print(i,"added")
        added_rows += 1
        df.iloc[[i]].to_sql(con=database_connection, name='job_seekers', if_exists='append', index=False, index_label='id')


# In[13]:


count_row = df.shape[0]
count_row


# In[14]:


print(added_rows)

