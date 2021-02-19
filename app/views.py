from django.shortcuts import render, get_object_or_404, redirect
from app.models import App, SnapAndDetail, TechStack
from account.models import AppUser
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from PIL import Image


def checkIfMobile(current):
    img = Image.open(current.screenshot)
    width, height = img.size
    if height < width:
        return False
    return True


def make_like(request, app_id):
    app = get_object_or_404(App, pk=app_id)
    app.likes += 1
    app.save()
    return JsonResponse({'current_likes':app.likes})


@login_required
def createProject(request):
    if request.method == "GET":
        return render(request, 'app/create.html')
    else:
        if request.POST['projname'] and request.FILES['myfile'] and request.POST['desc']:
            app = App()
            app.appname = request.POST['projname']
            app.appIcon = request.FILES['myfile']
            app.intro = request.POST['desc']
            app.user = request.user
            app.created = timezone.datetime.now()
            app.gitlink =  request.POST['gitlink'] if( request.POST['gitlink'] != None )  else '#'
            app.videolink =  request.POST['vidlink'] if( request.POST['vidlink'] != None ) else '#'
            app.appstorelink = request.POST['appstorelink']  if( request.POST['appstorelink'] != None ) else '#'
            app.playstorelink = request.POST['playlink']  if( request.POST['playlink'] != None ) else '#'
            app.weblink =  request.POST['weblink'] if( request.POST['weblink'] != None ) else '#'
            app.save()
            return redirect('account:home')
        else:
            return render(request, 'app/create.html',{'error':'Please fill required fileds.'})



def showproject(request, app_id):
    app = get_object_or_404(App, pk=app_id)
    appUser = get_object_or_404(AppUser, user=app.user)
    snaps = SnapAndDetail.objects.filter(app = app)
    techstacks = TechStack.objects.filter(app = app)
    if(len(snaps) == 0):
        return render(request, 'app/display.html', {'app':app, 'appUser':appUser, 'snapAndDetail':None, 'zero_length':True, 'techstacks':techstacks, 'ismobile':True})
    curr_snap = get_object_or_404(SnapAndDetail, pk=app.start_id)
    ismobile = checkIfMobile(curr_snap)
    return render(request, 'app/display.html', {'app':app, 'appUser':appUser, 'snapAndDetail':curr_snap, 'techstacks':techstacks, 'ismobile':ismobile})


def loadDataNext(request, app_id):
    snap_id = int(request.GET.get('snap_id',''))
    is_next = True if(request.GET.get('is_next',True)=='true') else False
    print(is_next)
    current = get_object_or_404(SnapAndDetail, pk=snap_id)
    if(is_next):
        next_obj = get_object_or_404(SnapAndDetail, pk=current.next_id)
    else:
        next_obj = get_object_or_404(SnapAndDetail, pk=current.prev_id)
    ismobile = checkIfMobile(next_obj)
    return JsonResponse({'header':next_obj.header, 'info':next_obj.info, 'image':next_obj.screenshot.url , 'ismobile':ismobile, 'curr_id':next_obj.id})



@login_required
def addSnap(request, app_id):
    if request.method == "POST":
        if request.POST['header'] and request.POST['info'] and request.FILES['myfile']:
            app = get_object_or_404(App, pk=app_id)
            snaps = SnapAndDetail.objects.filter(app=app)
            data_length = len(snaps)
            new_snap = SnapAndDetail()
            new_snap.header = request.POST['header']
            new_snap.info = request.POST['info']
            new_snap.screenshot = request.FILES['myfile']
            snap_id = request.POST['curr_snap_id']
            print('-----------------------------------------')
            print(request.POST['direction'])
            direction = True if(request.POST['direction'] == 'true') else False
            new_snap.app = app
            new_snap.save()
            if(data_length == 0):
                new_snap.next_id = new_snap.id
                new_snap.prev_id = new_snap.id
                new_snap.save()
                app.start_id = new_snap.id
                app.save()
                return JsonResponse({'zero_length':True, 'new_id':new_snap.id})
            elif(data_length == 1):
                curr_snap = get_object_or_404(SnapAndDetail, pk=snap_id)
                new_snap.next_id = curr_snap.id
                new_snap.prev_id = curr_snap.id
                curr_snap.next_id = new_snap.id
                curr_snap.prev_id = new_snap.id
                new_snap.save()
                curr_snap.save()
                #set start
                if(direction):
                    pass
                else:
                    app.start_id = new_snap.id
                    app.save()
            else:
                if(direction): # after
                    curr_snap = get_object_or_404(SnapAndDetail, pk=snap_id)
                    next_snap = get_object_or_404(SnapAndDetail, pk = curr_snap.next_id)
                    new_snap.next_id = next_snap.id
                    new_snap.prev_id = curr_snap.id
                    curr_snap.next_id = new_snap.id
                    next_snap.prev_id = new_snap.id
                    new_snap.save()
                    curr_snap.save()
                    next_snap.save()
                else:
                    curr_snap = get_object_or_404(SnapAndDetail, pk=snap_id)
                    prev_snap = get_object_or_404(SnapAndDetail, pk = curr_snap.prev_id)
                    new_snap.next_id = curr_snap.id
                    new_snap.prev_id = prev_snap.id
                    prev_snap.next_id = new_snap.id
                    curr_snap.prev_id = new_snap.id
                    new_snap.save()
                    curr_snap.save()
                    prev_snap.save()
                    # set start
                    if(curr_snap.id == app.start_id):
                        app.start_id = new_snap.id
                        app.save()

            return JsonResponse({'zero_length':False, 'new_id':new_snap.id})
        else:
            return JsonResponse({'zero_length':False,'error':'Error in this context'})



