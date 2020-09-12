from django.urls import path
from . import views


urlpatterns = [
    path('', views.render_main),
    path('logout', views.logout),
    path('create',views.register_event),
    # path('appointments',views.customer_manage),
    path('<int:id>',views.cancel_appointment),
    path('retrieve_post/<int:eid>',views.retrieve_post),
]