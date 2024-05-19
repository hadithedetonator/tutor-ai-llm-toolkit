from django.shortcuts import  render, redirect,get_object_or_404
from django.http import JsonResponse,HttpRequest
from django.contrib.auth.decorators import login_required
from .forms import RoomCreationForm,JoinRoomForm,BookUploadForm,QuizForm,AssignmentForm,ExamForm
from .models import CustomUser,Book
from langchain_community.llms import Ollama
import random

#from langchain_community.vectorstores import FAISS
#from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
#from langchain_community.embeddings import HuggingFaceEmbeddings


from .models import Room,QuizSubmission

#----------------APP LEVEL FUNCTIONS------------nov.23------#

@login_required
def home(request):
    return render(request, 'app/home.html')
    
def joined_rooms(request):
    user = request.user
    joined_rooms = Room.objects.filter(participants=user)
    return render(request, 'app/joined_rooms.html', {'joined_rooms': joined_rooms})

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user

            # Generate a random 6-digit pass key
            pass_key = str(random.randint(100000, 999999))
            room.pass_key = pass_key

            room.save()
            return redirect('app:home')
    else:
        form = RoomCreationForm()

    return render(request, 'app/create_room.html', {'form': form})

@login_required
def created_rooms(request):
    if request.user.is_teacher:
    # Fetch all rooms created by the teacher
        created_rooms = Room.objects.filter(creator=request.user)
        return render(request, 'app/created_rooms.html', {'created_rooms': created_rooms})
    else:
        return redirect('app:home')  # Change to the appropriate URL
    

from django.shortcuts import render, redirect
from .forms import QuizForm, AssignmentForm, ExamForm, QuizSubmissionForm, AssignmentSubmissionForm, ExamSubmissionForm
from .models import Quiz, Assignment, Exam, ExamSubmission,AssignmentSubmission
from django.core.files.uploadedfile import InMemoryUploadedFile


