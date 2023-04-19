from keywords import keyword_dict
from duckduckgo_search import ddg
import time
import pandas as pd
#from bson import json_util, ObjectId
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://dss:P8NKXqiTp3tN3vNt@dss-search.ujjrk5w.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["dss-search"]
mycol=mydb['search_new3']



addon_keywords={"awards":['recognized awards site:.gov.in','recognized awards site:.nic.in'],'research':['research paper site:.sciencedirect.com','research paper site:.researchgate.com','research paper site:.scholar.google.com'],
                'educational':['prestigious university research site:.edu','prestigious university research site:.iitd.ac.in','prestigious university research site:.iisc.ac.in'],
                'implemented':['related program or scheme implemented by government site:.gov.in','related program or scheme implemented by government site:.un.org','related program or scheme implemented by government site:.usa.gov']
                }



df=pd.DataFrame(columns=['query','title','link','description','department','addon_type'])


def scrape(request):
    for key in keyword_dict.keys:
        for q in keyword_dict[key]:
            for addon in addon_keywords:
                for regex in addon_keywords[addon]:
                    query=q+regex
                    
                    outputs = ddg(query, region='hi-in', safesearch='moderate', time='y',max_results=10,page=1)
                    print(query)
                    if outputs is None:
                        print("No result")
                    else:
                        print("results")
                        for res in outputs:
                            print(res)
                            obj={}
                            obj['query']=q
                            obj['title']=res['title']
                            obj['link']=res['href']
                            obj['body']=res['body']
                            obj['department']=key
                            obj['count']=1
                            obj['extra_keyword']=addon
                            a = mycol.insert_one(obj)
                            print(a.inserted_id)
                            df.loc[len(df.index)]=[q,res['title'],res['href'],res['body'],'test department',addon]
                    time.sleep(2)
    return "success"

scrape("abx")
df.to_csv('scrapeData.csv')