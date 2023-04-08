from django.shortcuts import render
from searchEngine.models import searchResult
from requests import Session
import json
from rest_framework.decorators import api_view
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.http.response import JsonResponse,HttpResponse
from rest_framework.parsers import JSONParser
from searchEngine.keywords import result
# Create your views here.
from bson import json_util, ObjectId
import pymongo
from duckduckgo_search import ddg
print(len(result))
myclient = pymongo.MongoClient("mongodb+srv://dss:P8NKXqiTp3tN3vNt@dss-search.ujjrk5w.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["dss-search"]
# print(mydb)
# mydb.create_collection('searchLinks')
mycol=mydb['search_new3']
# print(mycol)

@api_view(['GET'])
def searchQuery(request):
    q= request.GET.get('q')
    print('HII')
    result = mycol.aggregate([
        {
            '$search': {
                'index': 'default-1', 
                'text': {
                    'query': q, 
                    'path': 'body', 
                    'fuzzy': {
                        'maxEdits': 2
                    }
                }
            }
        }, {
            '$project': {
                '_id': 1, 
                'body': 1, 
                'title': 1,
                'link':1,
                'department':1,
                'sector':1,
                'extra_keyword':1,
                'count':1, 
                'score': {
                    '$meta': 'searchScore'
                }
            }
        }
    ])
    r=[]
    for i in result:
        print(i)
        r.append(i)
    d= json.loads(json_util.dumps(r))
    return JsonResponse(d,safe=False)
# @api_view(["GET"])
# def scrape(request):
#     # data= JSONParser().parse(request)
#     # data = request.data
#     try:
#         # mycol.delete_many({})
#         links= mydb['searchLinks']
#         print(len(result))
#         for q in result:
#             for i in range(2):
#                 BASE_URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyBcEBRIr1tmY_ZxuRgNN6cA1rLuhpr-KiA&cx=7692c9c0d3459418f&q="+ q
#                 if(i==1):
#                     BASE_URL= BASE_URL+'&start=11'
#                 print(BASE_URL)
#                 session = Session()
#                 print(i)
#                 response = session.get(BASE_URL)
#                 data= response.json()
#                 print(data)
#                 try:
#                     for i in data['items']:
#                         # try:
#                         x=links.find_one({'link':i['link']})
#                         if x:
#                             print('FOUNDD')
#                         else:
#                             print('NOT FOUND')      
#                             obj={}
#                             try:
#                                 obj['title']=i['title']
#                             except:
#                                 print(1)
#                             try:
#                                 obj['snippet']= i['snippet']
#                             except:
#                                 print(2)
#                             try: 
#                                 obj['link']= i['link']
#                             except:
#                                 print(3)
#                             # if(('pagemap' in i)  & ('metatags' in i['pagemap']) & ('og:description' in i['pagemap']['metatags'][0]) ):
#                             try:
#                                 obj['description']=i['pagemap']['metatags'][0]['og:description']
#                             except:
#                                 print('none')
#                             obj['searchItem']= json.dumps(i)
#                             a = mycol.insert_one(obj)
#                             b= links.insert_one({'link':i['link']})
#                             print(a.inserted_id)
#                 except:
#                     print('nan')
#         return JsonResponse({'message':'Added Successfully'}, safe= False)
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)
#         return JsonResponse('DID not get DATA', safe=False)

addon_keywords={"awards":['recognized awards site:.gov.in','recognized awards site:.niti.gov.in','recognized awards site:.nic.in'],'research':['research paper site:.sciencedirect.com','research paper site:.researchgate.com','research paper site:.scholar.google.com','research paper site:.niti.gov.in'],
                'educational':['prestigious university research site:.edu','prestigious university research site:.iitd.ac.in'],
                'implemented':['related program or scheme implemented by government site:.gov.in','related program or scheme implemented by government site:.un.org','related program or scheme implemented by government site:.usa.gov','related program or scheme implemented by government site:.niti.gov.in']
                }

@api_view(['GET'])
def scrape(request):
    for q in result:
        for addon in addon_keywords:
            for regex in addon_keywords[addon]:
                query=q+" "+regex
                outputs = ddg(query, region='hi-in', safesearch='moderate', time='y',max_results=10,page=1)
                if outputs is None:
                    print("No result")
                else:
                    for res in outputs:
                        print(res)
    return HttpResponse("success")






