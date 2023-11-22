#OLD
from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
  return render(request, 'basic_app/index.html')

@login_required
def special(request):
  return HttpResponse("You're logged in, awesome!")

#using login_required decorator to make sure only logged in users will be able to logout
@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))

def register(request):

  registered = False

  # user_form = None
  # profile_form = None
  if request.method == 'POST':
    user_form = UserForm(data = request.POST)
    profile_form = UserProfileInfoForm(data = request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit = False)
      profile.user = user

      if 'profile_pic' in request.FILES:
        print("found it")
        #in square brackets
        profile.profile_pic = request.FILES['profile_pic']
        profile.save()

        registered = True

      else:
        print(user_form.errors, profile_form.errors)

  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

  return render(request, 'basic_app/registration.html', 
                {'registered': registered, 
                 'user_form': user_form, 
                 'profile_form': profile_form})



def user_login(request):
  
  if request.method == 'POST':
    #fetching user details from login page
    username = request.POST.get('username')
    password = request.POST.get('password')

    #authenticaating user details
    user = authenticate(username=username, password=password)

    if user:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
      else:
        return HttpResponse("ACCOUNT NOT ACTIVE")
    else:
      print("Login Failed")
      print("Username : {} and Password : {}".format(username, password))
      return HttpResponse("Invalid Account Details Submitted")
  else:
    #nothin is provided for userrname and password
    return render(request,'basic_app/login.html')

  
