#!/home/ubuntu/reach/rentPricesMonitoring/venv2/bin/python


# coding: utf-8

# Import packages but issues with urllib2
from bs4 import BeautifulSoup
import codecs
from json import dumps
import urllib2
import sys
from datetime import datetime
import os.path
from urllib2 import urlopen, Request
#import urllib.request  as urllib2
import pickle


#ff=codecs.open("./output/test.json",'w',"utf-8")
#ff.write("tessst")
#ff.close()

# Print current date and time
print(datetime.today().strftime('%d/%m/%Y %H:%M'))

listArticle=[]

def praseOne(element):
    d=dict()
    linkA="https://ly.opensooq.com"+str(element.a["href"])
    #print(linkA)
    utf8string = linkA.encode("utf-8")
    #print(utf8string)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    #reg_url = utf8string
    #req = Request(url=reg_url, headers=headers)

    try:
        page = urllib2.urlopen(utf8string).read()
        soup = BeautifulSoup(page,'html.parser')


        counter=0
        id_post = soup.find('div', {'class':'postId mb15 mt15'})
        if id_post is not None:
            d["id"] = id_post.get_text().encode('utf-8').split(":")[1]
            x= soup.find('span', {'class':'postDate relative fRight'})

            d["date"] = x.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip()

            #print(d["id"],d["date"])
            #return True

            #print(x.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip())
            for i in soup.findAll('li',{'class':'inline vTop'}):
                test = True
                if (counter <= 9):
                    line = i.get_text().encode('utf-8').replace("\n", "").replace("\t", "").strip().split(":")
                    counter = counter +1
                    if (line[0] == "Cameras - Photography"):
                        counter = 10
                    else :
                        d[line[0]]=line[1]
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

print(1)
pagelink= "https://ly.opensooq.com/en/job-seekers/all"
#print(pagelink)
try:
    page = urllib2.urlopen(pagelink).read()
    soup = BeautifulSoup(page,'html.parser')
    for i in soup.findAll('div',{'class':'rectLiDetails tableCell vMiddle p8'}):
        praseOne(i)
        #print('ok')
        #raw_input('Enter your input:')

except urllib2.HTTPError, e:
    #print e.fp.read()
    print("********************************************************************")
    print ("error type2:")
    print(pagelink)
    print("********************************************************************")


#print(listArticle)




for i in range(2,10):
        print(i)
        pagelink= "https://ly.opensooq.com/en/job-seekers/all?page=%s&per-page=30"%(i)
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

'''
filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s.json" %datetime.today().strftime('%d_%m_%Y')
if os.path.isfile(filePath):
    i=2
    filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s_v%s.json" %(datetime.today().strftime('%d_%m_%Y'),i)
    while(os.path.isfile(filePath)):
        i+=1
        filePath = "/home/ubuntu/reach/rentPricesMonitoring/output/%s_v%s.json" %(datetime.today().strftime('%d_%m_%Y'),i)

'''



with open('/home/ubuntu/reach/rentPricesMonitoring/jobs/all_offers.obj', 'wb') as f:

  pickle.dump(listArticle, f)
