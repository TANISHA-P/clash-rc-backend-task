from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.core.checks import messages
from .models import *
import re


def index(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            internal = request.POST['input']
            filter_type = request.POST['category']
            if(filter_type == 'firstc'):
                pattern = re.compile(r'[1-9]\d[1-9]\d*|[1-9]\d\d\d+')
            elif(filter_type == 'secondc'):
                pattern = re.compile(r'\b\d{4}[-]\d{2}[-]\d{2}\b')
            elif(filter_type == 'thirdc'):
                pattern = re.compile(r"'(.*)'")
            elif(filter_type == 'fourthc'):
                pattern = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
                match = pattern.findall(internal)[0]
                if(0<=int(match[0:3])<=127):
                    return render(request,'index.html',{
                        'ip':match,'class':'class A'
                    })
                elif(128<=int(match[0:3])<=191):
                    return render(request,'index.html',{
                        'ip':match,'class':'class B'
                    })
                elif(192<=int(match[0:3])<=223):
                    return render(request,'index.html',{
                        'ip':match,'class':'class C'
                    })
                elif(224<=int(match[0:3])<=239):
                    return render(request,'index.html',{
                        'ip':match,'class':'class D'
                    })
                elif(240<=int(match[0:3])<=255):
                    return render(request,'index.html',{
                        'ip':match,'class':'class E'
                    })
                else:
                    return render(request,'index.html',{
                        'class':'None of the Input didn\'t match the selected category.'
                    })
            elif(filter_type == "fifthc"):
                pattern = re.compile(r'[A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}[-:][A-F0-9a-f]{2}')
            elif(filter_type == "sixthc"):
                def func(x):
                    char = x.group(0)
                    return "_"+char.lower()
                pattern = re.compile(r'([A-Z])')
                match = pattern.sub(func,internal)
                return render(request,'index.html',{
                    'class':match
                })
            match = pattern.findall(internal)
            if(len(match) == 0):
                return render(request,'index.html',{
                    'class':'Input didn\'t match the selected category.'
                })
            return render(request,"index.html",{
                'output':match
            })
        return render(request, "index.html")
    else:
        return render(request,"login.html",{
            "message": "Login to Continue"
        })

def login_view(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        usermy = authenticate(request, username = username, password = password)
        if usermy is not None:
            login(request,usermy)
            return render(request,"index.html",{
                "message":"Successfully Logged In"
            })
        else:
            return render(request,"login.html",{
                "message": "Wrong Credentials. Enter Again."
            })
    return render(request,"login.html")

def register_view(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        if User.objects.filter(username = username).exists():
            return render(request,"registration.html",{
                'message':'This username already exists.'
            })
        
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            return render(request,'registration.html',{
                'message':'This Email is already associated with another user'
            })
        pattern = re.compile(r'[a-zA-Z0-9-.+]+@[a-zA-Z0-9-.+]+\.[a-zA-Z]+')
        match = pattern.findall(email)
        if(len(match)==0):
            return render(request,'registration.html',{
                'message':'Email entered, not in proper format.\nSpecial characters ($,#,&,%) not allowed'
            })

        mobile = request.POST.get('mobile')
        if (len(str(mobile)) != 10):
            return render(request,'registration.html',{
                'message':'Phone no. should be 10 number long.'
            })

        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if(pass1 != pass2):
            return render(request,'registration.html',{
                'message':'Passwords don\'t match'
            })
        
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        newUser = User.objects.create_user(username = username, email = email, password = pass1, first_name = fname,last_name = lname)
        newUser.save()
        profile = Registration(user_info = newUser, mobile = mobile, gender = gender, bday = dob)
        profile.save()
        return render(request,"login.html",{
            "message" : "Succesfully registered. Login to continue."
        })
    else:
        return render(request,"registration.html")

def logout_view(request):
    logout(request)
    return render(request,"logout.html")
