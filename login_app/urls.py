from django.urls import path
from . import views

urlpatterns = [
    # Render Home, Login and Register Pages
    path('', views.render_welcome),
    path('login', views.render_login),
    path('register', views.render_register),
    # # Process Login and Register
    path('process_login', views.login),
    path('process_register', views.register)
]