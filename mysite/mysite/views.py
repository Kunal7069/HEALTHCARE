
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from login.models import *
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
# from _future_ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime,date
import numpy as np

from mysite.tasks import add


def sheet():
    entriesadded=EntriesAdded.objects.filter(name='LadleUpdateRoomWise')
    count=entriesadded[0].count
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1AQ6TgA_hm2bocR8eEwC9WLBDc7vScjg2ZhKAwAvIIBQ'
    SAMPLE_RANGE_NAME = 'Sheet1'
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)
    if not creds or not creds.valid:
    
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r"C:\Users\jaink\Desktop\LADLE TRACKER\mysite\mysite\credentials.json",SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json","w") as token:
            token.write(creds.to_json())
    service = build("sheets","v4", credentials=creds)
    sheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet['sheets']
    today = date.today()
    today = str(today)
    # Print sheet names
    for sheet in sheets:
        sheet_title = sheet['properties']['title']
        if sheet_title == today:
            break
    else:
        
    # Create a new sheet with today's date as the name
        request_body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': today
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(spreadsheetId= SPREADSHEET_ID , body=request_body).execute()
    # 

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{today}!A:G').execute()
    value = result.get('values',[])
    value = np.array(value)
    value=value[count:]
    ladleinfo=LadleInfo.objects.all()
    ladles=[]
    for x in ladleinfo:
            ladles.append(x.name)
    for l in ladles:
        for x in value:
            ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name=l,date=datetime.today().date())
            if len(ladleupdateroomwise)==0:
                name = l
                room=[]
                entry_time=[]
                exit_time=[]
                stop_points=[]
                if x[0]==name:
                    room.append(x[3])
                    entry_time.append(x[4])
                    exit_time.append(x[5])
                    string=""
                    for i in x[6]:
                        if i==",":
                            stop_points.append(string)    
                            string=""
                        else:
                            string=string+i  
                    stop_points.append(string)  
                    en=LadleUpdateRoomWise(name=name,entry_time=entry_time,room=room,exit_time=exit_time,stop_points=stop_points)
                    en.save()
                    count=count+1
            else:
                name_2 = l
                room=[]
                entry_time=[]
                exit_time=[]
                stop_points_1=[]
                stop_points_2=[]
                string=""
                for z in ladleupdateroomwise:
                    for y in z.stop_points:
                        if y=="'" and string!="":
                            stop_points_1.append(string)    
                            string=""
                        elif  y!="'" and y!="[" and y!="]" and y!=",":
                            string=string+y  
                for a in stop_points_1:
                        if a==" ":
                            stop_points_1.remove(a)
                string=""
                for z in ladleupdateroomwise:
                    for y in z.room:
                        if y=="'" and string!="":
                            room.append(string)    
                            string=""
                        elif  y!="'" and y!="[" and y!="]" and y!=",":
                            string=string+y     
                string=""
                for z in ladleupdateroomwise:
                    for y in z.entry_time:
                        if y=="'" and string!="":
                            entry_time.append(string)    
                            string=""
                        elif  y!="'" and y!="[" and y!="]" and y!=",":
                            string=string+y 
                string=""
                for z in ladleupdateroomwise:
                    for y in z.exit_time:
                        if y=="'" and string!="":
                            exit_time.append(string)    
                            string=""
                        elif  y!="'" and y!="[" and y!="]" and y!=",":
                            string=string+y 
                if x[0]==name_2:
                    room.append(x[3])
                    entry_time.append(x[4])
                    exit_time.append(x[5])
                    string=""
                    for i in x[6]:
                        if i==",":
                            stop_points_2.append(string)    
                            string=""
                        else:
                            string=string+i  
                    stop_points_2.append(string)
                    stop_points_3=stop_points_1+stop_points_2
                    datetime_objects = [datetime.strptime(timestamp, "%H:%M:%S") for timestamp in stop_points_3]
                    sorted_datetime_objects = sorted(datetime_objects)
                    sorted_timestamps = [datetime.strftime(dt, "%H:%M:%S") for dt in sorted_datetime_objects]
                    for a in room:
                        if a==" ":
                            room.remove(a)
                    for a in entry_time:
                        if a==" ":
                            entry_time.remove(a)
                    for a in exit_time:
                        if a==" ":
                            exit_time.remove(a)
                    LadleUpdateRoomWise.objects.filter(name=name_2,date=datetime.today().date()).update(entry_time=entry_time,room=room,exit_time=exit_time,stop_points=sorted_timestamps)
                    count=count+1
    EntriesAdded.objects.filter(name="LadleUpdateRoomWise").update(count=count)
    return count
    

