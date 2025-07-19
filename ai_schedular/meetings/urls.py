from django.urls import path
from . import views


app_name = "meetings"

urlpatterns = [
    # Meeting Views
    path("schedule/", views.schedule_meeting, name="schedule_meeting"), 
    path("success/", views.schedule_success, name="schedule_success"),
    path("list/", views.meeting_list, name="meeting_list"),
    path("detail/<int:meeting_id>/", views.meeting_detail, name="meeting_detail"),
    path("api/meetings/", views.get_meetings_json, name="meeting_json"),

  
]
