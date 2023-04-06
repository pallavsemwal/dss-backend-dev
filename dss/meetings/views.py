from http.client import HTTPResponse
from sched import scheduler
from telnetlib import STATUS
from tokenize import group
from django.shortcuts import render
from psycopg2 import Timestamp
from requests import request
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
# from backports.zoneinfo import ZoneInfo
from rest_framework.decorators import authentication_classes, permission_classes
import datetime
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.contrib.auth.models import User
from django.core import serializers
from meetings.models import meetingGroup, meeting, document
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, FileResponse, HttpRequest
from meetings.serializer import meetingSerializer, meetingGroupSerializer
from meetings.createNotice import generate_pdf
from message.views import create_message
from details.models.department import department
from details.models.profile import Profile
from django.db import connection
import pdfkit
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
# import pyrebase
from meetings.notice import createNotice




@api_view(['POST'])
def createMeetingGroup(request):
    d= JSONParser().parse(request)
    print(d)
    try:
        u= User.objects.get(pk=d["memberSecretary"])
        m = meetingGroup.objects.create(committeeName=d["committeeName"],memberSecretary=u, isRecurring=d["isRecurring"],recurringTime=d["recurringTime"],groupMembers=d["groupMembers"],relatedDepartmentId=d["relatedDepartmentId"])
    except IntegrityError as execption:
        print(str(execption))
        return JsonResponse({"message":"Integrity error","success":"False"}, safe=False)
    except Exception as exception:
        print(str(exception))
        return JsonResponse({"message":"Failed To create user","success":"False"}, safe=False)
    return JsonResponse({"message":"Meeting Group Created","groupId":m.pk,"success":"True"}, safe=False);
# Create your views here.
@api_view(['POST'])
def createMeeting(request):

    d= JSONParser().parse(request)
    print(d)
    # print("new", d) 
    # print(d["scheduledTime"])
    # print(datetime)
    # print(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S %Z"))
    # print(datetime.datetime.now().strftime("YYYY-MM-DD HH:MM:ss TZ"))
    # meetingSubject
    # scheduledTime
    # noticeLink
    # doablesAssigned
    # agenda=JSONField(null=True)
    try:
        group= meetingGroup.objects.get(pk=d["groupId"])
        d['committeeName']=group.committeeName
        url=createNotice(request,d)
        relatedDocumentLink=[url]
        for receiver in group.groupMembers:
            data={
            "senderId": group.memberSecretary.pk,
            "receiverId": receiver,
            "messageType": "notice",
            "messageContent": d["meetingSubject"],
            "relatedDocumentLink": relatedDocumentLink,
            "scheduledDate": str(datetime.datetime.strptime(d["scheduledTime"],"%Y-%m-%d %H:%M:%S")),
            "committeeName": group.committeeName
            }

            response = create_message(data)
            print("response",response)


        
        obj=meeting.objects.create(groupId=group,
            meetingSubject=d["meetingSubject"],
            agenda=d['agenda'],
            priority=d['priority'],
            timestampCreation=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scheduledTime=datetime.datetime.strptime(d["scheduledTime"],"%Y-%m-%d %H:%M:%S"),noticeLink=url)
        print(obj.pk)
        document.objects.create(meetingId=obj,documentLink=url,uploadedBy=request.user.id)
                
    except IntegrityError as execption:
        print(str(execption))
        return JsonResponse("Integrity Error", status=200, safe=False)
    except Exception as exception:
        print(str(exception))
        return JsonResponse("Failed to create meeting: Try Again", status=200, safe=False)
    return JsonResponse("Meeting Created", status=200, safe=False)


@api_view(['POST'])
def uploadDocument(request):
    d= JSONParser().parse(request)
    print(d)
    d['uploadedBy']=request.user.id
    print(request.user.id)
    m= meeting.objects.get(pk=d['meetingId']);
    try:
        document.objects.create(documentLink= d['documentLink'], meetingId= m, uploadedBy= d['uploadedBy'])
    except IntegrityError as execption:
        print(str(execption))
        return JsonResponse("Integrity Error", status=200, safe=False)
    except Exception as exception:
        print(str(exception))
        return JsonResponse("Failed to upload Meeting: Try Again", status=200, safe=False)
    return JsonResponse("Document Uploaded", status=200, safe=False)