def room_assignments(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    assignments = room.assignments.all()
    user = request.user
    
    if user.is_teacher:
        form = AssignmentForm(user=request.user)
    else:
        form = AssignmentSubmissionForm()

    # Get all submissions for the current user
    user_submissions = AssignmentSubmission.objects.filter(student=user)

    # Dictionary to store assignment IDs for which the user has already submitted
    submitted_assignment_ids = set(submission.assignment.id for submission in user_submissions)

    if request.method == 'POST':
        if user.is_teacher:
            form = AssignmentForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.room = room
                submission.save()
            else:
                print(form.errors)
        else:
            form = AssignmentSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.student = request.user
                assignment_id = request.POST.get('assignment_id')
                submission.assignment = Assignment.objects.get(id=assignment_id)

                # Get the first uploaded file
                submitted_file = request.FILES.get('submission')
                document = request.POST.get('document')
                if isinstance(submitted_file, InMemoryUploadedFile):
                    # Call the function with the file's file pointer
                    ai_report = check_submission(submitted_file.file,document)
                    submission.save()
                    # Process the AI report and set the fields accordingly
                    ai_marks = detect_percentage(ai_report)
                    submission.ai_report = ai_report
                    total_marks = submission.assignment.total_marks
                    submission.ai_marks = ai_marks / 100 * total_marks
                    submission.save()

                    return redirect(request.META.get('HTTP_REFERER', '/'))

                else:
                    print("Invalid file type")

            else:
                print("AssignmentSubmissionForm errors:", form.errors)
                
        return redirect(request.META.get('HTTP_REFERER', '/'))


    return render(request, 'app/room/assignments.html', {
        'room': room,
        'assignments': assignments,
        'user': user,
        'form': form,
        'submitted_assignment_ids': submitted_assignment_ids,
    })


def room_exams(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    exams = room.exams.all()
    user = request.user
    
    if user.is_teacher:
        form = ExamForm(user=request.user)
    else:
        form = ExamSubmissionForm()

     # Get all submissions for the current user
    user_submissions = ExamSubmission.objects.filter(student=user)

    # Dictionary to store quiz IDs for which the user has already submitted
    submitted_exam_ids = set(submission.exam.id for submission in user_submissions)

    if request.method == 'POST':
        if user.is_teacher:
            form = ExamForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.room = room
                submission.save()
            else:
                print(form.errors)
        else:
            form = ExamSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.student = request.user
                exam_id = request.POST.get('exam_id')
                submission.exam = Exam.objects.get(id=exam_id)

                # Get the first uploaded file
                submitted_file = request.FILES.get('submission')
                document = request.POST.get('document')
                if isinstance(submitted_file, InMemoryUploadedFile):
                    # Call the function with the file's file pointer
                    ai_report = check_submission(submitted_file.file,document)
                    submission.save()
                    # Process the AI report and set the fields accordingly
                    ai_marks = detect_percentage(ai_report)
                    submission.ai_report = ai_report
                    total_marks = submission.exam.total_marks
                    submission.ai_marks = ai_marks / 100 * total_marks
                    submission.save()

                    return redirect(request.META.get('HTTP_REFERER', '/'))

                else:
                    print("Invalid file type")

            else:
                print("ExamSubmission errors:", form.errors)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'app/room/exams.html', {
        'room': room,
        'exams': exams,
        'user': user,
        'form': form,
        'submitted_exam_ids': submitted_exam_ids,
    })


           

from .utils import detect_percentage

def room_quizzes(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    quizzes = room.quizzes.all()
    user = request.user

    if user.is_teacher:
        form = QuizForm(user=request.user)  # Pass the logged-in user to the form
    else:
        form = QuizSubmissionForm()

    # Get all submissions for the current user
    user_submissions = QuizSubmission.objects.filter(student=user)

    # Dictionary to store quiz IDs for which the user has already submitted
    submitted_quiz_ids = set(submission.quiz.id for submission in user_submissions)

    if request.method == 'POST':
        if user.is_teacher:
            form = QuizForm(request.POST, request.FILES, user=request.user)  
            if form.is_valid():
                submission = form.save(commit=False)
                submission.room = room
                submission.save()
            else:
                print(form.errors)
        else:
            form = QuizSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.student = request.user
                quiz_id = request.POST.get('quiz_id')
                submission.quiz = Quiz.objects.get(id=quiz_id)

                # Get the first uploaded file
                submitted_file = request.FILES.get('submission')
                document = request.POST.get('document')
                if isinstance(submitted_file, InMemoryUploadedFile):
                    # Call the function with the file's file pointer
                    ai_report = check_submission(submitted_file.file,document)
                    submission.save()
                    # Process the AI report and set the fields accordingly
                    ai_marks = detect_percentage(ai_report)
                    submission.ai_report = ai_report
                    total_marks = submission.quiz.total_marks
                    submission.ai_marks = ai_marks / 100 * total_marks
                    submission.save()

                    return redirect(request.META.get('HTTP_REFERER', '/'))

                else:
                    print("Invalid file type")

            else:
                print("QuizSubmissionForm errors:", form.errors)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'app/room/quizzes.html', {
        'room': room,
        'quizzes': quizzes,
        'user': user,
        'form': form,
        'submitted_quiz_ids': submitted_quiz_ids,
    })




def submitted_quizzes(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # For students, filter submissions based on the current user and the quiz
    if not request.user.is_teacher:
        submissions = QuizSubmission.objects.filter(quiz=quiz, student=user)
    else:
        submissions = QuizSubmission.objects.filter(quiz=quiz)

    return render(request, 'app/room/quiz_submissions.html', {'quiz': quiz, 'submissions': submissions})


def submitted_assignments(request, assignment_id):
    # Retrieve the quiz object
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Retrieve all submissions for the specified quiz
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)

    return render(request, 'app/room/assignment_submissions.html', {'assignment': assignment, 'submissions': submissions})

def submitted_exams(request, exam_id):
    # Retrieve the quiz object
    exam = get_object_or_404(Exam, id=exam_id)

    # Retrieve all submissions for the specified quiz
    submissions = ExamSubmission.objects.filter(exam=exam)

    return render(request, 'app/room/exam_submissions.html', {'exam': exam, 'submissions': submissions})



@login_required
def join_room(request):
    if request.method == 'POST' and not request.user.is_teacher:
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            pass_key = form.cleaned_data['pass_key']

            try:
                room = Room.objects.get(name=room_name, pass_key=pass_key)
                
                # Check if the user is already a participant or waiting for approval
                if room.is_participant(request.user):
                    return JsonResponse({'success': False, 'message': 'You are already a participant.'})
                elif room.has_join_request(request.user):
                    return JsonResponse({'success': False, 'message': 'Waiting for approval from the owner.'})
                
                # Add the user to the participants of the room
                room.join_requests.add(request.user)
                return JsonResponse({'success': True, 'message': 'Sent Join Request. Wait for approval.'})
            except Room.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Room Doesnt Exist. Double Check credentials.'})
    else:
        form = JoinRoomForm()

    return render(request, 'app/join_room.html', {'form': form})

@login_required
def leave_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Check if the user is a participant in the room
    if room.is_participant(request.user):
        # Remove the user from the participants of the room
        room.participants.remove(request.user)

    # Redirect to the home page or another appropriate URL
    return redirect('app:home')

@login_required
def join_requests(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Fetch join requests for the room
    join_requests = room.join_requests.all()

    return render(request, 'app/join_req.html', {'room': room, 'join_requests': join_requests})

@login_required
def accept_join_request(request, room_id, user_id):
    # Get the room and user
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(CustomUser, id=user_id)

    # Add the user to the participants and remove from join requests
    room.participants.add(user)
    room.join_requests.remove(user)

    return redirect('app:room_detail', room_id=room.id)

@login_required
def reject_join_request(request, room_id, user_id):
    # Get the room and user
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(CustomUser, id=user_id)

    # Remove the user from join requests
    room.join_requests.remove(user)

    return JsonResponse({'success': True, 'message': 'Join request rejected successfully.'})


@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Check if the user is the creator of the room
    if request.user == room.creator:
        # If the user is the creator, delete the room
        room.delete()
        return redirect('app:created_rooms')  # Redirect to dashboard or any other page after deletion
    
    # If the user is a participant but not the creator
    if request.user.is_authenticated and not request.user.is_teacher:

        room.participants.remove(request.user)

        room.save()
        # Redirect to a page indicating that the user is no longer a participant
        return redirect('app:joined_rooms')  # Change to the appropriate URL

    # Handle other cases, for example, the user is neither the creator nor a participant
    return redirect('app:home')  # Redirect to the home page or handle the case accordingly


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    return render(request, 'app/room_detail1.html', {'room': room})


@login_required
def kick_participant(request, room_id, user_id):
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(room.participants, id=user_id)
    
    # Remove the participant from the room
    room.participants.remove(participant)
    
    return JsonResponse({'success': True, 'message': 'Participant kicked successfully'})

def load_participants(request, room_id):
    # Retrieve the quiz object
    room = get_object_or_404(Room, id=room_id)

    # Retrieve all participants for the specified room
    participants = room.participants.all()

    return render(request, 'app/room/room_participants.html', {'room': room, 'participants': participants})


@login_required
def created_docs(request):
    user = request.user
    documents = SavedDocument.objects.filter(teacher=user)
    return render(request, 'app/created_docs.html', {'documents': documents})
from django.conf import settings

@login_required
def delete_document(request, doc_id):
    # Get the document object
    document = get_object_or_404(SavedDocument, pk=doc_id)

    # Delete the document from the file system
    document_path = os.path.join(settings.MEDIA_ROOT, str(document.document))
    if os.path.exists(document_path):
        os.remove(document_path)

    # Delete the document from the database
    document.delete()

    # Redirect to the created_docs page
    return redirect('app:created_docs')



@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            return redirect('app:book_list')  # Change to the appropriate URL
    else:
        form = BookUploadForm()

    return render(request, 'app/upload_book.html', {'form': form})

@login_required
def book_list(request):
    uploaded_books = Book.objects.filter(uploaded_by_id=request.user)
    return render(request, 'app/book_list.html', {'uploaded_books': uploaded_books})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.upload.delete()
        book.delete()
        return redirect('app:book_list')  # Redirect 
    

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'app/book_detail.html', {'book': book})

from .utils import set_qa_prompt,set_qa_prompt2

@login_required
def process_query1(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        text = request.POST.get('text')  # Get the text content
        
        llm = Ollama(base_url="http://localhost:11434", model='gemma:2b')
        prompt = set_qa_prompt()
        formatted_prompt = prompt.format(question=query,context=text)
        response_data = llm.invoke(formatted_prompt)
        
        return JsonResponse(response_data, safe=False)  # Return the response data as JSON

    return JsonResponse({'error': 'Method not allowed'}, status=405)

from io import BytesIO
from django.http import JsonResponse
import os
import re
from io import BytesIO
from google.cloud import vision
from pdf2image import convert_from_path  # Import convert_from_path
from django.http import JsonResponse


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/munib_ahmed1988/fyp/app/vision-key.json'
WORD = re.compile(r"\w+")


def detect_text(image_content):
    """Detects text in the image using Google Vision API."""
    try:
        try:
            print("before client")
            client = vision.ImageAnnotatorClient()
            print('Connected to Google Vision API')  # Debugging print statement
        except Exception as e:
                print(f"Error connecting to Google Vision API: {e}")
                raise Exception("Failed to connect to Google Vision API")

        image = vision.Image(content=image_content)
        print('Connected to image')  # Debugging print statement
        try:
            response = client.document_text_detection(image=image)
        
        except Exception as e:
            print(e)

        texts = response.text_annotations
        ocr_text = []
        for text in texts:
            ocr_text.append(text.description)
        return ocr_text
    
    except Exception as e:
        raise Exception(f"Error in detecting text: {e}")



import os
import requests
from pdf2image import convert_from_bytes
from io import BytesIO
from tempfile import NamedTemporaryFile

def convert_pdf_to_images(pdf_url):
    """Converts PDF pages to images."""
    images = []
    pages = convert_from_bytes(pdf_url)
    for page_num, page in enumerate(pages, start=1):
        with BytesIO() as output:
            page.save(output, format='JPEG')
            image_data = output.getvalue()
            images.append(image_data)
       
    return images

import PyPDF2
def extract_text_from_document(document):
    try:
        # Open the PDF file
        with open(document, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Initialize an empty string to store extracted text
            text = ""

            # Iterate through each page of the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the page object
                page = pdf_reader.pages[page_num]

                # Extract text from the page and append it to the text string
                text += page.extract_text()

            return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def check_submission(submission,document):
    try:
         # Extract text from the document
        document_text = extract_text_from_document(document)

        print("ye nikla h:"+ document_text)

        # Convert BytesIO object to raw bytes
        pdf_bytes = submission.getvalue()
        
        # Convert PDF to images
        pdf_images = convert_pdf_to_images(pdf_bytes)

        # Extract text from each image
        extracted_text = []
        for image_data in pdf_images:
            extracted_text.extend(detect_text(image_data))

        extracted_text = ' '.join(extracted_text)

        # Initialize Ollama with appropriate parameters
        llm = Ollama(base_url="http://localhost:11434", model='gemma:7b')
        
        # Set the prompt for language model
        prompt = set_qa_prompt2()
        formatted_prompt = prompt.format(test=document_text,submission=extracted_text)
        
        # Invoke the language model
        response_data = llm.invoke(formatted_prompt)
        
        return response_data
    
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

        
def update_quiz_submission_marks(request, quiz_id):
    if request.method == 'POST':
        # Retrieve all submitted marks from the form
        marks_dict = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('marks_')}
        
        # Update marks for each submission
        for submission_id, marks in marks_dict.items():
            submission = get_object_or_404(QuizSubmission, id=submission_id)
            submission.marks = marks
            submission.save()
        
        # Redirect back to the quiz submissions page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Redirect to some error page if accessed via GET method
    return redirect('app:home')  

def update_assignment_submission_marks(request, assignment_id):
    if request.method == 'POST':
        # Retrieve all submitted marks from the form
        marks_dict = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('marks_')}
        
        # Update marks for each submission
        for submission_id, marks in marks_dict.items():
            submission = get_object_or_404(AssignmentSubmission, id=submission_id)
            submission.marks = marks
            submission.save()
        
        # Redirect back to the assignment submissions page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Redirect to some error page if accessed via GET method
    return redirect('app:home')

def update_exam_submission_marks(request, exam_id):
    if request.method == 'POST':
        # Retrieve all submitted marks from the form
        marks_dict = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('marks_')}
        
        # Update marks for each submission
        for submission_id, marks in marks_dict.items():
            submission = get_object_or_404(ExamSubmission, id=submission_id)
            submission.marks = marks
            submission.save()
        
        # Redirect back to the exam submissions page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Redirect to some error page if accessed via GET method
    return redirect('app:home')



