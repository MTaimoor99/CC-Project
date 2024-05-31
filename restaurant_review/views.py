from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate,login as auth_login #For login and registration
from django.contrib import messages #For sending out flash messages
from django.contrib.auth.decorators import login_required #Needed to restrict access
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import logout #To log the user out
from .models import AttendanceRecord
from datetime import date,datetime,timedelta
#import datetime
from .helpers import generate_attendance_graph

# Create your views here.
@csrf_protect
def login(request):
     if request.user.is_authenticated:
        return redirect('index')
     else: 
        context={}
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)

            if user is not None:
                auth_login(request,user)
                return redirect('index')
            else:
                messages.info(request,'Username OR Password is incorrect')
                return render(request,'restaurant_review/Login.html',context)
        return render(request,'restaurant_review/Login.html',context)
     
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
                form.save() #Save to database
                user=form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user)
                return redirect('login')
        context={}
        context['form']=form
        return render(request,'restaurant_review/Register.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    if request.method=='POST':
        
        user=request.user
        current_time=datetime.now()
        current_time=current_time.strftime("%H:%M:%S")
        print(current_time)
        current_date=date.today()
        print(current_date)
        attendance_log=AttendanceRecord(user=user,timestamp=current_time,attendance_date=current_date)
        attendance_log.save()
        messages.success(request,"Your attendance has been successfully marked")
    return render(request,'restaurant_review/index.html')

@login_required
def details(request, id):
    print('Request for restaurant details page received')

@login_required
def attendance_history(request):
    print('Attendance History is here!')
    user = request.user
    attendance_records = AttendanceRecord.objects.filter(user=user)
    return render(request, 'restaurant_review/AttendanceHistory.html',{'attendance_records':attendance_records})


@login_required
def analytics_dashboard(request):
        user=request.user
        attendance_records = AttendanceRecord.objects.filter(user=user)
        date_list=[]
        for record in attendance_records:
            date_list.append(record.attendance_date)
        print(date_list)
        min_date=min(date_list)
        max_date=max(date_list)
        # Create a list of dates in the range from min_date to max_date
        date_range = [min_date + timedelta(days=i) for i in range((max_date - min_date).days + 1)]
        print(date_range)
        # Create a list of 0s and 1s representing presence or absence of dates in date_list
        presence_indicator = [1 if date in date_list else 0 for date in date_range]
        print(presence_indicator)
        attendance_plot=generate_attendance_graph(date_range,presence_indicator)
        return render(request, 'restaurant_review/AnalyticsDashboard.html',{'attendance_plot':attendance_plot})


@login_required
def add_review(request, id):
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        # Redisplay the form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        pass

    return HttpResponseRedirect(reverse('details', args=(id,)))