@api_view(["GET"])
@permission_classes([AllowAny])
def getAllMeetingsGroup(request):
    d=meetingGroup.objects.filter(groupMembers__contains=[request.user.pk])
    d=serializers.serialize('json',d)
    d=json.loads(d)
    print(d)
    return JsonResponse(d,status=status.HTTP_200_OK, safe=False)




@api_view(["GET"])
def getAllUsers(request):
    User=get_user_model()
    d=serializers.serialize('json', User.objects.all())
    d=json.loads(d)
    print(d)    
    return JsonResponse(d,status=status.HTTP_200_OK, safe=False)



@csrf_exempt
@api_view(['GET'])
def getAllDepartments(request):
    d=serializers.serialize('json', department.objects.all())
    d=json.loads(d)
    print(d)    
    return JsonResponse(d,status=status.HTTP_200_OK, safe=False)


#meeting main page api's
@api_view(['GET'])
def allDepartment(request):
    user_id=request.user.id
    d=Profile.objects.get(pk=user_id)
    out={"departments":[]}
    for dep in d.departments:
        out["departments"].append([department.objects.get(pk=dep).departmentName, dep])
    print(out)
    return JsonResponse(out,status=status.HTTP_200_OK, safe=False)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
        

@api_view(['GET'])
def upcomingMeetings(request):
    user_id=request.user.id
    page1=request.GET.get('page1')
    limit=request.GET.get('limit')
    print(user_id)
    # d=meeting.objects.filter(scheduledTime__gte=datetime.datetime.now())
    # d=serializers.serialize('json',d)
    # d=json.loads(d)
    # print(d)
    t=datetime.datetime.now()
    sql="""Select * from meetings_meeting
    left join meetings_meetingGroup on "groupId_id"="groupId" where "scheduledTime">=%s and %s=any("groupMembers") order by "scheduledTime"
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[t,user_id])
        row=dictfetchall(cursor)
    print(row)
    paginator=Paginator(row,limit)
    print("num", paginator.num_pages)
    try:
        content = paginator.page(page1).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list
    out={}
    out["num_pages"]=paginator.num_pages
    out["content"]= content
    return JsonResponse(out,status=status.HTTP_200_OK, safe=False)

    #return HttpResponse("Hello")

#department page api's
@api_view(['GET'])
def allMeetingGroup(request):
    # d= JSONParser().parse(request)
    id= request.GET.get('departmentId')
    print(id)
    d_id=id
    d_name=department.objects.get(pk=d_id).departmentName
    print(d_name)
    sql=""" select * from meetings_meetingGroup m left join auth_user u on m."memberSecretary_id"=u."id"
    where %s=any("relatedDepartmentId");
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[d_id])
        row=dictfetchall(cursor)
    out={
        "departmentName":d_name,
        "meetingGroups": row
    }
    # print(out)
    return JsonResponse(out,status=status.HTTP_200_OK, safe=False)