from reportlab.pdfgen import canvas
from io import BytesIO
from .models import SavedDocument
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import re  # Import the regular expression module

@csrf_exempt
def save_pdf(request):
    if request.method == 'POST':
        # Get title from the form
        title = request.POST.get('title', '').strip()  # Strip whitespace from the title
        d_type = request.POST.get('d_type')  # Get d_type from POST data

        if not title:
            return HttpResponseBadRequest("Title is required.")  # Return a 400 Bad Request if title is empty
        
        response_content = request.POST.get('response_content', '')  # Get response content from POST data
        
        # Create a BytesIO object to hold the PDF content
        buffer = BytesIO()

        # Create a PDF object
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Add content to PDF
        story = []

        # Add title
        title_text = f"<b>{title}</b>"
        story.append(Paragraph(title_text, styles['Title']))

        # Parse response content and add to PDF
        bold_pattern = re.compile(r'\*\*(.*?)\*\*')  # Regular expression to match text inside double asterisks
        for line in response_content.split('\n'):
            if line.strip():  # Only add non-empty lines
                # Check for bold text inside double asterisks and replace with <b> tags
                line = bold_pattern.sub(r'<b>\1</b>', line)
                story.append(Paragraph(line.strip(), styles['Normal']))
            else:
                story.append(Spacer(1, 12))  # Add some space between paragraphs

        # Add footer
        footer_text = "<font size='8'>Made by Tutor-Ai</font>"
        story.append(Paragraph(footer_text, styles['Normal']))

        pdf.build(story)

        try:
            # Save the PDF file to the saved_docs directory
            saved_document = SavedDocument.objects.create(title=title, teacher=request.user, d_type=d_type)
            saved_document.document.save(f'{title}.pdf', buffer)
        except Exception as e:
            # Handle any exceptions that might occur during saving
            return HttpResponseBadRequest(f"Failed to save PDF: {str(e)}")
        finally:
            # Close the BytesIO buffer
            buffer.close()

        return HttpResponse("PDF file saved successfully.")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed for this endpoint.")

    
