from django.shortcuts import render
import pandas as pd
import numpy as np
import faiss
import joblib
from deep_translator import GoogleTranslator
from django.core import serializers
from datetime import datetime
from http.client import HTTPResponse
from telnetlib import STATUS
from rest_framework.decorators import api_view
from django.http import HttpResponse,HttpResponseBadRequest, HttpResponseServerError, FileResponse, HttpRequest
import json
from details.models.profile import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.core import serializers
from django.db import IntegrityError
from details.models.calamity import Calamity
from details.models.crime import Crime
from details.models.epidemic import Epidemic
from details.models.publicGathering import PublicGathering
from details.models.rally import Rally
from  sentenceSimilarity.models import crimeSen,calamitySen,epidemicSen,publicGatheringSen,rallySen
from datetime import datetime
import datetime
import spacy.cli
import re
from django.contrib.auth.models import User
import random
#spacy.cli.download("en_core_web_lg")
# import spacy
# nlp = spacy.load('en_core_web_lg')


model=joblib.load('./sentenceSimilarity/saved_model.sav')

#these indexes should be reloaded periodically using cronjob

calamityIndex=faiss.read_index('./sentenceSimilarity/calamity_data.bin')
crimeIndex=faiss.read_index('./sentenceSimilarity/crime_data.bin')
epidemicIndex=faiss.read_index('./sentenceSimilarity/epidemic_data.bin')
rallyIndex=faiss.read_index('./sentenceSimilarity/rally_data.bin')
publicGatheringIndex=faiss.read_index('./sentenceSimilarity/publicGathering_data.bin')



def load_model(type):
    if type=="crime":
        index_name=crimeIndex
    elif type=="rally":
        index_name=rallyIndex
    elif type=="calamity":
        index_name=calamityIndex
    elif type=="epidemic":
        index_name=epidemicIndex
    elif type=="publicGathering":
        index_name=publicGatheringIndex
    return index_name

# Create your views here.
def fetch_info(id,semScore,type):
    if type=="crime":
        info = crimeSen.objects.get(pk=id)
    elif type=="rally":
        info = rallySen.objects.get(pk=id)
    elif type=="calamity":
        info = calamitySen.objects.get(pk=id)
    elif type=="epidemic":
        info = epidemicSen.objects.get(pk=id)
    elif type=="publicGathering":
        info = publicGatheringSen.objects.get(pk=id)
    

    meta_dict = dict()
    print(info.index)
    meta_dict['lesson'] = info.lesson
    meta_dict['semScore'] = semScore
    # d=serializers.serialize('json',info)
    # d=json.loads(d)
    meta_dict['index']= info.index
    return meta_dict
    
def search(query, top_k, index, model,type):
    similarity_measure = faiss.METRIC_INNER_PRODUCT  
    query_vector = model.encode([query])
    faiss.normalize_L2(query_vector)
    top_k = index.search(query_vector, top_k)
    top_k_ids = top_k[1].tolist()[0]
    top_k_simScore=top_k[0].tolist()[0]
    print(top_k_ids)
    #top_k_ids = list(np.unique(top_k_ids))
    #top_k_simScore=list(np.unique(top_k_simScore))
    #results =  [fetch_info(idx,type) for idx in top_k_ids]
    results=[]
    for i in range(len(top_k_ids)):
        results.append(fetch_info(top_k_ids[i],top_k_simScore[i],type))
    return results

def search_similiar_bert(query,type):
    s1=datetime.now()
    index_bert=load_model(type)
    print("load time",datetime.now()-s1)
    s2=datetime.now()
    results=search(query, top_k=5, index=index_bert, model=model,type=type)
    print("search time",datetime.now()-s2)
    #print(top_k)
    print(results)
    s3=datetime.now()
    similar_lesson_bert = []
    for result in results:
        similar_lesson_bert.append (
                {
                    #'Relevance': (p[1] * 100),
                    'lesson': result['lesson'],
                    'similarityScore' : result['semScore'],
                    'index':result['index']
                }

            )
    #p_names_bert=pd.DataFrame(p_names_bert, columns=['Product Name','Description'])
    print("result time",datetime.now()-s3)
    return similar_lesson_bert

@api_view(['POST'])
def similarSentence(request):
    data= JSONParser().parse(request)
    print(data)
    query=data['query']
    type= data['type']
    #start=datetime.now()
    res=search_similiar_bert(query,type)
    #print(datetime.now()-start)
    print(res[0])
    if(len(res)>0 and res[0]['similarityScore']<0.6):
        index_bert=load_model(data['type'])
        new_vector = model.encode([data['query']])
        faiss.normalize_L2(new_vector)
        #print(new_vector)    
        if data['type']=="crime":
            obj = crimeSen.objects.create(lesson=data['query'])
        elif data['type']=="rally":
            obj = rallySen.objects.create(lesson=data['query'])
        elif data['type']=="calamity":
            obj = calamitySen.objects.create(lesson=data['query'])
        elif data['type']=="epidemic":
            obj = epidemicSen.objects.create(lesson=data['query'])
        elif data['type']=="publicGathering":
            obj = publicGatheringSen.objects.create(lesson=data['query'])
        res[0]['index_new']=obj.pk
        new_id=obj.pk
        index_bert.add_with_ids(new_vector, np.array([new_id]))
        # print(new_id)
        faiss.write_index(index_bert, data['type']+'_data.bin')
    res=json.dumps(res)
    return JsonResponse(res,status=status.HTTP_200_OK, safe=False)


