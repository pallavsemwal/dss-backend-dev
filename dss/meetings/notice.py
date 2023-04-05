from django.db import connection
import pdfkit
from django.template.loader import get_template
import pyrebase
from django.shortcuts import render
import random
from django.template.loader import render_to_string
import string
import json

from meetings.createNotice import generate_pdf

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

def createNotice(request,data):
    #Define path to wkhtmltopdf.exe
    print(data['committeeName'])
    print(data['scheduledTime'][0:8])
    pdf_text="You are invited to meeting of "+ data['committeeName']+" scheduled on "+data['scheduledTime'][0:8]
    generate_pdf("meetings/templates/notice.pdf", pdf_text)
    #print(pdf)

    config = {
        "apiKey": "AIzaSyBcEBRIr1tmY_ZxuRgNN6cA1rLuhpr-KiA",
        "authDomain": "startup-fb1d9.firebaseapp.com",
        "projectId": "startup-fb1d9",
        "databaseURL" : "",
        "storageBucket": "startup-fb1d9.appspot.com",
        "messagingSenderId": "99269182406",
        "appId": "1:99269182406:web:ce541eb547617766ac68c7",
        "measurementId": "G-4MG5TT1N2K"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    path_on_cloud = "meeting/"+data['committeeName']+data['scheduledTime'][0:8]+random_char(random.randint(9, 20))+"_notice.pdf"
    path_local = 'meetings/templates/notice.pdf'
    print(storage.child(path_on_cloud).put(path_local))
    print(1)
    #print(storage.child(path_on_cloud).download("notice.pdf"))
    user={}
    user["idToken"]="100851090695921282290"
    url=storage.child(path_on_cloud).get_url(user["idToken"])
    #url=''
    print()
    print()
    print('this is the url',url)
    print()
    print()
    return url