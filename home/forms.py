from django import forms  
from django.contrib.auth.models import User
from .models import Student 
import uuid

from django.core.exceptions import ValidationError 

# class AccommodationForm(forms.ModelForm):
#     images = forms.FileField(
#         widget=forms.FileInput(attrs={'multiple': True}), 
#         required=False
#     )

#     class Meta:
#         model = Accommodation
#         fields = [
#             'accommodation_name', 
#             'address', 
#             'email', 
#             'description', 
#             'price', 
#             'offered_amenities', 
#             'accommodated_universities', 
#             'logo', 
#             'images'
#         ]

        
           
class StudentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.EmailField()
    cell_phone = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    enrolled_university = forms.CharField(max_length=50)
    bursary = forms.CharField(max_length=50, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self):
        data = self.cleaned_data

        # Create User object
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # Create Student object linked to the user
        student = Student.objects.create(
            user=user,
            id=uuid.uuid4(),
            name=data['name'],
            surname=data['surname'],
            email=data['email'],
            cell_phone=data['cell_phone'],
            gender=data['gender'],
            enrolled_university=data['enrolled_university'],
            bursary=data['bursary']
        )
        return student

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

 