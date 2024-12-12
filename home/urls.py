from django.urls import path ,include 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
urlpatterns = [ 
    path('auth/register/', views.register, name='register'), 
    path('auth/login/', views.user_login, name='login'),   
    path('logout/', views.logout_user, name='logout'),
    path('',views.home,name="home"),  
    path('dashboard/',views.dashboard,name="dashboard"),
    path('accomodations/<uuid:uuid>/',views.accomodation_detail,name="view_accommodation"),
    path('apply/<uuid:landlord_id>', views.apply, name='apply_for_accommodation_django'),
    path('dashboard/<uuid:accommodation_id>/applications/', views.view_application_details, name='view_application_details'),
    path('application-feedback/<uuid:accommodation_id>/',views.application_feedback, name="application_feedback") 

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