def student_analytics(request):
    # Retrieve quiz submission data
    quiz_submissions = QuizSubmission.objects.filter(student=request.user)
    quiz_marks = [submission.marks for submission in quiz_submissions if submission.marks is not None]
    quiz_stats = {
        'avg_marks': sum(quiz_marks) / len(quiz_marks) if quiz_marks else 0,
        'max_marks': max(quiz_marks) if quiz_marks else 0,
        'min_marks': min(quiz_marks) if quiz_marks else 0,
    }

    # Retrieve assignment submission data
    assignment_submissions = AssignmentSubmission.objects.filter(student=request.user)
    assignment_marks = [submission.marks for submission in assignment_submissions if submission.marks is not None]
    assignment_stats = {
        'avg_marks': sum(assignment_marks) / len(assignment_marks) if assignment_marks else 0,
        'max_marks': max(assignment_marks) if assignment_marks else 0,
        'min_marks': min(assignment_marks) if assignment_marks else 0,
    }

    # Retrieve exam submission data
    exam_submissions = ExamSubmission.objects.filter(student=request.user)
    exam_marks = [submission.marks for submission in exam_submissions if submission.marks is not None]
    exam_stats = {
        'avg_marks': sum(exam_marks) / len(exam_marks) if exam_marks else 0,
        'max_marks': max(exam_marks) if exam_marks else 0,
        'min_marks': min(exam_marks) if exam_marks else 0,
    }

    return render(request, 'app/student_analytics.html', {
        'quiz_stats': quiz_stats,
        'assignment_stats': assignment_stats,
        'exam_stats': exam_stats
    })
