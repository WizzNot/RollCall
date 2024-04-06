from django.urls import path

from events import views

app_name = 'events'

urlpatterns = [
    path('add_event/', views.add_event, name='add_event'),
]
