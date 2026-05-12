from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', login_view, name='login_view'),
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/add_home/', add_home, name='add_home'),
    path('superadmin/add_admin/', add_admin, name='add_admin'),
    path('list-homes/', views.list_homes, name='list_homes'),
    path('list-admins/', views.list_admins, name='list_admins'),
    path('edit-admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('delete-admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('edit-home/<int:home_id>/', views.edit_home, name='edit_home'),
    path('delete-home/<int:home_id>/', views.delete_home, name='delete_home'),
    path('superadmin/profile/', views.view_superadmin_profile, name='view_superadmin_profile'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('nurses/', views.add_list_nurses, name='add_list_nurses'),
    path('delete_nurse/<int:nurse_id>/', views.delete_nurse, name='delete_nurse'),
    path('doctors/', views.add_list_doctors, name='add_list_doctors'),
    path('doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('profile/', views.view_admin_profile, name='view_admin_profile'),
    path('residents/add/', views.add_resident, name='add_resident'),
    path('residents/', views.view_residents, name='view_residents'),
    path('residents/edit/<int:resident_id>/', views.edit_resident, name='edit_resident'),
    path('residents/delete/<int:resident_id>/', views.delete_resident, name='delete_resident'),
    path('nurse/dashboard/', nurse_dashboard, name='nurse_dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('nurse/patients/', views.list_patients, name='nurse_list_patients'),
    path('nurse/vitals/', views.manage_vitals, name='manage_vitals'),
    path('api/latest_vitals/', latest_vitals_api, name='latest_vitals_api'),

    path('nurse/vitals/edit/<int:vitals_id>/', views.edit_vitals, name='edit_vitals'),
    path('nurse/vitals/delete/<int:vitals_id>/', views.delete_vitals, name='delete_vitals'),

    path('doctor/patients/', views.doctor_view_patients, name='list_patients'),
    path('doctor/patient/<int:resident_id>/vitals/', views.doctor_view_vitals, name='doctor_view_vitals'),
    path('doctor/patient/<int:resident_id>/vitals/json/', views.latest_vitals_json, name='latest_vitals_json'),

    # path('doctor/patient/<int:resident_id>/profile/', views.doctor_view_profile, name='doctor_profile'),
    # urls.py
    path('doctor/patient/<int:resident_id>/add-prescription/', views.add_prescription, name='add_prescription'),
    path("nurse/resident/<int:resident_id>/prescriptions/", views.nurse_view_prescriptions, name="nurse_view_prescriptions"),

    path("nurse/<int:nurse_id>/profile/", views.nurse_profile, name="nurse_profile"),
    path("doctor/<int:doctor_id>/profile/", views.doctor_profile, name="doctor_profile"),

    # urls.py
    path("nurse/profile/<int:nurse_id>/edit/", views.nurse_update_profile, name="nurse_update_profile"),
    # urls.py
    path("doctor/profile/<int:doctor_id>/edit/", views.doctor_update_profile, name="doctor_update_profile"),
    

]