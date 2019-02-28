from django import forms
from .models import Attendance, Schedule


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)


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
