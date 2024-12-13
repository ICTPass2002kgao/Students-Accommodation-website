from django.shortcuts import get_object_or_404, render 
from .models import Accommodation, Accommodation, AccommodationImage,Application,Student
from django.shortcuts import render, redirect 
from .forms import  StudentRegistrationForm, LoginForm   
from django.contrib.auth import   login ,authenticate
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.core.mail import send_mail 
from django.contrib.auth import logout 

from django.db.models import Count, Sum
 

################################## ENDPOINTS FOR WEB APPLICATION ####################################################

@login_required
def logout_user(request):
    logout(request)  
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registered successfully! Now proceed to login')
            return render(request,'response.html',{
                'heading':'Account registered',
                'message':'Your account have been registered successfully, You may proceed to login.'})  
        else:
            messages.error(request, 'Please correct the errors below.') 
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
 
                if user.is_staff:
                    return redirect("dashboard")  
                return redirect("home") 
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.db.models import Count




@login_required
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('login')

    # Handle POST request to create a new accommodation
    if request.method == 'POST': 
        accommodation_name = request.POST.get('accommodation_name')
        address = request.POST.get('address') 
        description = request.POST.get('description')
        price = request.POST.get('price')  
        logo = request.FILES.get('logo')
 
        accommodation = Accommodation.objects.create(
            accommodation_name=accommodation_name,
            address=address, 
            description=description,
            price=price,  
            logo=logo,
        )
 
        # Handle multiple images for the accommodation
        images = request.FILES.getlist('images') 
        for image in images:
            AccommodationImage.objects.create(accommodation=accommodation, image=image)

    # Aggregate statistics
    total_accommodations = Accommodation.objects.count()
    total_views = Accommodation.objects.aggregate(Sum('views'))['views__sum'] or 0
    total_applications = Application.objects.count()

    # Dynamic data for views chart
    views_data = {
        'labels': list(Accommodation.objects.values_list('accommodation_name', flat=True)),
        'values': list(Accommodation.objects.values_list('views', flat=True)),
    }

    # Dynamic data for applications chart
    applications_data = {
        'labels': list(
            Accommodation.objects.annotate(application_count=Count('application'))
            .values_list('accommodation_name', flat=True)
        ),
        'values': list(
            Accommodation.objects.annotate(application_count=Count('application'))
            .values_list('application_count', flat=True)
        ),
    }

    # Pass data to the template
    context = {
        'user': request.user,
        'total_accommodations': total_accommodations,
        'total_views': total_views,
        'total_applications': total_applications,
        'views_data': views_data,
        'applications_data': applications_data,
        'accommodations': Accommodation.objects.all(),
        'applications': Application.objects.all(),
        'pending_requests': 12,  # Replace with dynamic data if necessary
    }

    return render(request, 'dashboard.html', context)

def send_application_email(application): 
    student_email_subject = "Application Submitted Successfully"
    student_email_body = f"""
Dear {application.student.name},

Your application for "{application.accommodation.accommodation_name}" has been submitted successfully.

Thank you,
Accommodation Team
    """
    send_mail(
        student_email_subject,
        student_email_body,
        'studentlivingdelivery@gmail.com',
        [application.student.email],
        fail_silently=False,
    )

    landlord_email_subject = "New Application Received"
    landlord_email_body = f"""
Dear {application.accommodation.accommodation_name},

A new application has been submitted by {application.student.name} for your accommodation.

Please log in to your dashboard to review the application.

Thank you,
Accommodation Team

    """
    send_mail(
        landlord_email_subject,
        landlord_email_body,
        'studentlivingdelivery@gmail.com',
        [application.accommodation.email],
        fail_silently=False,
    )

@login_required
def view_application_details(request, accommodation_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('login')
     
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    applications = Application.objects.filter(accommodation=accommodation)
    
    context = {
        'accommodation': accommodation,
        'applications': applications,
    }
    return render(request, 'ApplicationDetails.html', context)

@login_required
def apply(request, landlord_id): 
    if request.method == "POST":   
        student_id = request.user.id 
        try:    
            student = get_object_or_404(Student, user__id=student_id) 
            accommodation = get_object_or_404(Accommodation, id=landlord_id)
            if Application.objects.filter(student=student, accommodation=accommodation).exists():
                return render(request, 'response.html', {
                    'heading': 'Already Applied',
                    'message': 'You have already applied for this accommodation.'
                })
            application = Application.objects.create(
                student=student,
                accommodation=accommodation,  
                status="pending"   
            ) 
             
            send_application_email(application) 
            return render(request, 'response.html', {
                'heading': 'Application Submitted Successfully',
                'message': 'Your application has been submitted successfully!'
            })

        except Exception as e:    
            return render(request, 'error_page.html', {'error_message': str(e)}) 
 
    return render(request, 'application_form.html', {
        'accommodations': Accommodation.objects.all()   
    })
    

@login_required
def application_feedback(request, accommodation_id):
    if request.method == 'POST': 
        selected_students_ids = request.POST.getlist('students')
        action = request.POST.get('action')
        feedback_message = request.POST.get('feedback_message')

        if not selected_students_ids or not action:
            messages.error(request, "Please select at least one student and an action.")
            return redirect('view_application_details', accommodation_id=accommodation_id)
 
        applications = Application.objects.filter(student__id__in=selected_students_ids, accommodation__id=accommodation_id)
        
        for application in applications: 
            application.status = action
            application.save()
 
            student = application.student
            subject = f"Application from {application.accommodation.accommodation_name}"
            message = f"Dear {student.name } {student.surname},\n\nYour application for accommodation has been {action}.\n\nPlease come to our accommodation to sign your contract and please consider your application as failure should you be unable to  come register within 2 days.\n\n\nFeedback: {feedback_message}"
            send_mail(
                subject,
                message,
                'studentlivingdelivery@gmail.com',  
                [student.email],  
                fail_silently=False,
            )
        
        messages.success(request, "Feedback sent and student statuses updated.")
        return redirect('view_application_details', accommodation_id=accommodation_id)
     
    accommodation = Accommodation.objects.get(id=accommodation_id)
    applications = Application.objects.filter(accommodation=accommodation)
    context = {
        'accommodation': accommodation,
        'applications': applications,
    }

    return render(request, 'ApplicationDetails.html', context)   
def accomodation_detail(request, uuid):
    accomodation = get_object_or_404(Accommodation, id=uuid)
    
    if not request.user.is_staff:
        accomodation.views += 1
        accomodation.save()
         
        
    
    return render(request, 'accomodation_detail.html', {'accommodation': accomodation})

def home(request): 
    accomodations = Accommodation.objects.all()
    return render(request, 'index.html', {'accommodations': accomodations})
 