@api_view(['POST'])
def addLesson(request):
    data=JSONParser().parse(request)
    index_bert,model=load_model(data['type'])
    new_vector = model.encode([data['text']])
    faiss.normalize_L2(new_vector)
    #print(new_vector)
    
    if data['type']=="crime":
        obj = crimeSen.objects.create(lesson=data['text'])
    elif data['type']=="rally":
        obj = rallySen.objects.create(lesson=data['text'])
    elif data['type']=="calamity":
        obj = calamitySen.objects.create(lesson=data['text'])
    elif data['type']=="epidemic":
        obj = epidemicSen.objects.create(lesson=data['text'])
    elif data['type']=="publicGathering":
        obj = publicGatheringSen.objects.create(lesson=data['text'])

    print(obj.pk)
    new_id=obj.pk
    index_bert.add_with_ids(new_vector, np.array([new_id]))
    # print(new_id)
    faiss.write_index(index_bert, data['type']+'_data.bin')
    return JsonResponse("New Lesson Added", status=200, safe=False)
    


#Lesson learnt
@api_view(['POST'])
def lessonLearnt(request):
    data=JSONParser().parse(request)  #expecting type of law and order
    if data['type']=='crime':
        d=serializers.serialize('json', Crime.objects.all())
    elif data['type']=='calamity':
        d=serializers.serialize('json', Calamity.objects.all())
    elif data['type']=='epidemic':
        d=serializers.serialize('json', Epidemic.objects.all())
    elif data['type']=='rally':
        d=serializers.serialize('json', Rally.objects.all())
    elif data['type']=='publicGathering':
        d=serializers.serialize('json', PublicGathering.objects.all())
    d=json.loads(d)
    return JsonResponse(d,status=status.HTTP_200_OK, safe=False)


@api_view(['PUT'])
def updateCount(request):
    d= JSONParser().parse(request)
    id=d['id']
    type=d['type']
    if type=='crime':
        obj=crimeSen.objects.get(pk=id)
        crimeSen.objects.filter(pk=id).update(count=obj.count+1)
    elif type=='calamity':
        obj=calamitySen.objects.get(pk=id)
        calamitySen.objects.filter(pk=id).update(count=obj.count+1)
    elif type=='rally':
        obj=rallySen.objects.get(pk=id)
        rallySen.objects.filter(pk=id).update(count=obj.count+1)
    elif type=='epidemic':
        obj=epidemicSen.objects.get(pk=id)
        epidemicSen.objects.filter(pk=id).update(count=obj.count+1)
    elif type=="publicGathering":
        obj=publicGatheringSen.objects.get(pk=id)
        publicGatheringSen.objects.filter(pk=id).update(count=obj.count+1)

    return HttpResponse("count updated")


# def preprocessing(sentence):
 
#     #remove distracting single quotes
#     sentence = re.sub('\'','',sentence)
#     #replace extra spaces with single space
#     sentence = re.sub(' +',' ',sentence)

#     #remove unwanted lines starting from special charcters
#     sentence = re.sub(r'\n: \'\'.*','',sentence)
#     sentence = re.sub(r'\n!.*','',sentence)
#     sentence = re.sub(r'^:\'\'.*','',sentence)
    
#     #remove non-breaking new line characters
#     sentence = re.sub(r'\n',' ',sentence)

#     return sentence


# @api_view(['POST'])
# def databaseHelper(request):
#     rally_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Rally (2).csv")
#     for i in range(len(rally_sen)):
#         u_id=request.user.id
#         person=User.objects.get(pk=u_id)
#         obj=Rally.objects.create(
#             owner=person,rally_title=rally_sen.iloc[i]['Title'],attendance=random.randint(100,100000),
#             lesson_learnt=rally_sen.iloc[i]['Lesson Learned'],
#             date=datetime.date.today(),
#             police=random.randint(10,100),ambulance=random.randint(100,1000),
#             firefighters=random.randint(100,10000)
#         )
#         text=preprocessing(rally_sen.iloc[i]['Lesson Learned'])
#         sentences = [str(i) for i in nlp(text).sents]
#         for sen in sentences:
#             d_id=obj.pk
#             detailInst=Rally.objects.get(pk=d_id)
#             newobj=rallySen.objects.create(detailId=detailInst,lesson=sen)
#             print(newobj.pk)

#     return HttpResponse("All rally Data Added")

        