@api_view(["GET"])
def meetingDetail(request):
    # d_id= request.GET.get('meetingId')
    meet=meeting.objects.get(pk=request.GET.get('meetingId'));
    group=meetingGroup.objects.get(pk=meet.groupId.pk   )
    groupMembers= group.groupMembers
    out={}
    out["group"]={"name":meet.groupId.committeeName,"groupId":meet.groupId.pk}
    out["meetingSubject"]=meet.meetingSubject
    out["minutesOfMeeting"]=meet.minutesOfMeeting
    out["agenda"]=meet.agenda
    out["doablesAssigned"]=meet.doablesAssigned
    out["timestamp"]=meet.timestampCreation
    out["scheduledTime"]=meet.scheduledTime
    out["noticeLink"]=meet.noticeLink
    getUsers=""" select "id" as id, "first_name" as first_name, "last_name" as last_name,"email" as email  from auth_user
    where "id" in %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(getUsers,[tuple(groupMembers)])
        rows=dictfetchall(cursor)
        out["groupMembers"]=rows
    getDocuments =""" select * from meetings_document where "meetingId_id" = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(getDocuments,[request.GET.get('meetingId')])
        rows=dictfetchall(cursor)
        out["uploadedDocuments"]=rows
    getDoables= """ select * from doables_doable where "typeId" = %s """
    with connection.cursor() as cursor:
        cursor.execute(getDoables,[request.GET.get('meetingId')])
        rows=dictfetchall(cursor)
        out["doables"]=rows
    return JsonResponse(out, status=200, safe=False)
        # d=json.loads(d)
    # print(d)    
    # return JsonResponse(d,status=status.HTTP_200_OK, safe=False)
    # print(d_id)
    # getMeeting=""" select *  from meetings_meeting where "meetingId"=%s;
    # """
    # out={}
    # with connection.cursor() as cursor:
    #     cursor.execute(getMeeting,[d_id])
    #     row=dictfetchall(cursor)
    # out['meeting']=row
    # print(out)
    return JsonResponse(out, status=200, safe=False)


