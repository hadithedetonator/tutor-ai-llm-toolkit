from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=255)
    pass_key = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser, related_name='joined_rooms', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    join_requests = models.ManyToManyField(CustomUser, related_name='pending_requests', blank=True)

    def has_join_request(self, user):
        return user in self.join_requests.all()

    def is_participant(self, user):
        return user in self.participants.all()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='books/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SavedDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
    ]
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.FileField(upload_to='saved_docs')
    d_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Quiz(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='quizzes')
    file = models.ForeignKey(SavedDocument, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_marks = models.FloatField()
    end_time = models.CharField(max_length=20)  # Change to CharField

    def __str__(self):
        return self.title

class Assignment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assignments')
    file = models.ForeignKey(SavedDocument, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)
    total_marks = models.FloatField()
    end_time = models.CharField(max_length=20)  # Change to CharField

    def __str__(self):
        return self.title
    
class Exam(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='exams')
    file = models.ForeignKey(SavedDocument, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)
    total_marks = models.FloatField()
    end_time = models.CharField(max_length=20)  # Change to CharField

    def __str__(self):
        return self.title
   
class QuizSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='submissions')
    submission = models.FileField(upload_to='quiz_submissions/')
    marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_report = models.TextField(null=True, blank=True)  # New field for AI report
    ai_marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks
    
    def __str__(self):
        return self.student.first_name
    
class AssignmentSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='submissions')
    submission = models.FileField(upload_to='assignment_submissions/')
    marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_report = models.TextField(null=True, blank=True)  # New field for AI report
    ai_marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks
    
    def __str__(self):
        return self.student.first_name


class ExamSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name='submissions')
    submission = models.FileField(upload_to='exam_submissions/')
    marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_report = models.TextField(null=True, blank=True)  # New field for AI report
    ai_marks = models.FloatField(null=True, blank=True)  # Nullable field to store marks

    def __str__(self):
        return self.student.first_name
