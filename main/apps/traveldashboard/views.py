from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from django.db.models import Q
from .models import User, Trip, Attending
# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/travels')
    return render(request, 'traveldashboard/index.html')

def register(request):
    check = User.userManager.checkreg(request.POST['name'], request.POST['username'], request.POST['pass'], request.POST['conf_pass'])
    if check == True:
        passinput = request.POST['pass'].encode()
        hashed = bcrypt.hashpw(passinput, bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed)
        return redirect('/')
    else:
        for error in check:
            messages.error(request, error)
        return redirect('/')

def login(request):
    check = User.userManager.checklog(request.POST['loginuser'], request.POST['loginpass'])

    if check[0] == True:
        request.session['user']=check[1].id
        return redirect('/travels')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/')

def logout(request):
    del request.session['user']
    return redirect('/')

def travels(request):
    if not 'user' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user'])
    usertrips = Trip.objects.filter(created_by=request.session['user'])
    tripsjoined = Attending.objects.filter(user_id=request.session['user'])
    excludeme = [o.id for o in tripsjoined]
    alltrips = Trip.objects.all()


    context = {
        'user':user,
        'usertrips':usertrips,
        'othertrips':tripsjoined,
        'alltrips': alltrips,
    }
    return render(request, 'traveldashboard/travels.html', context)

def add(request):
    if not 'user' in request.session:
        return redirect('/')
    return render(request, 'traveldashboard/add.html')

def new(request):
    check = Trip.tripManager.tripvalid(request.POST['destination'], request.POST['desc'], request.POST['datefrom'], request.POST['dateto'])
    if check == True:
        Trip.objects.create(destination=request.POST['destination'], description=request.POST['desc'],datefrom = request.POST['datefrom'], dateto = request.POST['dateto'], created_by = User.objects.get(id=request.session['user']))
        return redirect ('/travels')
    for error in check:
        messages.error(request, error)
    return redirect('/travels/add')

def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user'])
    Attending.objects.create(trip_id=trip, user_id=user)
    return redirect('/travels')


def destination(request, id):
    if not 'user' in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    context = {
        'trip':trip,
    }
    return render(request, 'traveldashboard/destination.html', context)
