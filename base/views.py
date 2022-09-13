from contextlib import redirect_stderr
from multiprocessing import Event, context
from traceback import print_tb
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from .models import Events,Pictures,Speakers,Brochures
import datetime
from .form import EventsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import CharField,TextField
from django.db.models import  Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
import json

def paginate(obj,page_number):
    p = Paginator(obj, 30)
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    return page_obj


def home(request):

    #PAGINATION start
    events = Events.objects.all()
    p = Paginator(events, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    print("total number of pages are ",p.num_pages)
    context = {'events': page_obj,'p_count':p.num_pages}
    return render(request, 'base/home.html', context)
     #PAGINATION Ends


def like(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        print("got here --------------------------",id)
        value = request.POST.get('key', None)
        print("got key as",value)
        event = Events.objects.filter(id=id)[0]
        print(event)
        print("rn likes is ")
        if value=="like":
            print("in the like option")
            event.num_likes=event.num_likes+1
        else:
            print("in the else option**")
            event.num_likes=event.num_likes-1
        # event.num_likes=0
        event.save()
        ctx = {'likes_count':event.num_likes}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
       
    
   
#browse by campus
def browse_campus(request,key):
    print("-----------------got the key as ",key)
    events = Events.objects.filter(campus__contains=key)
    print("event is ",events)
    page_number=request.GET.get('page')
    events=paginate(events,page_number)
    context = {'events': events}
    return render(request, 'base/events.html', context)



# browse by tags
def browse_tags(request,key):
    events = Events.objects.filter(tags__contains=key)
    context = {'events': events}
    home(context)
    return render(request, 'base/home.html', context)

#browse by department
def browse_department(request,key):
    events = Events.objects.filter(department__contains=key)
    context = {'events': events}
    return render(request, 'base/home.html', context)



def Event_search(request):
    search_term = ''

    if 'search_term' in request.GET:
        print("-----------------------got inside")
        search_term = request.GET['search_term']
        fields = [f for f in Events._meta.fields if isinstance(f, CharField) or isinstance(f, TextField)]
        queries = [Q(**{f.name: search_term}) for f in fields]

        qs = Q()
        for query in queries:
            qs = qs | query
        eventsearch = Events.objects.filter(qs)
        page_number=request.GET.get('page')
        eventsearch=paginate(eventsearch,page_number)
        
        print("event search isjahskjdhk ",eventsearch)
        return render(request, 'base/events.html', {'events' : eventsearch, 'search_term': search_term })
    return HttpResponse("No Result")

def events(request):
    events = None

    return render(request, 'base/dashboard.html')
def Edit_Event1(request,pk):
    event = Events.objects.get(id=pk)
    if request.method == 'POST':
        form = EventsForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
    form=EventsForm(instance=event)
    context={'context':form}
    return render(request,'base/edit-event1.html',context)

def Edit_Event(request,pk):
    form = Events.objects.get(id=pk)
    pictures = Pictures.objects.filter(event_id=pk)
    speaker = Speakers.objects.filter(event_id=pk)
    brouchers = Brochures.objects.filter(event_id=pk)

    if request.method=="POST":
        
        form.title = request.POST.get('title')
        # form.name = request.POST.get('description')
        form.about = request.POST.get('about')
        form.event_start_date = request.POST.get('start_date')
        form.event_end_date = request.POST.get('end_date')
        department = request.POST.getlist('department[]')
        form.department=",".join(department)
        print("check list data ",department)
        campus = request.POST.getlist('campus[]')
        form.campus=",".join(campus)
        print("check list data ",campus)
        tags = request.POST.getlist('tag[]')
        form.tags=",".join(tags)
        print("check list data ",tags)
        form.email = request.POST.get('email')
        if len(request.FILES) != 0:
         form.featured_img = request.FILES.get('featured_img')
        form.event_start_time = request.POST.get('start_time')
        form.event_end_time = request.POST.get('end_time')
        form.contact = request.POST.get('contact')
        form.address = request.POST.get('address')
        form.is_online_event = request.POST.get('is_online_event')
        form.website = request.POST.get('website')
        form.facebook = request.POST.get('facebook')
        form.youtube = request.POST.get('youtube')
        form.instagram = request.POST.get('instagram')
        form.twitter = request.POST.get('twitter')
        form.external_link = request.POST.get('external_link')
        form.button_name = request.POST.get('button_name')
        form.custom_text = request.POST.get('custom_text')
        speaker.name = request.POST.get('spkr_name')
        speaker.about = request.POST.get('spkr_about')
        speaker.profile_pic = request.FILES.get('spkr_profile_pic')
        brouchers.document = request.FILES.get('event_broucher')
        form.publish = 'publish'
        form.google_map = request.POST.get('google_map')
        form.attachment = request.POST.get('docs[]')
        form.save()
        speaker.event_id = form.id
        speaker.save()
        brouchers.event_id = form.id
        brouchers.save()
        

        files = request.FILES.getlist('event_images')
        for f in files:
            print('form.id is -------------',form.id)
            Pictures.objects.create(event_id=form.id,event_images=f)
        
        return redirect('single-event',pk)
    # event=Events.objects.filter(id=pk).first()
    # print("got into edit event  id is ",pk,event,request.method)
    # form= EventsForm(instance=event)
    # if request.method == "POST":
    #     print("indide post method")
    #     form= EventsForm(request.POST,instance=event)
    #     if form.is_valid():
    #             print("form is valid-----------------")
    #             form.save()
    #             home(request)
    #     else:
    #         print("form is invalid &&&&&&&&^^^^^^^^",form)
    context = {
        "form":form,
        'pictures':pictures,
        'speaker':speaker,
        'brouchers':brouchers

    }
    return render(request, 'base/edit-event.html', context)

@login_required(login_url='login')
def createEvent(request):
    if request.method=="POST":
        form = Events()
        speaker = Speakers()
        brouchers = Brochures()
        form.title = request.POST.get('title')
        # form.name = request.POST.get('description')
        form.about = request.POST.get('about')
        form.event_start_date = request.POST.get('start_date')
        form.event_end_date = request.POST.get('end_date')
        department = request.POST.getlist('department[]')
        form.department=",".join(department)
        print("check list data ",department)
        campus = request.POST.getlist('campus[]')
        form.campus=",".join(campus)
        print("check list data ",campus)
        tags = request.POST.getlist('tag[]')
        form.tags=",".join(tags)
        print("check list data ",tags)
        form.email = request.POST.get('email')
        if len(request.FILES) != 0:
         form.featured_img = request.FILES.get('featured_img')
        form.event_start_time = request.POST.get('start_time')
        form.event_end_time = request.POST.get('end_time')
        form.contact = request.POST.get('contact')
        form.address = request.POST.get('address')
        form.is_online_event = request.POST.get('is_online_event')
        form.website = request.POST.get('website')
        form.facebook = request.POST.get('facebook')
        form.youtube = request.POST.get('youtube')
        form.instagram = request.POST.get('instagram')
        form.twitter = request.POST.get('twitter')
        form.external_link = request.POST.get('external_link')
        form.button_name = request.POST.get('button_name')
        form.custom_text = request.POST.get('custom_text')
        speaker.name = request.POST.get('spkr_name')
        speaker.about = request.POST.get('spkr_about')
        speaker.profile_pic = request.FILES.get('spkr_profile_pic')
        brouchers.document = request.FILES.get('event_broucher')
        form.publish = request.POST.get('publish')
        form.google_map = request.POST.get('google_map')
        form.attachment = request.POST.get('docs[]')
        form.save()
        speaker.event_id = form.id
        speaker.save()
        brouchers.event_id = form.id
        brouchers.save()
        

        files = request.FILES.getlist('event_images')
        for f in files:
            print('form.id is -------------',form.id)
            Pictures.objects.create(event_id=form.id,event_images=f)
            # images = Pictures.objects.all()
            # context ={'images':images}
        # else:
        #     images= Pictures.objects.all()
        home(request)
    
        
    context = {}
    return render(request, 'base/create-event.html', context)

def myListing(request):
    recent_events2 = Events.objects.all().order_by('-created_at')[:12]
    context={'recent_events2':recent_events2}
    return render(request, 'base/dashboard.html',context)  

def singlEvent(request,pk):
    
    countevent = Events.objects.get(id=pk)
    # countViews = Events.objects.get(id=pk)
    #to count the number of views
    # counts = request.session.get('count',countevent.view_count)
    # views = counts + 1
    # request.session['count'] = views
    # countViews.view_count = views
    # countViews.save()
    blog_object=Events.objects.get(id=pk)
    print('bhdfjbdfhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',blog_object)
    blog_object.view_count=blog_object.view_count + 1
    blog_object.save()
  #views
    event = Events.objects.get(id=pk)
    speaker =Speakers.objects.filter(event_id=pk)
    pictures = Pictures.objects.filter(event_id=pk)
    
    brouchures = Brochures.objects.filter(event_id=pk)
    recent_events = Events.objects.all().order_by('-created_at')[:4]
    context={'event':event,'speaker':speaker,'pictures':pictures,'brouchers':brouchures,'recent_events':recent_events,'blog_object':blog_object}
    return render(request, 'base/singlevent.html',context)  

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:    
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

        
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def updateEvent(request, pk):
    edited = Events.objects.get(id=pk)
    form = EventsForm(instance=edited)

    if request.method == 'POST':
        form = Events(request.POST, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "base/create-event.html", context)

# def blog_post (request,id):
    #your code
    # blog_object=Events.objects.get(id=id)
    # blog_object.postviews=blog_object.postviews+1
    # blog_object.save()
@login_required(login_url='login')
def deleteEvent(request, pk):
    deleteEv = Events.objects.get(id=pk)
    deletePics = Pictures.objects.filter(event_id=pk)
    deletePics.delete()
    deleteEv.delete()
    return redirect('list')

#Delete method.


