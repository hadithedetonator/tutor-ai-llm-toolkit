from django import forms
from .models import Room , Book 


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        labels = {
            'name': 'Room Name',
        }

class JoinRoomForm(forms.Form):
    room_name = forms.CharField(max_length=100, label='Room Name')
    pass_key = forms.CharField(max_length=100, label='Pass Key')


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'upload']


from .models import Quiz, Assignment, Exam, QuizSubmission, AssignmentSubmission, ExamSubmission,SavedDocument



from django.core.exceptions import ValidationError
import re

class QuizForm(forms.ModelForm):
    end_time = forms.CharField(label='End Time', required=True)

    class Meta:
        model = Quiz
        fields = ['title', 'file', 'total_marks', 'end_time']
    
    def __init__(self, *args, user=None, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['file'].queryset = SavedDocument.objects.filter(teacher=user,d_type='quiz')

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']

        # Regular expression pattern to match the desired time format '11:00 AM'
        time_pattern = re.compile(r'^\d{1,2}:\d{2} (AM|PM)$')

        # Validate the format
        if not time_pattern.match(end_time):
            raise ValidationError("Invalid time format. Please enter time in 'HH:MM AM/PM' format.")

        return end_time
    
class AssignmentForm(forms.ModelForm):
    end_time = forms.CharField(label='End Time', required=True)
    class Meta:
        model = Assignment
        fields = ['title', 'file', 'total_marks', 'end_time']

    def __init__(self, *args, user=None, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['file'].queryset = SavedDocument.objects.filter(teacher=user,d_type='assignment')


    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']

        # Regular expression pattern to match the desired time format '11:00 AM'
        time_pattern = re.compile(r'^\d{1,2}:\d{2} (AM|PM)$')

        # Validate the format
        if not time_pattern.match(end_time):
            raise ValidationError("Invalid time format. Please enter time in 'HH:MM AM/PM' format.")

        return end_time
    
class ExamForm(forms.ModelForm):
    end_time = forms.CharField(label='End Time', required=True)

    class Meta:
        model = Exam
        fields = ['title', 'file', 'total_marks', 'end_time']

    def __init__(self, *args, user=None, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['file'].queryset = SavedDocument.objects.filter(teacher=user,d_type='exam')

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']

        # Regular expression pattern to match the desired time format '11:00 AM'
        time_pattern = re.compile(r'^\d{1,2}:\d{2} (AM|PM)$')

        # Validate the format
        if not time_pattern.match(end_time):
            raise ValidationError("Invalid time format. Please enter time in 'HH:MM AM/PM' format.")

        return end_time
    

class QuizSubmissionForm(forms.ModelForm):
    class Meta:
        model = QuizSubmission
        fields = ['submission']

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submission']

class ExamSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExamSubmission
        fields = ['submission']