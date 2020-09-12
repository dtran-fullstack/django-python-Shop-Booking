from django.shortcuts import render, redirect
from login_app.models import *
from django.contrib import messages
import bcrypt

# Login and Register
def to_login(request):
    return redirect('/login')

# Login
def render_login(request):
    return render(request,'login.html')
    
def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # request.session['name'] = logged_user.fullname()
                request.session['uid'] = logged_user.id
                if (logged_user.user_type == 1):
                    return redirect('/dashboard')
                elif (logged_user.user_type == 2):
                    return redirect(f'/dashboard/{logged_user.id}/profile')
                else:
                    return redirect('/customer')
    messages.error(request,"Invalid email or incorrect password!")
    return redirect("/login")

# Register
def render_register(request):
    return render(request,'register.html')

def register(request):
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
            user = User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                phone = request.POST['phone'],
                email = request.POST['email'],
                password = pw_hash
            )
            if user.id == 1: 
                user.user_type = 1
                user.save()
            return redirect('/login')
    return redirect('/register')

