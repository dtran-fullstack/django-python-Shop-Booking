from django.shortcuts import render, redirect
from login_app.models import *
from shop_app.models import *
from dashboard_app.models import *
from django.contrib import messages
import datetime
import time

# Create your views here.
def render_main(request):
    if 'uid' not in request.session:
        return redirect('/login')
    customer = User.objects.get(id = request.session['uid'])
    
    context = {
        "employees" : User.objects.filter(user_type = 2),
        "customer" : customer,
        "services" : Service.objects.all(),
        "events" : customer.book_events.all(),
    }

    return render(request,'cust_appointment.html',context)

# Retrieve posts
def retrieve_post(request, eid):
    request.session['selected_id'] = eid
    employee = User.objects.get(id=request.session['selected_id'])
    print(employee.posts.first().image)
    context = {
        "posts" : employee.posts.all()
    }
    return render(request,'image.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

def register_event(request):
    if request.method == 'POST':
        errors = Event.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/customer')
        else:
            employee = User.objects.get(id=request.POST['employee'])
            customer = User.objects.get(id=request.session['uid'])
            booked_events = employee.has_events.filter(date=request.POST['date']) # all events for selected emplpyee on that date
            # Customer should not have more than 2 pending request
            # Customer should not have 2 pending requeset with same employee
            customer_events = customer.book_events.exclude(status=2) # get all accepted and pending events for customer  
            if len(customer_events) == 2:
                messages.error(request,"Unable to book a new appointment! Pending appointments reach limit!")
                return redirect('/customer')
            elif len(customer_events) == 1:
                # one employee per event
                if customer_events[0].employees.first().id == employee.id:
                    messages.error(request,f"Unable to book a new appointment! You already have one appointment with {employee.first_name}")
                    return redirect('/customer')
            # Check OVERLAP EVENTS
            # Convert time to sec 
            x = time.strptime(request.POST['time']+":00",'%H:%M:%S')
            request_time = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            for event in booked_events:
                x = time.strptime(str(event.time),'%H:%M:%S')
                check_time = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                print(f"Request: {request_time} - Booked_Event: {check_time}")
                if check_time + 3600 >= request_time or request_time + 3600 >= check_time:
                    messages.error(request, "Overlap Appointments")
                return redirect('/customer')

            # Create the appoinment
            desc = ""
            for service in request.POST.getlist('services[]'):
                desc += service + " | "
            event = Event.objects.create(
                date = request.POST['date'],
                time = request.POST['time'],
                description = desc,
            )
            event.employees.add(employee)
            event.customers.add(customer)
            messages.error(request,"Succefully Book")
    return redirect('/customer')

def cancel_appointment(request, id):
    event = Event.objects.get(id=id)
    event.status = 2
    event.save()
    return redirect('/customer')


    