def home(request):
    ans=sheet()
    ladleupdate=LadleUpdate.objects.filter(name='24')
    ladleinfo=LadleInfo.objects.filter(name='24')
    ladleupdateroomwise1=LadleUpdateRoomWise.objects.filter(name='24')
    
    start_time=[]
    stop_points=[]
    stop_time=[]
    turnover_time=[]
    work=[]
    stoppoint_time=[]
    data={}
    string=""
    for x in ladleinfo:
        for y in x.stop_point_work:
            if y=="'" and string!="":
                work.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdate:
        for y in x.stop_points:
            if y=="'" and string!="":
                stoppoint_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdate:
        for y in x.start_time:
            if y=="'" and string!="":
                start_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdate:
        for y in x.stop_points:
            if y=="'" and string!="":
                stop_points.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdate:
        for y in x.stop_time:
            if y=="'" and string!="":
                stop_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    no_of_turnover=len(stop_time)  
    start_stop_time = list(zip(start_time,stop_time))
    for x in start_stop_time:
        timestamp_format = "%H:%M:%S"
        result=datetime.strptime(x[1], timestamp_format)-datetime.strptime(x[0], timestamp_format)
        turnover_time.append(result) 
    time_slot=[]
    index=0
    for x in start_stop_time:
        time_slot.append(x[0])
        for i in range(0,(ladleinfo[0].stop_point_no-2)):
            time_slot.append(stop_points[(2*index)+i])
        index=index+1
        time_slot.append(x[1])
    for i in range(0,(ladleinfo[0].stop_point_no-2)):
        work=work+work
    task = list(zip(time_slot,work))
    for x in task:
        data[x[0]]=x[1]
    average_turnaround_time=0
    for x in turnover_time:
        dt_object = datetime.strptime(str(x), "%H:%M:%S")
        hour = dt_object.hour
        minute = dt_object.minute
        second = dt_object.second
        average_turnaround_time = average_turnaround_time+int((hour*60*60)+(60*minute)+second)
    
    hours, remainder = divmod(average_turnaround_time/no_of_turnover, 3600)
    minutes, seconds = divmod(remainder, 60)
    average_turnaround_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    return render(request,"dashboard.html",{'ladleupdateroomwise1':ladleupdateroomwise1,'ans':ans,'average_turnaround_time':average_turnaround_time,'stoppoint_time':stoppoint_time,'data':data,'work':work,'ladleinfo':ladleinfo,'ladleupdate':ladleupdate,'no_of_turnover':no_of_turnover,'start_time':start_time,'stop_time':stop_time,'turnover_time':turnover_time})

def home_2(request):
    # ans=sheet()
    ladleinfo=LadleInfo.objects.all()
    return render(request,"homepage.html",{'ladleinfo':ladleinfo})

