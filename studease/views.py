from django.shortcuts import render,HttpResponse,redirect
#added manually
from datetime import datetime
#added manually to display allert messages..
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
import sqlite3
from .models import loginDetails
#It is the main index page
def my_view(request):
    # Query the database using the model
    data = loginDetails.objects.all()[3].username
    new_record = loginDetails(username='Example', password='This is an example.')
    new_record.save()
    # Use the data in your view
    context = {"data": data}
    return render(request, 'test.html', context)
def index(request):
    #variable can be sent through this method..
    #context is a dictonary of variables
    context={
            "variable":"this is sent"
    }
    #this is used to flash message on the web page
    # if request.method =="POST":
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     Contact = contact(email = email,name = name,date = datetime.today())
    #     Contact.save()
    #     messages.success(request, "this is a text message")
    print(request.user)
    if request.user.is_anonymous:
        return HttpResponse("Hello")
    return render(request,'index.html',context)
# Create your views here.
#we use HttpResponse to render string directly..
def loginUser(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check if user has entered correct credentials
        print(username,password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
    # A backend authenticated the credentials
        else:
            return render(request,'login.html')
    # No backend authenticated the credentials
        
    print(request.user)

    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

#It is used to create user in DATA BASE
def signUpUser(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        # check for erroneous input
        #
        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        print(myuser.username)
        print(myuser.first_name)
        print(myuser.last_name)
        print(myuser.email)
        messages.success(request, "Your account has successfully created")
    return render(request, 'signup.html')

