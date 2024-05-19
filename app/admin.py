from django.contrib import admin
from .models import  Assignment, AssignmentSubmission, Exam, ExamSubmission, Quiz, QuizSubmission, Room,Book,SavedDocument

# Register the Room model
admin.site.register(Room)
admin.site.register(Book)
admin.site.register(SavedDocument)
admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Exam)
admin.site.register(QuizSubmission)
admin.site.register(AssignmentSubmission)
admin.site.register(ExamSubmission)
