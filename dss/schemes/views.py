from http.client import HTTPResponse
from sched import scheduler
from telnetlib import STATUS
from tokenize import group
from django.shortcuts import render
from psycopg2 import Timestamp
from requests import request
from rest_framework.decorators import api_view
from schemes.models import scheme1
from django.http.response import JsonResponse
from django.core import serializers
import json

# Create your views here.
@api_view(["GET"])
def getData(request):
    data= scheme1.objects.all()
    d=serializers.serialize('json',data)
    d=json.loads(d)
    return JsonResponse(d, status=200 , safe=False)
