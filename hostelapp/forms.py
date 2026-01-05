from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Complaint, Room


# 🔹 Registration Form (for student sign-up)
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user


# 🔹 Room Form (Admin use)
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'max_capacity']  # ✅ make sure it's 'max_capacity'



# 🔹 Student Details Form (Admin use)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['contact_number', 'address', 'room']


    def clean_contact_number(self):
        number = self.cleaned_data['contact_number']

        if not number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")

        if len(number) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")

        if number[0] not in ['6', '7', '8', '9']:
            raise forms.ValidationError("Contact number must start with 6, 7, 8, or 9.")

        return number
# 🔹 Complaint Form (Student files complaint)
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description']


# 🔹 Admin Reply to Complaints
class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['admin_reply', 'status']
        widgets = {
            'admin_reply': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class FeeDefaulterPredictionForm(forms.Form):
    YEAR_CHOICES = [(2022, '2022'), (2023, '2023'), (2024, '2024')]
    DEPT_CHOICES = [('CSE', 'CSE'), ('ECE', 'ECE'), ('ME', 'ME')]

    year = forms.ChoiceField(choices=YEAR_CHOICES)
    department = forms.ChoiceField(choices=DEPT_CHOICES)
    attendance_percent = forms.IntegerField(label="Attendance %", min_value=0, max_value=100)
    internal_score = forms.IntegerField(label="Internal Score", min_value=0, max_value=100)
    parent_income = forms.IntegerField(label="Parent Income (₹)", min_value=1000)
    scholarship = forms.BooleanField(required=False)
    hostel_stay = forms.BooleanField(required=False)