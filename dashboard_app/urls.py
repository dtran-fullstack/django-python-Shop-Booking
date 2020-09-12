from django.urls import path
from . import views

urlpatterns = [
    # ADMIN LOGIN
    path('',views.dashboard),
    path('logout',views.logout),
    # Add new employee
    path('new',views.new_employee),
    path('new/create',views.create),
    # Edit existing employee
    path('<int:id>',views.render_edit),
    path('<int:id>/update_<str:field>',views.update),
    path('<int:id>/remove',views.remove),
    # View my pay
    path('<int:id>/activities',views.render_activities),
    path('<int:id>/activities/today',views.process_today),
    path('<int:id>/activities/period',views.process_period),
    # View employee profile
    path('<int:id>/profile',views.render_employee_events, name = "root"),
    path('<int:id>/profile/<int:eid>/<str:action>',views.event_action), #accept or decline an appointment
    path('<int:id>/profile/upload',views.upload),
    path('<int:id>/<int:pid>/remove',views.remove_post), #remove a post
]