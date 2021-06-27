from django.shortcuts import render
from .forms import UserForm,UserProfileForm, EventForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.views import generic
import calendar
from django.contrib.auth.models import User
from .utils import Calendar
from .models import Event

def base(request):
    return render(request, 'base.html', {})

def home(request):
    return render(request, 'home.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
         user_form = UserForm(data=request.POST)
         profile_form = UserProfileForm(data=request.POST)
         if user_form.is_valid() and profile_form.is_valid():
             user = user_form.save()
             user.set_password(user.password)
             user.save()
             profile = profile_form.save(commit=False)
             profile.user = user
             profile.save()
             return HttpResponseRedirect(reverse('app:login'))
         else:
             print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form,
                                             'profile_form': profile_form,})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('app:calendar'))
            else:
                return HttpResponse("Account not active")
        else:
            context = {
                'message': "Username and Password are incorrect"
            }
            return render(request, "login.html", context)
    else:
        return render(request,'login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:base'))


def ycalendar(request):
    return render(request,'ycalendar.html',{})

def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('app:calendar'))
    return render(request, 'event.html', {'form': form})



def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def CalanderView1(request):
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)
    event_list = Event.objects.order_by('start_time')
    today = date.today()
    month = get_date(request.GET.get('month', None)).month

    return render(request, 'home.html', {'calendar': mark_safe(html_cal),
                                          'prev_month': prev_month(d),
                                          'next_month': next_month(d),
                                          'month':month,
                                          'today':today,
                                          'event':event_list})

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)