def deleteSnap(request, app_id):
    if request.method == "POST":
        app = get_object_or_404(App, pk=app_id)
        snap_id = request.POST['snap_id']
        curr_snap = get_object_or_404(SnapAndDetail, pk=snap_id)
        snaps = SnapAndDetail.objects.filter(app=app)
        if(len(snaps) == 1):
            curr_snap.delete()
            app.start_id = -1
            app.save()
            return JsonResponse({'zero_length':True})
        elif(len(snaps) == 2):
            next_snap = get_object_or_404(SnapAndDetail, pk = curr_snap.next_id)
            next_snap.next_id = next_snap.id
            next_snap.prev_id = next_snap.id
            next_snap.save()
        else:
            prev_snap = get_object_or_404(SnapAndDetail, pk=curr_snap.prev_id)
            next_snap = get_object_or_404(SnapAndDetail, pk=curr_snap.next_id)
            prev_snap.next_id = curr_snap.next_id
            next_snap.prev_id = curr_snap.prev_id
            prev_snap.save()
            next_snap.save()
        if(app.start_id == curr_snap.id):
            app.start_id = next_snap.id
            app.save()
        curr_snap.delete()
        return JsonResponse({'zero_length':False, 'new_id':next_snap.prev_id})


@login_required
def editSnap(request, app_id):
    if request.method == "POST":
        snap_id = request.POST['snap_id']
        curr_snap = get_object_or_404(SnapAndDetail, pk=snap_id)
        print(curr_snap)
        if(request.POST.get('header', '') != ''):
            curr_snap.header = request.POST['header']
        if(request.POST.get('info', '') != ''):
            curr_snap.info = request.POST['info']
        if(request.FILES.get('myfile', '') != ''):
            curr_snap.screenshot = request.FILES.get('myfile')
        curr_snap.save()
        return JsonResponse({'new_id':curr_snap.prev_id})

@login_required
def deleteProject(request, app_id):
    if request.method == "POST":
        app = get_object_or_404(App, pk=app_id)
        app.delete()
        return redirect('account:home')


def deleteStack(request):
    if request.method == "POST":
        stack_id = request.POST['stack_id']
        curr_stack = get_object_or_404(TechStack, pk=stack_id)
        past_app = curr_stack.app
        print(curr_stack)
        curr_stack.delete()
        stack_list = []
        for tech in TechStack.objects.filter(app=past_app):
            print(tech.name)
            newobj = {
                'name':tech.name,
                'link':tech.link,
                'url':tech.icon.url,
                'id':tech.id
            }
            stack_list.append(newobj)
        return JsonResponse({'techstacks':stack_list})


def addStack(request, app_id):
    if request.method == "POST":
        if request.POST['name'] and request.POST['link'] and request.FILES['myfile']:
            app = get_object_or_404(App, pk=app_id)
            ts = TechStack()
            ts.name = request.POST['name']
            ts.link = request.POST['link']
            ts.icon = request.FILES['myfile']
            ts.app = app
            ts.save()
            stack_list = []
            for tech in TechStack.objects.filter(app=app):
                print(tech.name)
                newobj = {
                    'name':tech.name,
                    'link':tech.link,
                    'url':tech.icon.url,
                    'id':tech.id
                }
                stack_list.append(newobj)
            return JsonResponse({'techstacks':stack_list})
