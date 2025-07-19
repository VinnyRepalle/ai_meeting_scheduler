from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import MeetingForm
from .models import Meeting
from django.utils import timezone
import logging
from .utils import create_zoom_meeting

logger = logging.getLogger(__name__)






def schedule_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)

            if meeting.platform == "zoom":
                zoom_link, actual_passcode = create_zoom_meeting(
                    meeting.title,
                    meeting.scheduled_time,
                    meeting.passcode
                )
                if zoom_link:
                    meeting.meeting_link = zoom_link
                if actual_passcode:
                    meeting.passcode = actual_passcode  

            meeting.save()
            return redirect('meetings:schedule_success')
    else:
        form = MeetingForm()

    return render(request, 'meetings/schedule.html', {'form': form})


def schedule_success(request):
    return render(request, 'meetings/success.html')


def list_upcoming_meetings(request):
    meetings = Meeting.objects.filter(scheduled_time__gte=timezone.now()).order_by('scheduled_time')
    return render(request, 'meetings/list.html', {'meetings': meetings})


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return render(request, 'meetings/detail.html', {'meeting': meeting})


def get_meetings_json(request):
    meetings = Meeting.objects.all().order_by('-scheduled_time')
    data = [
        {
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'platform': m.platform,
            'scheduled_time': m.scheduled_time.isoformat(),
            'meeting_link': m.meeting_link,
            'status': m.get_status_display(),
        }
        for m in meetings
    ]
    return JsonResponse(data, safe=False)


def meeting_list(request):
    meetings = Meeting.objects.all().order_by('-scheduled_time')
    return render(request, "meetings/meeting_list.html", {"meetings": meetings})