#meeting group page api's
@api_view (['GET'])
def meetingGroupDetails(request):  #meeting group name,member secretary name and past meeting info
    # d= JSONParser().parse(request)
    meetingGroupId=request.GET.get('meetingGroupId')
    page1=request.GET.get('page1')
    page2=request.GET.get('page2')
    limit=10  #content on a page
    out={}
    out["committeeName"]=meetingGroup.objects.get(pk=meetingGroupId).committeeName
    group=meetingGroup.objects.get(pk=meetingGroupId)
    print(group.memberSecretary.pk)
    memberSecretary=User.objects.get(pk=group.memberSecretary.pk).get_full_name()
    groupMembers= group.groupMembers
    print(groupMembers)
    out["memberSecretary"]=memberSecretary
    # out["groupMembers"]= groupMembers
    sql=""" select "scheduledTime" as  scheduledTime, "meetingSubject" as meetingSubject , "meetingId" as meetingId from meetings_meeting
        where "groupId_id"=%s order by "scheduledTime" desc ;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[meetingGroupId])
        row=dictfetchall(cursor)
    paginator=Paginator(row,limit)
    try:
        content = paginator.page(page1).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list
    out['pastMeetings']=content
    

    getUsers=""" select "id" as id, "first_name" as first_name, "last_name" as last_name,"email" as email  from auth_user
    where "id" in %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(getUsers,[tuple(groupMembers)])
        rows=dictfetchall(cursor)
    print(rows)
    paginator=Paginator(rows,limit)
    try:
        content = paginator.page(page2).object_list
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        content = paginator.page(1).object_list
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        content = paginator.page(paginator.num_pages).object_list


    out["groupMembers"]=content


    sql=""" select count(d."doableId") as totalDoable, sum(case d."completed" when true then 1 else 0 end) as completedDoable,
        d."assignedTo" as assignedTo, concat(u."first_name",u."last_name") as name from doables_doable d inner join meetings_meeting m on d."typeId"=m."meetingId"
        inner join public.auth_user u on u."id"= d."assignedTo" where m."groupId_id"=%s group by d."assignedTo",u."first_name",u."last_name"
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[meetingGroupId])
        row=dictfetchall(cursor)
    out["doables"]=row
    
    #print(out)
    return JsonResponse(out,status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def meetingGroupDoable(request):    #doable counts for each person and completed doable for each
    id=request.GET.get('groupId')
    meetingGroupId=id
    # sql=""" select count(d."doableId") as totalDoable, sum(case d."completed" when true then 1 else 0 end) as completedDoable,
    #     d."assignedTo" as assignedTo, concat(u."first_name",u."last_name") as name from doables_doable d left join meetings_meeting m on d."typeId"=m."meetingId"
    #     left join public.auth_user u on u."id"= d."assignedTo" where m."groupId_id"=%s group by d."assignedTo",u."first_name",u."last_name"
    # """
    sql="""
        select * from doables_doable d inner join meetings_meeting m on d."typeId"=m."meetingId" where m."groupId_id"=%s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql,[meetingGroupId])
        row=dictfetchall(cursor)
    print(len(row))
    paginator=Paginator(row,5)
    print(paginator.page(1))
    return JsonResponse(row,status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def totalMeeting(request):
    id=request.GET.get('groupId')
    meetingGroupId=id
    sql="""
        select count(m."meetingId") as totalMeeting from meetings_meeting m where m."groupId_id"=%s;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[meetingGroupId])
        row=dictfetchall(cursor)
    return JsonResponse(row,status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def doableCount(request):
    id=request.GET.get('groupId')
    meetingGroupId=id
    sql="""
        select count(d."doableId") as totalDoable, sum(case d."completed" when true then 1 else 0 end) as completedTotalDoable
        from doables_doable d left join meetings_meeting m on d."typeId"=m."meetingId"
    """
    with connection.cursor() as cursor:
        cursor.execute(sql,[meetingGroupId])
        row=dictfetchall(cursor)
    return JsonResponse(row,status=status.HTTP_200_OK, safe=False)


#put request
@api_view(['PUT'])
def updateMeetingGroup(request):
    d= JSONParser().parse(request)
    id=d['meetingGroupId']
    d.pop('meetingGroupId')
    print(id)
    try:
        meetingGroup.objects.filter(pk=id).update(**d)
    except IntegrityError as execption:
        print(str(execption))
        return HttpResponseBadRequest("Integrity error")
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to create user: Try Again")
    return HttpResponse("Meeting Group Updated")

@api_view(['PUT'])
def rescheduleMeeting(request):
    d= JSONParser().parse(request)
    meetingId=d['meetingId']

    try:
        meetingObj=meeting.objects.get(pk=meetingId)
        group= meetingGroup.objects.get(pk=meetingObj.groupId.groupId)
        print(1)

        for receiver in group.groupMembers:
            data={
            "senderId": group.memberSecretary.pk,
            "receiverId": receiver,
            "messageType": "notice",
            "messageContent": meetingObj.meetingSubject,
            "relatedDocumentLink": "https://www.clickdimensions.com/links/TestPDFfile.pdf",
            "scheduledDate": str(datetime.datetime.strptime(d["scheduledTime"],"%Y-%m-%d %H:%M:%S")),
            "committeeName": group.committeeName
            }
            response = create_message(data)
            print("response",response)
    
        meeting.objects.filter(pk=meetingId).update(scheduledTime=datetime.datetime.strptime(d["scheduledTime"],"%Y-%m-%d %H:%M:%S"))
                        
    except IntegrityError as execption:
        print(str(execption))
        return HttpResponseBadRequest("Integrity error")
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to reschedule meeting: Try Again")
    return HttpResponse("Meeting reschedule")
    


@api_view(['PUT'])
def updateMeeting(request):
    d= JSONParser().parse(request)
    id=d['meetingId']
    d.pop('meetingId')
    print(id)
    try:
        meeting.objects.filter(pk=id).update(**d)
    except IntegrityError as execption:
        print(str(execption))
        return HttpResponseBadRequest("Integrity error")
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to Update group: Try Again")
    return HttpResponse("Meeting Group Updated")

@api_view(['DELETE'])
def deleteMeetingGroup(request):
    id=request.GET.get('meetingGroupId')
    meetingGroupId=id
    
    try:
        meetingGroup.objects.get(pk=meetingGroupId).delete()
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to delete : Try Again")
    return HttpResponse("Meeting Group deleted")

@api_view(['DELETE'])
def deleteMeeting(request):
    id=request.GET.get('meetingId')
    meetingId=id
    
    try:
        meeting.objects.get(pk=meetingId).delete()
    except Exception as exception:
        print(str(exception))
        return HttpResponseBadRequest("Failed to delete : Try Again")
    return HttpResponse("Meeting deleted")
           



