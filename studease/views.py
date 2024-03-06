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
from .models import RollNumber,SubSection,TimeTable, vacantvenue # type: ignore
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
    return redirect("/")


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
    beams_client = PushNotifications(
    instance_id='55ce1d19-843c-4b89-8476-fa7f264cba16',
    secret_key='CD131592DFB7DAA3E3D7F5AC314182F0D26A7D08002D90A731733A75B390D3AA',
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
#val:13:40:00
def periodreturn(val):
    if   '08:30' <val<'09:25':
        return 'p1'
    if   '09:25' <val<'10:40':
        return 'p2'
    if   '10:40' <val<'11:35':
        return 'p3'
    if   '11:35' <val<'12:30':
        return 'p4'
    if   '12:30' <val<'13:45':
        return 'p5'
    if   '13:45' <val<'14:40':
        return 'p6'
    if   '14:40' <val<'15:35':
        return 'p7'
    if   '15:35' <val<'16:30':
        return 'p8'
    if   '16:30' <val<'17:25':
        return 'p9'
    if   '17:25' <val<'18:20':
        return 'p10'

def buddyship(request):
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    context ={
                "welcomenote": usercreated.username,
            }
    return render(request,'buddyship.html',context)

def resultbuddyship(request):
    print('hello')
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    sub_section_free_value={}
    if request.method == 'POST':
        print('hi')
        my_datetime_str = request.POST.get('datetime')
        # Convert the string to a datetime object
        if my_datetime_str is not None:
            my_datetime = datetime.strptime(my_datetime_str, '%Y-%m-%dT%H:%M')
            print(my_datetime)
            day_of_week = my_datetime.strftime('%A')
            time_of_day = my_datetime.strftime('%H:%M')
            print(time_of_day)
            if day_of_week =='Monday':
                time_empty= TimeTable.objects.filter(monday='',period=periodreturn(time_of_day))
                object_free_subsection=time_empty.values('sub_section_id')
                sub_section_free=SubSection.objects.filter(id__in=object_free_subsection)
                sub_section_free_value=sub_section_free.values('sub_section_name')
            if day_of_week =='Tuesday':
                time_empty= TimeTable.objects.filter(tuesday='',period=periodreturn(time_of_day))
                object_free_subsection=time_empty.values('sub_section_id')
                sub_section_free=SubSection.objects.filter(id__in=object_free_subsection)
                sub_section_free_value=sub_section_free.values('sub_section_name')
            if day_of_week =='Wednesday':
                time_empty= TimeTable.objects.filter(wednesday='',period=periodreturn(time_of_day))
                object_free_subsection=time_empty.values('sub_section_id')
                sub_section_free=SubSection.objects.filter(id__in=object_free_subsection)
                sub_section_free_value=sub_section_free.values('sub_section_name')
            if day_of_week =='Thursday':
                time_empty= TimeTable.objects.filter(thursday='',period=periodreturn(time_of_day))
                object_free_subsection=time_empty.values('sub_section_id')
                sub_section_free=SubSection.objects.filter(id__in=object_free_subsection)
                sub_section_free_value=sub_section_free.values('sub_section_name')
        else:
            print("Error: my_datetime_str is None")
        
    context ={
                "welcomenote": usercreated.username,
                'sub_section_free_value':sub_section_free_value,
            }
    return render(request,'resultbuddyship.html',context)

def serviceworker(request):
    return render(request,'service-worker.js')

def vacantvenues(request):
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    context={
        "welcomenote": usercreated.username,
    }
    return render(request,'vacantvenue.html',context)

def resultvacantvenue(request):
    usercreated = RollNumber.objects.get(roll_number=request.user.username)
    vacant={}
    if request.method =="POST":
        my_datetime_str = request.POST.get('datetime')
            # Convert the string to a datetime object
        if my_datetime_str is not None:
            my_datetime = datetime.strptime(my_datetime_str, '%Y-%m-%dT%H:%M')
            print(my_datetime)
            day_of_week = my_datetime.strftime('%A')
            time_of_day = my_datetime.strftime('%H:%M')
            dummy_vacantvenue= vacantvenue.objects.filter(day=day_of_week)
            # print(periodreturn(time_of_day))
            if periodreturn(time_of_day) is'p1':
                vacant = dummy_vacantvenue.filter(p1=0).values('room')
            if periodreturn(time_of_day) is 'p2':
                vacant = dummy_vacantvenue.filter(p2=0).values('room')
                print(vacant)
            if periodreturn(time_of_day) is 'p3':
                vacant = dummy_vacantvenue.filter(p3=0).values('room')
            if periodreturn(time_of_day) is 'p4':
                vacant = dummy_vacantvenue.filter(p4=0).values('room')
            if periodreturn(time_of_day) is 'p5':
                vacant = dummy_vacantvenue.filter(p5=0).values('room')
            if periodreturn(time_of_day) is 'p6':
                vacant = dummy_vacantvenue.filter(p6=0).values('room')
            if periodreturn(time_of_day) is 'p7':
                vacant = dummy_vacantvenue.filter(p7=0).values('room')
            if periodreturn(time_of_day) is 'p8':
                vacant = dummy_vacantvenue.filter(p8=0).values('room')
            if periodreturn(time_of_day) is 'p9':
                vacant = dummy_vacantvenue.filter(p9=0).values('room')
            if periodreturn(time_of_day) is 'p10':
                vacant = dummy_vacantvenue.filter(p10=0).values('room')
        else:
            print("Error: my_datetime_str is None")
    context={
        'welcomenote':usercreated.username,
        'vacantvenue':vacant
    }
    return render(request,'resultvacantvenue.html',context)


def roomrover(request):
    return render(request,'roomrover.html')