def detail(request):
    ladlename = request.GET.get('ladlename')
    date='default'
    if request.method == 'POST':
        date = request.POST.get('date')
    if date=='default':
        date=datetime.today().date()
    ladleupdateroomwise1=LadleUpdateRoomWise.objects.filter(name=ladlename,date=date)
    ladleinfo=LadleInfo.objects.filter(name=ladlename)
    room=[]
    entry_time=[]
    exit_time=[]
    stop_points=[]
    stop_point_work=[]
    turnover_time=[]
    string=""
    for x in ladleinfo:
        for y in x.stop_point_work:
            if y=="'" and string!="":
                stop_point_work.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    string=""
    for x in ladleupdateroomwise1:
        for y in x.stop_points:
            if y=="'" and string!="":
                stop_points.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise1:
        for y in x.entry_time:
            if y=="'" and string!="":
                entry_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise1:
        for y in x.exit_time:
            if y=="'" and string!="":
                exit_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y 
    string=""
    for x in ladleupdateroomwise1:
        for y in x.room:
            if y=="'" and string!="":
                room.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y 
    for a in room:
        if a==" ":
            room.remove(a)
    for a in stop_points:
        if a==" ":
            stop_points.remove(a)
    for a in entry_time:
        if a==" ":
            entry_time.remove(a)
    for a in exit_time:
        if a==" ":
            exit_time.remove(a)
    for a in stop_point_work:
        if a==" ":
            stop_point_work.remove(a)
    list1 = list(zip(room,entry_time,exit_time))
    no_of_rounds=int(len(stop_points)/len(stop_point_work))
    start_time=[]
    for i in range(0,no_of_rounds):
        start_time.append(stop_points[(int(len(stop_point_work)))*i])
    stop_time=[]
    for i in range(1,no_of_rounds+1):
        stop_time.append(stop_points[((int(len(stop_point_work)))*i)-1])
    start_stop_time = list(zip(start_time,stop_time))
    for x in start_stop_time:
        timestamp_format = "%H:%M:%S"
        result=datetime.strptime(x[1], timestamp_format)-datetime.strptime(x[0], timestamp_format)
        turnover_time.append(result) 
    average_turnaround_time=0
    data=[]
    if no_of_rounds!=0:
        for x in turnover_time:
            dt_object = datetime.strptime(str(x), "%H:%M:%S")
            hour = dt_object.hour
            minute = dt_object.minute
            second = dt_object.second
            data.append(int((hour*60*60)+(60*minute)+second))
            average_turnaround_time = average_turnaround_time+int((hour*60*60)+(60*minute)+second)
        hours, remainder = divmod(average_turnaround_time/no_of_rounds, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_turnaround_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    for i in range(0,int(len(stop_points)/len(stop_point_work))):
        stop_point_work=stop_point_work+stop_point_work
    labels=[]
    for i in range(1,int(no_of_rounds)+1):
        labels.append('Round '+str(i))
    list2=list(zip(stop_points,stop_point_work))
        
    return render(request,"detail.html",{'ladlename':ladlename,'date':date,'list1':list1,'list2':list2,'no_of_rounds':no_of_rounds,'start_time':start_time,'stop_time':stop_time,'turnover_time':turnover_time,'average_turnaround_time':average_turnaround_time,'data':data,'labels':labels})

def find(request):
    ladleupdateroomwise=LadleUpdateRoomWise.objects.filter(name='24')
    entry_time=[]
    room=[]
    exit_time=[]
    string=""
    for x in ladleupdateroomwise:
        for y in x.entry_time:
            if y=="'" and string!="":
                entry_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    string=""
    for x in ladleupdateroomwise:
        for y in x.room:
            if y=="'" and string!="":
                room.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y   
    string=""
    for x in ladleupdateroomwise:
        for y in x.exit_time:
            if y=="'" and string!="":
                exit_time.append(string)    
                string=""
            elif  y!="'" and y!="[" and y!="]" and y!=",":
                string=string+y  
    for a in room:
        if a==" ":
            room.remove(a)
    for a in entry_time:
        if a==" ":
            entry_time.remove(a)
    for a in exit_time:
        if a==" ":
            exit_time.remove(a)            
    task = list(zip(entry_time,exit_time,room))
    time="19:42:01"
    result="none"
    for x in task:
        if datetime.strptime(time,"%H:%M:%S")>=datetime.strptime(x[0],"%H:%M:%S") and datetime.strptime(time,"%H:%M:%S")<=datetime.strptime(x[1],"%H:%M:%S"):
            result=x[2]
            break
        
    return render(request,"find.html",{'result':result})

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_frames_2():
    video_capture = cv2.VideoCapture(1)
    while True:
        # Read a frame from the webcam
        success, frame = video_capture.read()

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        # Yield the frame bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

def get_frames():
    laptop_camera = cv2.VideoCapture(0) 
    external_camera = cv2.VideoCapture(1)
    while True:
        # Read frames from the cameras
        success_laptop, frame_laptop = laptop_camera.read()
        success_external, frame_external = external_camera.read()

        # Convert the frames to JPEG format
        ret_laptop, jpeg_laptop = cv2.imencode('.jpg', frame_laptop)
        ret_external, jpeg_external = cv2.imencode('.jpg', frame_external)

        frame_bytes_laptop = jpeg_laptop.tobytes()
        frame_bytes_external = jpeg_external.tobytes()

        # Yield the frame bytes from both cameras
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_laptop + b'\r\n\r\n',
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_external + b'\r\n\r\n'
        )

@gzip.gzip_page
def live_feed(request):
    return StreamingHttpResponse(get_frames(), content_type="multipart/x-mixed-replace;boundary=frame")

def camera(request):
    return render(request,"camera.html")
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
# @gzip.gzip_page
# def video_feed_2(request):
#     return StreamingHttpResponse(generate_frames_2(),content_type="multipart/x-mixed-replace;boundary=frame")

