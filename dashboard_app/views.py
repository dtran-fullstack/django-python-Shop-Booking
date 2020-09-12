from django.shortcuts import render, redirect
from login_app.models import *
from shop_app.models import *
from dashboard_app.models import *
import bcrypt
from django.contrib import messages
import datetime
from django.utils import timezone

SERVICES = [
    {"price": 35, "name": "Full Set Arcrylic"},
    {"price": 45, "name": "Full Set Arcrylic with Gel Polish"},
    {"price": 25, "name": "Fill"},
    {"price": 30, "name": "Fill with Gel Polish"},
    {"price": 55, "name": "Full Set Pink & White"},
    {"price": 40, "name": "Fill Pink & White"},
    {"price": 45, "name": "Dip"}, {"price": 5, "name": "Longer nails"},
    {"price": 20, "name": "Manicure"},
    {"price": 30, "name": "Mani w/ Gel Polish"}, {"price": 5, "name": "w/french"},
    {"price": 20, "name": "Gel Polish"}, {"price": 5, "name": "w/french"},
    {"price": 50, "name": "Pedicure & Manicure"},
    {"price": 35, "name": "Pedicure"},
    {"price": 5, "name": "Pedi w/ Gel Polish"}, {"price": 5, "name": "w/french"},
    {"price": 55, "name": "Deluxe Pedicure"},
    {"price": 65, "name": "Deluxe Pedicure with Gel"},
    {"price": 55, "name": "Full Set Ombre"},
    {"price": 40, "name": "Fill Ombre"},
    {"price": 5, "name": "Design"},
    {"price": 10, "name": "Cut"},
    {"price": 5, "name": "Take-off Gel"},
    {"price": 10, "name": "Take-off Acrylic"},
    {"price": 10, "name": "Eyebrow Wax"},
    {"price": 7, "name": "Lip Wax"},
    {"price": 15, "name": "Eyebrow + Lip Wax"},
    {"price": 5, "name": "Nails Repair"},
]


# Admin DASHBOARD
def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/login')
    # Create Serive table one time
    if Service.objects.first() == None:
        for service in SERVICES:
            Service.objects.create(
                name = service["name"],
                price = service["price"],
            )
    # When admin login, update the appointments list of any past due
    past_events = Event.objects.filter(date__lt = datetime.date.today())
    for event in past_events:
        print(event.date)
        event.status = 9 #completed
        event.save()

    context = {
        "users" : User.objects.exclude(user_type = 3),
    }
    return render(request, 'dashboard.html', context)

def new_employee(request):
    return render(request, 'new_employee.html')

def create(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        users = User.objects.filter(email=request.POST['email'])
        if users:
            messages.error(request, "Email is already taken!")
        elif len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                phone = request.POST['phone'],
                email = request.POST['email'],
                user_type = 2,
                password = pw_hash
            )
            return redirect('/dashboard')
    return redirect('/dashboard/new')

def logout(request):
    request.session.flush()
    return redirect('/')

# Employee PAYMENT
def render_activities(request,id):
    if 'uid' not in request.session:
        return('/login')
    # Get all today activities and get total earn and tip
    employee = User.objects.get(id=id)
    today_activities = employee.activities.all().filter(created_at__gte=datetime.date.today())

    # print(f'Activities: {today_activities} for {(datetime.datetime.today())}')
    total_today = 0
    tip_today = 0
    for activity in today_activities:
        total_today += activity.amount
        tip_today += activity.tip
        
    context = {
        "employee" : employee,
        "services" : Service.objects.all(),
        "total_today" : total_today,
        "tip_today" : tip_today,
    }
    return render(request,'employee.activities.html',context)
    
def process_today(request,id):
    if request.method == 'POST':
        employee = User.objects.get(id=id)
        # Register one activity and amount 
        # work = ""
        # for service in request.POST.getlist('services[]'):
        #     work += service + "/ "
        Activity.objects.create(
            # services = work,
            amount = float(request.POST['amount']),
            tip = float(request.POST['tip']),
            employee = employee
        )  
    return redirect(f'/dashboard/{id}/activities')

def process_period(request,id):
    if request.method == 'POST':
        print(request.POST['start'] + "and" + request.POST['end'])
        employee = User.objects.get(id=id)
        startdate = request.POST['start']
        enddate = request.POST['end']
        activities = employee.activities.all().filter(created_at__gte=startdate,created_at__lte=enddate)

        total_period = 0
        tip_period = 0
        for activity in activities:
            total_period += activity.amount
            tip_period += activity.tip
            print(f'Amount: {activity.amount} on {activity.created_at}')
        print (f'Total_Period: {total_period}')
    return redirect(f'/dashboard/{id}/activities')

# Employee APPOINTMENTS
def render_employee_events(request,id):
    # employee = User.objects.get(id=id)
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        # "events" : employee.has_events.all()
        "employee" : User.objects.get(id=id)
    }
    return render(request,'employee_appointments.html',context)

def event_action(request,id,eid,action):
    event = Event.objects.get(id=eid)
    if action == "accept":
        event.status = 1
        event.save()
    elif action == "decline":
        event.status = 2
        event.save()
    return redirect(f'/dashboard/{id}/profile')

# Edit Employees
def render_edit(request,id):
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        "employee" : User.objects.get(id=id)
    }
    return render(request,'edit.html',context)

def update(request,id,field):
    employee = User.objects.get(id=id)
    if request.method == 'POST':
        if field == "fname":
            if len(request.POST['fname']) < 2:
                messages.error(request,"Invalid first name")
                return redirect(f'/dashboard/{id}')
            employee.first_name = request.POST['fname']
        elif field == "lname":
            if len(request.POST['lname']) < 2:
                messages.error(request,"Invalid last name")
                return redirect(f'/dashboard/{id}')
            employee.last_name == request.POST['lname']
        elif field == "email":
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(request.POST['email']):
                messages.error(request,"Invalid Email")
                return redirect(f'/dashboard/{id}')
            employee.email == request.POST['email']
        elif field == "password":
            if len(request.POST['password']) < 8:
                messages.error(request,"Password should be at least 8 characters!")
                return redirect(f'/dashboard/{id}')
            elif request.POST['password'] != request.POST['confirm_password']:
                messages.error(request,"Confirm password doesn't match. Please confirm!")
                return redirect(f'/dashboard/{id}')
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            employee.password = pw_hash
        employee.save()
    return redirect(f'/dashboard/{id}')

# Change status to 9 as deleted
def remove(request,id):
    employee = User.objects.get(id=id)
    employee.user_type = 9
    employee.save()
    return redirect('/')

# Upload photos
def upload(request,id):
    if request.method == 'POST' and len(request.FILES)>0:
        employee = User.objects.get(id=id)
        print(f' this is file {request.FILES}')
        Post.objects.create(
            image = request.FILES['photo'],
            employee = employee,
        )
    return redirect(f'/dashboard/{id}/profile')

def remove_post(request,id,pid):
    print(f"uid: {id} and postID: {pid}")
    Post.objects.get(id=pid).delete()
    print("Complete delete")
    return redirect(f'/dashboard/{id}/profile')

