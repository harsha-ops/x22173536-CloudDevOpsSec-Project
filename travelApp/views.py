# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-variable
# pylint: disable=unused-import
# pylint: disable=bad-whitespace
#pylint: disable=trailing-whitespace
#pylint: disable=lines-too-long


from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Vacations
from django.contrib import auth
# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    resultFromValidator = User.objects.registerValidator(request.POST)
    print("RESULT FROM VALIDATOR BELOW!")
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/signup")
    
    newUser= User.objects.create(Name= request.POST['name'], Username = request.POST['Uname'], Password= request.POST['pw'])
    print("HERE IS THE NEW USER")
    print(newUser)
    request.session['loggedInId']= newUser.id

    return redirect("/travels")




def login(request):
    print(request.POST)
    resultFromValidator = User.objects.loginValidator(request.POST)
    print("PRINT LOGIN VALIDATIONS HERE")
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/signin")

    UserMatch = User.objects.filter(Username= request.POST['username'])


   
   
    request.session['loggedInId'] = UserMatch[0].id
    
    return redirect("/travels")
    


def travels(request):
    loggedInUser = User.objects.get(id=request.session['loggedInId'])
    if 'loggedInId' not in request.session:
        messages.error(request, "Log in to view Page.")
        return redirect("/")

    

    context = {
        'loggedInId': loggedInUser,
        'allVacations': Vacations.objects.all(),
        'YourTrips': Vacations.objects.filter(PossibleTrips = loggedInUser),
        'otherTrips': Vacations.objects.exclude(PossibleTrips = loggedInUser)

    }
    return render(request, "travels.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def addtrip(request):
    return render(request, "addtrip.html")

def createtrip(request): 
    print(request.POST)
    resultFromValidator = Vacations.objects.vacationsValidator(request.POST)
    print(resultFromValidator)
    if len(resultFromValidator)> 0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/travels/add")
    newVacation= Vacations.objects.create(Name= request.POST['des'], TravelStart= request.POST['leave'], TravelEnd= request.POST ['return'], Plan= request.POST ['desc'], Traveler= User.objects.get(id=request.session['loggedInId'] ))
    return redirect("/travels")

def tripdetails(request, tripID): 
    context = {
        'trip2show' : Vacations.objects.get(id= tripID)

    }
    return render(request, "tripinfo.html", context)

def JoinTrip(request, tripID):
    loggedInUser = User.objects.get(id=request.session['loggedInId'])
    this_trip = Vacations.objects.get(id= tripID)
    this_trip.PossibleTrips.add(loggedInUser)
    
    return redirect("/travels")

def cancel(request, tripID): 
    loggedInUser = User.objects.get(id=request.session['loggedInId'])
    this_trip = Vacations.objects.get(id= tripID)
    this_trip.PossibleTrips.remove(loggedInUser)

    return redirect("/travels")


def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'signin.html')

def signout(request):
    return render(request,'index.html')