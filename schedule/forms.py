from django import forms
from .models import Attendance, Schedule
from datetime import date


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['mark', 'lecture_date']


class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['day'].empty_label = None

    monday, tuesday, wednesday, thursday, friday, saturday = 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'
    days = ((monday, 'Mon'), (tuesday, 'Tue'), (wednesday, 'Wed'), (thursday, 'Thu'), (friday, 'Fri'), (saturday, 'Sat'))
    day = forms.MultipleChoiceField(choices=days)

    class Meta:
        model = Schedule
        fields = '__all__'

    def clean_day(self):
        day = self.cleaned_data['day']
        day = ','.join(day)
        return day


class CheckAttendanceForm(forms.Form):
    roll_no = forms.IntegerField(min_value=1)
    start_date = forms.DateField()
    end_date = forms.DateField(initial=date.today, widget=forms.DateInput(attrs={'max': date.today}))
