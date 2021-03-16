#!/home/ubuntu/reach/rentPricesMonitoring/venv2/bin/python


# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import codecs
from json import dumps
import urllib2
import sys
from datetime import datetime
import os.path
from urllib2 import urlopen, Request

# In[2]:

#ff=codecs.open("./output/test.json",'w',"utf-8")
#ff.write("tessst")
#ff.close()

print(datetime.today().strftime('%d/%m/%Y %H:%M'))


# In[3]:


listArticle=[]

def praseOne(element):
    d=dict()
    linkA="https://ly.opensooq.com"+str(element.a["href"])
    utf8string = linkA.encode("utf-8")
    #print(utf8string)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    #reg_url = utf8string
    #req = Request(url=reg_url, headers=headers)

    try:
        page = urllib2.urlopen(utf8string).read()
        soup = BeautifulSoup(page,'html.parser')
        #print(utf8string)
        counter=0
        id_post = soup.find('div', {'class':'postId mb15 mt15'})
        if id_post is not None:
            d["id"] = id_post.get_text().encode('utf-8').split(":")[1].strip()
            x= soup.find('span', {'class':'postDate relative fRight'})
            #print(x.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip())
            d["date"] = x.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip()
            for i in soup.findAll('li',{'class':'inline vTop relative mb15'}):
                test = True
                if (counter <= 9):
                    line = i.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip().split(":")
                    counter = counter +1
                    if (line[0] == "Cameras - Photography"):
                        counter = 10
                    else :
                        d[line[0]]=line[1].strip()
            #print(d)
            listArticle.append(d)
    except urllib2.HTTPError, e:
        #print e.fp.read()
        print("********************************************************************")
        print ("error:")
        print(utf8string)
        print("********************************************************************")

        #print(utf8string)




# In[4]:


pagelink= "https://ly.opensooq.com/en/real-estate-for-rent/apartments-for-rent"
#print(pagelink)
try:
    page = urllib2.urlopen(pagelink).read()
    soup = BeautifulSoup(page,'html.parser')
    for i in soup.findAll('div',{'class':'rectLiDetails tableCell vMiddle p8'}):
        praseOne(i)
        #print(i)
        #raw_input('Enter your input:')

except urllib2.HTTPError, e:
    #print e.fp.read()
    print("********************************************************************")
    print ("error type2:")
    print(pagelink)
    print("********************************************************************")


# In[48]:




# In[ ]:


for i in range(2,30):
        pagelink= "https://ly.opensooq.com/en/real-estate-for-rent/apartments-for-rent?page="+str(i)
        #print(pagelink)
        try:
            page = urllib2.urlopen(pagelink).read()
            soup = BeautifulSoup(page,'html.parser')
            for i in soup.findAll('div',{'class':'rectLiDetails tableCell vMiddle p8'}):
                    praseOne(i)
        except urllib2.HTTPError, e:
            #print e.fp.read()
            print("********************************************************************")
            print ("error type2:")
            print(pagelink)
            print("********************************************************************")
        #print(i)


# In[52]:

filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s.json" %datetime.today().strftime('%d_%m_%Y')
if os.path.isfile(filePath):
    i=2
    filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s_v%s.json" %(datetime.today().strftime('%d_%m_%Y'),i)
    while(os.path.isfile(filePath)):
        i+=1
        filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s_v%s.json" %(datetime.today().strftime('%d_%m_%Y'),i)



f=codecs.open(filePath,'w',"utf-8")


# In[51]:


f.write('{ "Offres": [')
c=0
for i in range(len(listArticle)):
        f.write(dumps(listArticle[c]))
        if c < len(listArticle) - 1 :
                f.write(",\n")
        c+=1

f.write("] \n }")
f.close()


# In[ ]: