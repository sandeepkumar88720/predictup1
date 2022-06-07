from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from .graph import get_plot
# from .yahoo import df
# from .yahoo import y_test,y_predicted
from django.views.generic import TemplateView
import pandas as pd
import json

#home_page
def home_Page(request):
    return render(request, 'predict/home_page.html')


# #dshboard
# def dashboard(request):
#     y=df.Close
#     x=df.Date
#     chart = get_plot(request,x,y_test,y_predicted)
#     return render(request, 'predict/chart.html',{'chart':chart})
#

# Sign UP
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully !!')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, "predict/signup.html", {'form': fm})

# Login View
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in  Successfully !!')
                    return HttpResponseRedirect('/home_mpl/')
        else:
            fm =AuthenticationForm()
        return render(request, "predict/login.html", {'form': fm})
    else:
        return HttpResponseRedirect('/home_mpl/')

# User Profile
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'predict/profile.html ')
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# Change Password with old password
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed  Successfully !!')
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'predict/changepass.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')

# index

# def index(request):
#     #chart = {'chart':df}
#     chart = {'Date':df.Date,
#              'Open':df.Open,
#              'High':df.High,
#              'Low':df.Low,
#              'Close':df.Close,
#              'Volume':df.Volume}
#     #chart=json.dump(chart)
#     return chart #render(request, "predict/index.html", {'my_data':chart})

# class Index(TemplateView):
#     template_name = "predict/index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context=pd.DataFrame({'Date':df.Date,
#                                  'Open':df.Open,
#                                  'High':df.High,
#                                  'Low':df.Low,
#                                  'Close':df.Close,
#                                  'Volume':df.Volume})
#         dataframe={'context':context}
#         print(dataframe)
#
#         return (dataframe)


