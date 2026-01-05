from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import StudentForm, ComplaintForm, RoomForm, AdminReplyForm,FeeDefaulterPredictionForm
from .models import Student, Complaint, CustomUser, Room, FeePayment
from django.http import HttpResponse,FileResponse
from datetime import date, timedelta
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
import numpy as np
import joblib
import os
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  
            return redirect('admin_dashboard')  
        else:
            return redirect('student_dashboard')  
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = 'student'
        user.save()
        Student.objects.create(user=user)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')
    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    else:
        return render(request, 'error.html', {'message': 'User role not recognized.'})

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    complaints = Complaint.objects.filter(student=student).order_by('-submitted_at')

    model = joblib.load('fee_defaulter_model.pkl')
    scaler = joblib.load('scaler.pkl')


    features = np.array([[ 
        student.attendance_percent,
        student.internal_score,
        student.parent_income,
        student.cgpa,
        int(student.scholarship)
    ]])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
   
    likely_to_default = student.payment_status != "Paid"

    context = {
        'student': student,
        'room': student.room,
        'complaints': complaints,
        'payment_status': student.payment_status,
        'likely_to_default': likely_to_default,
    }

    return render(request, 'student_dashboard.html', context)


@login_required
def admin_dashboard(request):
    students = Student.objects.select_related('room').all()
    total_students = students.count()
    total_rooms = Room.objects.count()
    total_complaints = Complaint.objects.count()
    rooms = Room.objects.all()  

    return render(request, 'admin_dashboard.html', {
        'students': students,
        'total_students': total_students,
        'total_rooms': total_rooms,
        'total_complaints': total_complaints,
        'rooms': rooms,  
    })
@login_required
def submit_complaint(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = student
            complaint.save()
            return redirect('submit_complaint')  
    
    else:
        form = ComplaintForm()

   
    complaints = Complaint.objects.filter(student=student).order_by('-id')

    return render(request, 'submit_complaint.html', {
        'form': form,
        'complaints': complaints
    })


@login_required
def view_complaints(request):
    user = request.user
    complaints = []
    if user.role == 'admin':
        complaints = Complaint.objects.all()
    else:
        student = get_object_or_404(Student, user=user)
        complaints = Complaint.objects.filter(student=student)
    return render(request, 'view_complaints.html', {'complaints': complaints})



@login_required
def view_profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/view_profile.html', {'student': student})


@login_required
def view_room_info(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/view_room_info.html', {'room': student.room})


@login_required
def view_students(request):
    students = Student.objects.select_related('user', 'room').all()
    return render(request, 'admin_view_students.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif form.is_valid():
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='student'
            )
            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "Student added successfully.")
            return redirect('view_students')
    else:
        form = StudentForm()
    return render(request, 'admin_add_student.html', {'form': form})
@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        username = request.POST.get('username')
        email = request.POST.get('email')

        if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif form.is_valid():
            user.username = username
            user.email = email
            user.save()
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect('view_students')
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
        }
        form = StudentForm(instance=student, initial=initial_data)

    return render(request, 'admin_edit_student.html', {'form': form, 'student': student})
@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.user.delete()  
        student.delete()       
        messages.success(request, 'Student deleted successfully.')
        return redirect('admin_view_students')

    return render(request, 'admin_confirm_delete_student.html', {'student': student})


@login_required
def view_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'admin_room_list.html', {'rooms': rooms})

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_rooms')
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})

@login_required
def assign_room(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        room_id = request.POST.get('room')
        room = get_object_or_404(Room, id=room_id)

        student.room = room
        student.save()

        messages.success(request, f"Assigned {room.room_number} to {student.user.username}")
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('view_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'edit_room.html', {'form': form})
@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('view_rooms')
    return render(request, 'confirm_delete_room.html', {'room': room})

@login_required
def edit_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id, student=request.user.student)

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  
    else:
        form = ComplaintForm(instance=complaint)

    return render(request, 'edit_complaint.html', {'form': form, 'complaint': complaint})
@login_required
def delete_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id, student__user=request.user)

    if complaint.status != 'pending':
        messages.error(request, "You can only delete complaints that are still pending.")
        return redirect('view_complaints')

    if request.method == 'POST':
        complaint.delete()
        messages.success(request, "Complaint deleted successfully.")
        return redirect('view_complaints')

    return render(request, 'confirm_delete.html', {'complaint': complaint})