from django.db.models import Avg,Max  # Add this line

def teacher_analytics(request):
    rooms = Room.objects.filter(creator=request.user)
    room_stats = []
    for room in rooms:
        # Calculate average marks for each submission type
        quiz_avg_marks = QuizSubmission.objects.filter(quiz__room=room).aggregate(avg_marks=Avg('marks'))['avg_marks'] or 0
        assignment_avg_marks = AssignmentSubmission.objects.filter(assignment__room=room).aggregate(avg_marks=Avg('marks'))['avg_marks'] or 0
        exam_avg_marks = ExamSubmission.objects.filter(exam__room=room).aggregate(avg_marks=Avg('marks'))['avg_marks'] or 0

        # Find the user with the highest marks for each submission type
        top_quiz_scorer = QuizSubmission.objects.filter(quiz__room=room).order_by('-marks').first()
        top_assignment_scorer = AssignmentSubmission.objects.filter(assignment__room=room).order_by('-marks').first()
        top_exam_scorer = ExamSubmission.objects.filter(exam__room=room).order_by('-marks').first()

        # Get the user objects for the top scorers
        top_quiz_scorer_user = top_quiz_scorer.student if top_quiz_scorer else None
        top_assignment_scorer_user = top_assignment_scorer.student if top_assignment_scorer else None
        top_exam_scorer_user = top_exam_scorer.student if top_exam_scorer else None

        room_stats.append({
            'room': room,
            'quiz_avg_marks': quiz_avg_marks,
            'assignment_avg_marks': assignment_avg_marks,
            'exam_avg_marks': exam_avg_marks,
            'top_quiz_scorer_user': top_quiz_scorer_user,
            'top_assignment_scorer_user': top_assignment_scorer_user,
            'top_exam_scorer_user': top_exam_scorer_user,
        })

    return render(request, 'app/teacher_analytics.html', {'room_stats': room_stats})
def help(request):
    return render(request, 'app/help.html')
