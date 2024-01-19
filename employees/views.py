from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Employees
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import re
# Create your views here.




#----------------userhomepage


@never_cache
def homepage(request):

  if 'user' in request.session:
    username=request.session['user']
    context={
      'name':username
    }
    
    return render(request,'home.html',context)
  
  else:
    return redirect('login')



#----------------userloginpage
@never_cache
def loginpage(request):
    
    if 'user' in request.session:
      return redirect('home')
    

    # elif 'admin' in request.session:
    #   return redirect('adminhome')
    
    

    if request.method=="POST":
      username=request.POST.get('username')
      password=request.POST.get('password')

      user=authenticate(request,username=username,password=password)
      if user is not None:
        login(request,user)
        request.session['user']=username
        return redirect('home')
      else:
        return render(request,'login.html',{'error_msg1':'invalid username or password!'})
        
    return render(request,'login.html') 



#----------------usersignuppage
@never_cache
def signuppage(request):
    

    if 'user' in request.session:
      return redirect('home')
    
   
    
    if request.method=="POST":
      username=request.POST.get('username')
      email=request.POST.get('email')
      password1=request.POST.get('password1')
      password2=request.POST.get('password2')

      regex_pattern=r'^[\w-]+$' 


      if not (username and email and password1 and password2):
        return render(request,'signup.html',{'error_msg':'please fill the required fields'})
      
      if not re.match(regex_pattern,username):
        return render(request,'signup.html',{'error_empty_name':'empty spaces are not allowed!'})

      elif User.objects.filter(username=username).exists():
        return render(request,'signup.html',{'error_user':'username already exists'})
      elif User.objects.filter(email=email).exists():
        return render(request,'signup.html',{'error_email':'email already exists'})
      
      elif password1!=password2:
        return render(request,'signup.html',{'error_pass':'password mismatch'})
      
      if not re.match(regex_pattern,password1):
        return render(request,'signup.html',{'error_empty_pass':'empty spaces are not allowed!'})
      
      else:
        user=User.objects.create_user(username=username,email=email,password=password1)
        user.save()
        return redirect('login')
    
    return render(request,'signup.html') 


#----------------userlogout
@never_cache
def logoutbutton(request):
  if 'user' in request.session:
   request.session.flush()
   logout(request)
  return redirect('login')


#--------------adminhomepage


@login_required(login_url='adminlogin')
@never_cache
def adminhomepage(request):

  users=User.objects.filter(is_staff=False)
  context={
    'data':users
  }
  return render(request,'admin_home.html',context)




#--------------adminloginpage

@never_cache
def adminloginpage(request):
  
    if 'admin' in request.session:
      return redirect('adminhome')
    

    # elif 'user' in request.session:
    #   return redirect('home')


    if request.method=="POST":
      username=request.POST.get('username')
      admin_password=request.POST.get('password')
    
      user=authenticate(request,username=username,password=admin_password)
      if user is not None and user.is_superuser:
        login(request,user)
        request.session['admin']=username
        return redirect('adminhome')
      else:
        return render(request,'admin_login.html',{'error_msg':'invalid username or password!'})

    return render(request,'admin_login.html')


#--------------adminlogout
@never_cache
def adminlogout(request):

  if 'admin' in request.session:
    del request.session['admin']
    logout(request)
    return redirect('adminlogin')




#--------------addingdata

def add(request):

  if request.method=='POST':
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')

    if User.objects.filter(username=name).exists():
      return render(request,'alert.html')
    else:

      data=User.objects.create_user(username=name,email=email,password=password)
      data.save()
      return redirect('adminhome')
  
  return render(request,'admin_home.html')




#--------------edit


def edit(request):
  data=User.objects.all()

  context={
    'data':data
  }

  return render(request,'admin_home.html',context)


#--------------update


def update(request,id):

  if request.method=="POST":
    name=request.POST.get('name')
    email=request.POST.get('email')

    User.objects.filter(id=id).update(username=name,email=email)
    
    return redirect('adminhome')

  return render(request,'admin_home.html')


#--------------delete

def delete(request,id):

  data=User.objects.filter(id=id)
  data.delete()

  return redirect('adminhome')


#--------------search

def search(request):
  if 'q' in request.GET:

    q=request.GET['q']
    print(q)
    data=User.objects.filter(username__icontains=q)
    context={
      'data':data
    }

  return render(request,'admin_home.html',context)


#--------------alert

def alert(request):
  return redirect('adminhome')