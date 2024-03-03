from django.shortcuts import render,HttpResponse,redirect
#added manually
from datetime import datetime
#added manually to display allert messages..
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
# from studease.models import YourNewTable
# from .models import SubSection
#It is the main index page
from .models import RollNumber,SubSection,TimeTable
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
    data = User.objects.all()[0].username
    context={
            "variable": request.user
    }
    #this is used to flash message on the web page
    # if request.method =="POST":
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     Contact = contact(email = email,name = name,date = datetime.today())
    #     Contact.save()
    #     messages.success(request, "this is a text message")
    # print(request.user)
    print(request.user)
    if request.user.is_anonymous:
        return redirect('login')
    return render(request,'index.html',context)
# Create your views here.
#we use HttpResponse to render string directly..
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")

#It is used to create user in DATA BASE
def signUpUser(request):
    if request.method == 'POST':
        # Extract data from the form
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        email = request.POST.get('email')

        # Check if the user already exists
        if not User.objects.filter(username=username).exists():
            # Create a new user
            user = User.objects.create_user(username, email, password)

            # Additional fields (optional)
            user.first_name = request.POST.get('fname', '')
            user.last_name = request.POST.get('lname', '')
            user.save()

            #log in the user
            login(request, user)

            print(f'User {username} created successfully.')
        else:
            print(f'User {username} already exists.')

    return redirect("/")


def userTimeTable(request):
    # name_value = YourNewTable.objects.all()[2]
    # desc_value = YourNewTable.objects.all()[2].description
    username = request.user
    print(username)
    sub_sections = SubSection.objects.all()
    time_tables = TimeTable.objects.all()
    return render(request, 'usertimetable.html', { 'username' : username, 'sub_sections': sub_sections, 'time_tables': time_tables})