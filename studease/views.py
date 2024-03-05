from django.shortcuts import render,HttpResponse,redirect
#added manually
from datetime import datetime
#added manually to display allert messages..
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from studease.models import userfeedbacktable
from pusher_push_notifications import PushNotifications
# from studease.models import YourNewTable
# from .models import SubSection
#It is the main index page
from .models import RollNumber,SubSection,TimeTable
import uuid
from pusher import Pusher
def my_view(request):
    # Query the database using the model
    # data = loginDetails.objects.all()[0].username
    # new_record = loginDetails(username='Example', password='This is an example.')
    # new_record.save()
    # Use the data in your view
    # context = {"data": data}
    # return render(request, 'test.html', context)
    # main_elements = SubSection.objects.all()
    # user_data = request.user.username
    # context={
    #     'main_elements': main_elements,
    #     'user_data1':user_data,
    # }
    return render(request, 'test.html')


def index(request):
    #variable can be sent through this method..
    #context is a dictonary of variables
    #it is used to fetch data from table
    #we will replace this will request.user
    print(request.user)
    # request.user.username
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    # section = SubSection.objects.get(id=user.sub_section)
    # print(usercreated.sub_section.sub_section_name)
    indexcontext={
            "welcomenote": usercreated.username
    }
    #this is used to flash message on the web page
    # if request.method =="POST":
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     Contact = contact(email = email,name = name,date = datetime.today())
    #     Contact.save()
    #     messages.success(request, "this is a text message")
    # print(request.user)
    print("hello")
    if request.method == "POST":
        print("hi")
        feedbackfirstname= request.POST.get('feedbackfirstname')
        feedbacklastname= request.POST.get('feedbacklastname')
        feedbackemail= request.POST.get('feedbackemail')
        feedbackmessage= request.POST.get('feedbackmessage')
        print(feedbackfirstname)
        print(feedbacklastname)
        feedback = userfeedbacktable(feedbackfirstname=feedbackfirstname,feedbacklastname=feedbacklastname,feedbackemail=feedbackemail,feedbackmessage=feedbackmessage)
        feedback.save()
    # print(request.user)
    if request.user.is_anonymous:
        return redirect('login')
    return render(request,'index.html',indexcontext)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request,'Invalid Username or Password')
            return redirect("login")
    else:
        return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("/login")


def signUpUser(request):
    if request.method == 'POST':
        # Extract data from the form
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')

        # Check if the user already exists
        if not User.objects.filter(username=username).exists():
            # Create a new user
            if pass1==pass2:
                user = User.objects.create_user(username, email, pass1)

                # Additional fields (optional)
                user.first_name = request.POST.get('fname', '')
                user.last_name = request.POST.get('lname', '')
                user.save()

                #log in the user
                login(request, user)
            else:
                return HttpResponse("Password doesn't match")
            print(f'User {username} created successfully.')
        else:
            print(f'User {username} already exists.')

    return redirect("index")


def usertimetable(request):
    # name_value = YourNewTable.objects.all()[2]
    # desc_value = YourNewTable.objects.all()[2].description
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    # section = SubSection.objects.get(id=user.sub_section)
    # print(usercreated.sub_section.sub_section_name)

    # logic to display date and time on website
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.strftime("%B")
    date = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second
    currentday = current_datetime.strftime("%A") 

    #logic to display classes on that particular day 

    sub_section_user = usercreated.sub_section
    print(sub_section_user)
    timetable_variable = TimeTable.objects.filter(sub_section_id=sub_section_user)
    print(timetable_variable)

    if currentday == "Monday":
        print("today is monday")
        table_data = timetable_variable.values('monday','time','newtime')
    if currentday == "Tuesday":
        print("today is tuesday")
        table_data = timetable_variable.values('tuesday','time','newtime')
    if currentday == "Wednesday":
        table_data = timetable_variable.values('wednesday','time','newtime')
    if currentday == "Thursday":
        table_data = timetable_variable.values('thursday','time','newtime')
    if currentday == "Saturday":
        table_data = timetable_variable.values('saturday','time','newtime')
    print(table_data ,"\n")
    senduserid=str(uuid.uuid4())
    print(senduserid)


    beams_client = PushNotifications(
    instance_id=str(uuid.uuid4()),
    secret_key='XTELaPqb7HwKBPXK5IB3P5bWmvaYbDvEvj6_W9v3sco',
    )
    response = beams_client.publish_to_interests(
    interests=['donuts'],
    publish_body={
    'apns': {
      'aps': {
        'alert': {
          'title': 'Hello',
          'body': 'Hello, world!',
        },
      },
    },
    'fcm': {
      'notification': {
        'title': 'Hello',
        'body': 'Hello, world!',
      },
    },
    'web': {
      'notification': {
        'title': 'Hello',
        'body': 'Hello, world!',
      },
    },
  },
)
    print(response['publishId'])
    contextusertimetable={
                "senduserid":senduserid,
                "welcomenote": usercreated.username,
                "currentday": currentday,
                "year":year,
                "month":month,
                "hour":hour,
                "minute":minute,
                "second":second,
                "date":date,
                "display_table_data":table_data,

        }
    return render(request, 'usertimetable.html',contextusertimetable) # type: ignore

def homepage(request):
    if request.method == "POST":
        print("hi")
        feedbackfirstname= request.POST.get('feedbackfirstname')
        feedbacklastname= request.POST.get('feedbacklastname')
        feedbackemail= request.POST.get('feedbackemail')
        feedbackmessage= request.POST.get('feedbackmessage')
        print(feedbackfirstname)
        print(feedbacklastname)
        feedback = userfeedbacktable(feedbackfirstname=feedbackfirstname,feedbacklastname=feedbacklastname,feedbackemail=feedbackemail,feedbackmessage=feedbackmessage)
        feedback.save()
    if not request.user.is_anonymous:
        return redirect('index')
    return render(request,"homepage.html")


def base(request):
    return render(request,"base.html")


def test(request):
    roll_numbers = RollNumber.objects.all().select_related('sub_section')
    context = {'roll_numbers': roll_numbers}
    return render(request,"test.html",context)


def testweb(request):
    return render(request,'testweb.html')


def usertimetableindex(request):

    return render(request,'usertimetableindex.html')


def buddyship(request):

    if request.method =="POST":
        usertimestart=request.POST.get('timestart')
        usertimeend = request.POST.get('timeend')
        userday=request.POST.get('')

    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.strftime("%B")
    date = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second
    currentday = current_datetime.strftime("%A")

    time_empty= TimeTable.objects.filter(monday='')
    print(time_empty.values('sub_section_id'))
    # sub_section_available= time_empty.sub_section_name

    # print(sub_section_available)
    context ={
        "welcomenote": usercreated.username,

    }
    return render(request,'buddyship.html',context)

def serviceworker(request):
    return render(request,'service-worker.js')