@staff_member_required
def admin_complaint_list(request):
    complaints = Complaint.objects.all().order_by('-submitted_at')
    return render(request, 'admin_complaint_list.html', {'complaints': complaints})

@staff_member_required
def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in progress', 'resolved']:
            complaint.status = new_status
            complaint.save()
            messages.success(request, "Complaint status updated.")
        else:
            messages.error(request, "Invalid status.")
        return redirect('admin_complaint_list')
    return render(request, 'admin/update_complaint_status.html', {'complaint': complaint})

@login_required
def admin_reply_view(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        form = AdminReplyForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('view_complaints')  
    else:
        form = AdminReplyForm(instance=complaint)
    return render(request, 'admin_reply.html', {'form': form, 'complaint': complaint})

def predict_fee_defaulter(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        attendance = float(request.POST.get('attendance_percent'))
        internal = float(request.POST.get('internal_score'))
        income = float(request.POST.get('parent_income'))
        cgpa = float(request.POST.get('cgpa'))
        scholarship = int(request.POST.get('scholarship'))

        features = np.array([[attendance, internal, income, cgpa, scholarship]])

        model = joblib.load('fee_defaulter_model.pkl')
        scaler = joblib.load('scaler.pkl')
        scaled_features = scaler.transform(features)

        prediction = model.predict(scaled_features)[0]
        result = "✅ Likely to PAY Fees" if prediction == 1 else "❌ Likely to DEFAULT"

        return render(request, 'predict_result.html', {
            'student': student,
            'result': result
        })

    return render(request, 'predict_fee_defaulter.html', {'student': student})

@login_required
def auto_assign_rooms(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('admin_dashboard')

    unassigned_students = Student.objects.filter(room__isnull=True)
    rooms = Room.objects.all()

    assigned_count = 0
    for student in unassigned_students:
        for room in rooms:
            if not room.is_full(): 
                student.room = room
                student.save()
                assigned_count += 1
                break  
    if assigned_count == 0:
        messages.warning(request, "No available rooms found.")
    else:
        messages.success(request, f"{assigned_count} students auto-assigned to rooms.")

    return redirect('admin_dashboard')


def is_student(user):
    return hasattr(user, 'student')

def is_admin(user):
    return user.is_superuser or user.is_staff



@login_required
@user_passes_test(is_student)
def student_fee_status(request):
    student = request.user.student
    fee_payment, created = FeePayment.objects.get_or_create(student=student)

    context = {
        'fee_paid': fee_payment.fee_paid,
        'receipt': fee_payment.receipt.url if fee_payment.receipt else None,
    }
    return render(request, 'student/fee_status.html', context)


@login_required
def pay_fee(request):
    student = request.user.student

    if request.method == 'POST':
        receipt_file = request.FILES.get('receipt')  

        fee_payment, created = FeePayment.objects.get_or_create(student=student)
        fee_payment.fee_paid = True
        if receipt_file:
            fee_payment.receipt = receipt_file
        fee_payment.save()

        messages.success(request, 'Fee payment recorded successfully!')
        return redirect('fee_status')

    return render(request, 'pay_fee.html')


@login_required
@user_passes_test(is_student)
def download_receipt(request):
    student = Student.objects.get(user=request.user)
    
    if not student.has_paid_fees:
        return HttpResponse("You have not paid fees.", status=403)

    template = get_template("receipt_template.html")
    context = {
        "student": student,
        "room": student.room,
    }

    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="receipt_{request.user.username}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    
    return response



@login_required
@user_passes_test(is_admin)
def admin_view_all_fees(request):
    students = Student.objects.all()
    fee_data = []
    for student in students:
        fee_payment, created = FeePayment.objects.get_or_create(student=student)
        fee_data.append({
            'student': student,
            'fee_paid': fee_payment.fee_paid,
            'receipt': fee_payment.receipt.url if fee_payment.receipt else None,
        })

    context = {'fee_data': fee_data}
    return render(request, 'admin/view_all_fees.html', context)

@login_required
def admin_view_fees(request):
    students = Student.objects.select_related('user').all()

    return render(request, 'admin_view_fees.html', {'students': students})

@login_required
def mock_pay(request):
    student = get_object_or_404(Student, user=request.user)
    student.payment_status = "Paid"
    student.has_paid_fees = True  
    student.save()
    return redirect('student_dashboard')  

def predict_fee_defaulter_list(request):
    students = Student.objects.all()
    return render(request, 'predict_fee_list.html', {'students': students})