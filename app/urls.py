from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app import views

app_name = 'app'  # Add this line to specify the app namespace


urlpatterns = [
    path("",views.home, name='home'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('joined-rooms/',views.joined_rooms,name='joined_rooms'),
    path('leave-room/<int:room_id>/', views.leave_room, name='leave_room'),
    path('created-rooms/', views.created_rooms, name='created_rooms'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),

    path('room/<int:room_id>/quizzes', views.room_quizzes, name='room_quizzes'),
    path('room/<int:room_id>/assignments/', views.room_assignments, name='room_assignments'),
    path('room/<int:room_id>/exams/', views.room_exams, name='room_exams'),

    path('quiz/<int:quiz_id>/submit/', views.room_quizzes, name='submit_quiz'),
    path('assignment/<int:assignment_id>/submit/', views.room_assignments, name='submit_assignment'),
    path('exam/<int:exam_id>/submit/', views.room_exams, name='submit_exam'),
    
    path('submissions/quizzes/<int:quiz_id>/', views.submitted_quizzes, name='submitted_quizzes'),
    path('submissions/assignments/<int:assignment_id>/', views.submitted_assignments, name='submitted_assignments'),
    path('submissions/exams/<int:exam_id>/', views.submitted_exams, name='submitted_exams'),


    path('update_submission_marks/<int:quiz_id>/', views.update_quiz_submission_marks, name='update_quiz_submission_marks'),
    path('update_assignment_submission_marks/<int:assignment_id>/', views.update_assignment_submission_marks, name='update_assignment_submission_marks'),
    path('update_exam_submission_marks/<int:exam_id>/', views.update_exam_submission_marks, name='update_exam_submission_marks'),
    
    path('check-submission/', views.check_submission, name='check_submission'),

    path('kick_participant/<int:room_id>/<int:user_id>/', views.kick_participant, name='kick_participant'),
    path('room/<int:room_id>/participants/', views.load_participants, name='load_participants'),


    path('student-analytics/', views.student_analytics, name='student_analytics'),
    path('teacher-analytics/', views.teacher_analytics, name='teacher_analytics'),

    path('room_detail/<int:room_id>/', views.room_detail, name='room_detail'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('room/<int:room_id>/join-requests/', views.join_requests, name='join_requests'),
    path('accept-join-request/<int:room_id>/<int:user_id>/', views.accept_join_request, name='accept_join_request'),
    path('reject-join-request/<int:room_id>/<int:user_id>/', views.reject_join_request, name='reject_join_request'),
    path('upload-book/', views.upload_book, name='upload_book'),
    path('book-list/', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('query-form/', views.process_query1, name='query_form'),
    path('save-pdf/', views.save_pdf, name='save_pdf'),
    path('created_docs/', views.created_docs, name='created_docs'),
    path('delete_document/<int:doc_id>/', views.delete_document, name='delete_document'),

    path('help/',views.help, name='help'),


]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
