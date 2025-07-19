from django import forms
from .models import Meeting
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'host_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'participant_emails': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'scheduled_time': forms.SplitDateTimeWidget(
                date_attrs={'class': 'form-control', 'type': 'date'},
                time_attrs={'class': 'form-control', 'type': 'time'}
            ),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'passcode': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get('scheduled_time')

        if isinstance(scheduled_time, list):
            try:
                scheduled_time = scheduled_time[0]
            except IndexError:
                raise ValidationError("Invalid scheduled time input.")
        
        if scheduled_time and scheduled_time < timezone.now():
            raise ValidationError("Scheduled time must be in the future.")
        return scheduled_time

    def clean_passcode(self):
        passcode = self.cleaned_data.get("passcode")
        if passcode and not re.fullmatch(r'[\w@\-_*]{1,10}', passcode):
            raise ValidationError("Passcode must be 1–10 characters and only contain a-z, A-Z, 0-9, @, -, _, *.")
        return passcode

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if isinstance(status, list):
            return status[0]
        return status
