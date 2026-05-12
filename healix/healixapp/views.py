# from http import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Nurse, SuperAdmin

from django.shortcuts import render, redirect
from .models import SuperAdmin, Admin
from django.contrib import messages

def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # SuperAdmin Login
        try:
            superadmin = SuperAdmin.objects.get(email=email)
            if password == superadmin.password:
                request.session['superadmin_id'] = superadmin.id
                messages.success(request, "Login successful! Welcome Super Admin.")
                return redirect('superadmin_dashboard')
            else:
                error = "Invalid password"
        except SuperAdmin.DoesNotExist:
            pass

        # Admin Login
        try:
            admin = Admin.objects.get(email=email)
            if password == admin.password:
                request.session['admin_id'] = admin.id
                messages.success(request, "Login successful! Welcome Admin.")
                return redirect('admin_dashboard')
            else:
                error = "Invalid password"
        except Admin.DoesNotExist:
            pass

        # Nurse Login
        try:
            nurse = Nurse.objects.get(email=email)
            if password == nurse.password:
                request.session['nurse_id'] = nurse.id
                messages.success(request, "Login successful! Welcome Nurse.")
                return redirect('nurse_dashboard')
            else:
                error = "Invalid password"
        except Nurse.DoesNotExist:
            pass

        # Doctor Login
        try:
            doctor = Doctor.objects.get(email=email)
            if password == doctor.password:
                request.session['doctor_id'] = doctor.id
                messages.success(request, "Login successful! Welcome Doctor.")
                return redirect('doctor_dashboard')
            else:
                error = "Invalid password"
        except Doctor.DoesNotExist:
            pass

        if not error:
            error = "User does not exist"
        
    return render(request, 'login.html', {'error': error})


#superadmin view fnctions start

from .models import OldAgeHome, Admin, SuperAdmin

from django.shortcuts import render, redirect
from .models import OldAgeHome, Admin, SuperAdmin

def superadmin_dashboard(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    # Query all old age homes and admins
    homes = OldAgeHome.objects.all()
    admins = Admin.objects.all()  # <-- Make sure you pass this

    return render(request, 'superadmin/superadmin_dashboard.html', {
        'homes': homes,
        'admins': admins
    })

from django.contrib import messages

def add_home(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone_number')
        place = request.POST.get('place')

        OldAgeHome.objects.create(name=name, address=address, phone_number=phone, place=place)

        messages.success(request, "Home added successfully!")
        return redirect('add_home')   # Stay on the same page

    return render(request, 'superadmin/add_home.html')


from .models import OldAgeHome, Admin, SuperAdmin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import OldAgeHome, Admin, SuperAdmin
from django.contrib import messages

def add_admin(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    homes = OldAgeHome.objects.all()

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        home_id = request.POST.get('home')

        superadmin = SuperAdmin.objects.get(id=request.session['superadmin_id'])

        # Validation
        if not name or not email or not password or not home_id:
            messages.error(request, "All fields are required.")
            return redirect('add_admin')

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format.")
            return redirect('add_admin')

        if len(password) < 6:
            messages.warning(request, "Password must be at least 6 characters.")
            return redirect('add_admin')

        home = get_object_or_404(OldAgeHome, id=home_id)

        # Check duplicate
        if Admin.objects.filter(home=home).exists():
            messages.error(request, f"An admin already exists for {home.name}.")
            return redirect('add_admin')

        # Create admin
        Admin.objects.create(
            name=name,
            email=email,
            password=password,
            home=home,
            superadmin=superadmin
        )

        messages.success(request, "Admin added successfully!")
        return redirect('list_admins')

    return render(request, 'superadmin/add_admin.html', {'homes': homes})

from django.shortcuts import render, redirect
from .models import OldAgeHome, Admin, SuperAdmin

# List Old Age Homes
def list_homes(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    homes = OldAgeHome.objects.all()  # Or filter by superadmin if needed
    return render(request, 'superadmin/list_homes.html', {'homes': homes})

# List Admins
def list_admins(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    superadmin = SuperAdmin.objects.get(id=request.session['superadmin_id'])
    admins = Admin.objects.filter(superadmin=superadmin)
    return render(request, 'superadmin/list_admins.html', {'admins': admins})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, OldAgeHome, SuperAdmin

# Edit Admin
from django.contrib import messages

def edit_admin(request, admin_id):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    admin = get_object_or_404(Admin, id=admin_id)
    homes = OldAgeHome.objects.all()

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        home_id = request.POST.get('home')

        # Validation
        if not name or not email or not password or not home_id:
            messages.error(request, "All fields are required.")
            return redirect('edit_admin', admin_id=admin_id)

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format.")
            return redirect('edit_admin', admin_id=admin_id)

        if len(password) < 6:
            messages.warning(request, "Password must be at least 6 characters.")
            return redirect('edit_admin', admin_id=admin_id)

        home = get_object_or_404(OldAgeHome, id=home_id)

        admin.name = name
        admin.email = email
        admin.password = password
        admin.home = home
        admin.save()

        messages.success(request, "Admin updated successfully!")
        return redirect('list_admins')

    return render(request, 'superadmin/edit_admin.html', {
        'admin': admin,
        'homes': homes,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin

# Delete Admin
def delete_admin(request, admin_id):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    admin = get_object_or_404(Admin, id=admin_id)
    admin.delete()

    messages.success(request, "Admin deleted successfully!")
    return redirect('list_admins')


from django.shortcuts import render, redirect, get_object_or_404
from .models import OldAgeHome, SuperAdmin

# Edit Old Age Home
def edit_home(request, home_id):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    home = get_object_or_404(OldAgeHome, id=home_id)

    if request.method == "POST":
        home.name = request.POST.get('name')
        home.address = request.POST.get('address')
        home.phone_number = request.POST.get('phone_number')
        home.place = request.POST.get('place')
        home.save()

        messages.success(request, "Old Age Home updated successfully!")
        return redirect('list_homes')

    return render(request, 'superadmin/edit_home.html', {'home': home})

# Delete Old Age Home
def delete_home(request, home_id):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    home = get_object_or_404(OldAgeHome, id=home_id)
    home.delete()

    messages.warning(request, "Old Age Home deleted!")
    return redirect('list_homes')



def view_superadmin_profile(request):
    if not request.session.get('superadmin_id'):
        return redirect('superadmin_login')

    superadmin = SuperAdmin.objects.get(id=request.session['superadmin_id'])
    return render(request, 'superadmin/profile.html', {'superadmin': superadmin})



#superadmin functions end here

#admin functions start here

def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('login_view')

    admin = Admin.objects.get(id=request.session['admin_id'])
    home = admin.home

    return render(request, 'admin/admin_dashboard.html', {
        'admin': admin,
        'home': home
    })

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
def add_list_nurses(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])
    home = admin.home
    error = None

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone_number')

        # VALIDATIONS
        if not all([name, email, password, phone]):
            messages.error(request, "All fields are required.")
            return redirect('add_list_nurses')

        if Nurse.objects.filter(email=email).exists():
            messages.warning(request, "Nurse with this email already exists.")
            return redirect('add_list_nurses')

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format.")
            return redirect('add_list_nurses')

        if not re.fullmatch(r'[6-9]\d{9}', phone):
            messages.warning(request, "Phone number must be 10 digits and start with 6-9.")
            return redirect('add_list_nurses')

        if len(password) < 6 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            messages.warning(request, "Password must be at least 6 characters and include letters + numbers.")
            return redirect('add_list_nurses')

        # IF OK — SAVE
        Nurse.objects.create(
            admin=admin,
            home=home,
            name=name,
            email=email,
            password=password,
            phone_number=phone
        )
        messages.success(request, "Nurse added successfully!")
        return redirect('add_list_nurses')

    nurses = Nurse.objects.filter(home=home)
    return render(request, 'admin/add_list_nurses.html', {"home": home, "nurses": nurses})

from django.http import HttpResponse
def delete_nurse(request, nurse_id):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    try:
        nurse = Nurse.objects.get(id=nurse_id)
        admin = Admin.objects.get(id=request.session['admin_id'])

        if nurse.home != admin.home:
            messages.error(request, "Not authorized to delete this nurse.")
            return redirect('add_list_nurses')

        nurse.delete()
        messages.success(request, "Nurse deleted successfully!")

    except Nurse.DoesNotExist:
        messages.warning(request, "Nurse does not exist.")

    return redirect('add_list_nurses')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Doctor, Admin
import re

from django.shortcuts import render, redirect
from .models import Resident, Admin, Nurse, Doctor, Vitals
def add_list_doctors(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])
    home = admin.home

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone_number')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')

        # VALIDATIONS
        if not all([name, email, password, phone, specialization, qualification]):
            messages.error(request, "All fields are required.")
            return redirect('add_list_doctors')

        if Doctor.objects.filter(email=email).exists():
            messages.warning(request, "Doctor with this email already exists.")
            return redirect('add_list_doctors')

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format.")
            return redirect('add_list_doctors')

        if not re.fullmatch(r'[6-9]\d{9}', phone):
            messages.warning(request, "Phone number must be 10 digits and start with 6-9.")
            return redirect('add_list_doctors')

        if len(password) < 6 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            messages.warning(request, "Password must be at least 6 characters and include letters + numbers.")
            return redirect('add_list_doctors')

        # SAVE
        Doctor.objects.create(
            admin=admin,
            home=home,
            name=name,
            email=email,
            password=password,
            phone_number=phone,
            specialization=specialization,
            qualification=qualification
        )
        messages.success(request, "Doctor added successfully!")
        return redirect('add_list_doctors')

    doctors = Doctor.objects.filter(home=home)
    return render(request, 'admin/add_list_doctors.html', {"home": home, "doctors": doctors})

def delete_doctor(request, doctor_id):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        admin = Admin.objects.get(id=request.session['admin_id'])

        if doctor.home != admin.home:
            messages.error(request, "You cannot delete a doctor from another home.")
            return redirect('add_list_doctors')

        doctor.delete()
        messages.success(request, "Doctor deleted successfully!")

    except Doctor.DoesNotExist:
        messages.warning(request, "Doctor does not exist.")

    return redirect('add_list_doctors')



def view_admin_profile(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])
    return render(request, 'admin/profile.html', {'admin': admin})



def add_resident(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])
    home = admin.home

    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        room_number = request.POST.get('room_number')
        emergency_name = request.POST.get('emergency_contact_name')
        emergency_phone = request.POST.get('emergency_phone')
        emergency_address = request.POST.get('emergency_address')
        emergency_place = request.POST.get('emergency_place')

        if not all([name, age, gender, room_number, emergency_name, emergency_phone, emergency_address, emergency_place]):
            messages.error(request, "All fields are required.")
            return redirect('add_resident')

        if len(emergency_phone) != 10 or not emergency_phone.isdigit():
            messages.warning(request, "Emergency phone must be 10 digits.")
            return redirect('add_resident')

        Resident.objects.create(
            home=home,
            name=name,
            age=age,
            gender=gender,
            room_number=room_number,
            emergency_contact_name=emergency_name,
            emergency_phone=emergency_phone,
            emergency_address=emergency_address,
            emergency_place=emergency_place
        )

        messages.success(request, "Resident added successfully!")
        return redirect('add_resident')

    return render(request, 'admin/add_resident.html', {"home": home})


def view_residents(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = Admin.objects.get(id=request.session['admin_id'])
    home = admin.home

    residents = Resident.objects.filter(home=home)

    return render(request, 'admin/view_residents.html', {
        'residents': residents,
        'home': home
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import Resident, Admin
def edit_resident(request, resident_id):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    resident = get_object_or_404(Resident, id=resident_id)

    if request.method == "POST":
        resident.name = request.POST.get('name')
        resident.age = request.POST.get('age')
        resident.gender = request.POST.get('gender')
        resident.room_number = request.POST.get('room_number')
        resident.emergency_contact_name = request.POST.get('emergency_contact_name')
        resident.emergency_phone = request.POST.get('emergency_phone')
        resident.emergency_address = request.POST.get('emergency_address')
        resident.emergency_place = request.POST.get('emergency_place')
        resident.save()

        messages.success(request, "Resident updated successfully!")
        return redirect('view_residents')

    return render(request, 'admin/edit_resident.html', {"resident": resident})
def delete_resident(request, resident_id):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    resident = get_object_or_404(Resident, id=resident_id)
    resident.delete()

    messages.success(request, "Resident deleted successfully!")
    return redirect('view_residents')

#Admin functions end here
#Nurse functions start here
def nurse_dashboard(request):
    if not request.session.get('nurse_id'):
        return redirect('login_view')

    nurse = Nurse.objects.get(id=request.session['nurse_id'])
    home = nurse.home

    # Get all residents (patients) of this nurse's home
    patients = Resident.objects.filter(home=home)

    return render(request, 'nurse/nurse_dashboard.html', {
        'nurse': nurse,
        'home': home,
        'patients': patients,  # Pass patients to template
    })



from .models import Nurse
def nurse_update_profile(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)

    if request.method == "POST":
        nurse.name = request.POST.get("name")
        nurse.email = request.POST.get("email")
        nurse.phone_number = request.POST.get("phone_number")
        nurse.address = request.POST.get("address")
        nurse.place = request.POST.get("place")
        nurse.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("nurse_profile", nurse_id=nurse.id)

    return render(request, "nurse/update_profile.html", {"nurse": nurse})



def list_patients(request):
    if not request.session.get('nurse_id'):
        return redirect('login_view')

    nurse = Nurse.objects.get(id=request.session['nurse_id'])
    home = nurse.home
    patients = Resident.objects.filter(home=home)

    return render(request, 'nurse/list_patients.html', {
        'patients': patients,
        'home': home,
    })
from django.shortcuts import render, redirect
from .models import Vitals, Nurse, Doctor, Resident
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Vitals, Nurse, Doctor, Resident
from django.core.cache import cache
from django.http import JsonResponse
def manage_vitals(request):

    nurse_id = request.session.get("nurse_id")
    if not nurse_id:
        return redirect("login")

    nurse = Nurse.objects.get(id=nurse_id)

    patients = Resident.objects.all()
    doctors = Doctor.objects.all()
    vitals_list = Vitals.objects.order_by('-created_at')

    latest_vitals = cache.get("latest_vitals", {})

    if request.method == "POST":
        blood_pressure = request.POST.get("blood_pressure")
        blood_sugar = request.POST.get("blood_sugar")

        # HEART RATE NOW CONTAINS bp_pulse FROM HTML SCRIPT
        heart_rate = request.POST.get("heart_rate")

        oxygen_level = request.POST.get("oxygen_level")

        print("DEBUG: Saving pulse as heart rate:", heart_rate)

        Vitals.objects.create(
            nurse=nurse,
            resident_id=request.POST.get("resident"),
            doctor_id=request.POST.get("doctor"),
            blood_pressure=blood_pressure,
            blood_sugar=blood_sugar,
            heart_rate=heart_rate,       # 👈 SAVES bp_pulse HERE
            oxygen_level=oxygen_level
        )

        return redirect("manage_vitals")

    return render(request, "nurse/manage_vitals.html", {
        "patients": patients,
        "doctors": doctors,
        "vitals_list": vitals_list,
        "latest_vitals": latest_vitals
    })

def latest_vitals_api(request):
    data = cache.get("latest_vitals", {})
    return JsonResponse(data)

def edit_vitals(request, vitals_id):
    vitals = get_object_or_404(Vitals, id=vitals_id)
    doctors = Doctor.objects.filter(home=vitals.resident.home)

    if request.method == "POST":
        vitals.doctor = Doctor.objects.get(id=request.POST.get('doctor'))
        vitals.blood_pressure = request.POST.get('blood_pressure')
        vitals.blood_sugar = request.POST.get('blood_sugar')
        vitals.heart_rate = request.POST.get('heart_rate')
        vitals.oxygen_level = request.POST.get('oxygen_level')
        vitals.save()

        messages.success(request, "Vitals updated successfully!")
        return redirect('manage_vitals')

    return render(request, 'nurse/edit_vitals.html', {
        'vitals': vitals,
        'doctors': doctors
    })
def delete_vitals(request, vitals_id):
    vitals = get_object_or_404(Vitals, id=vitals_id)
    vitals.delete()
    messages.success(request, "Vitals deleted successfully!")
    return redirect('manage_vitals')


def nurse_view_prescriptions(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    prescriptions = Prescription.objects.filter(resident=resident).order_by("-created_at")
    return render(request, "nurse/view_prescriptions.html", {
        "resident": resident,
        "prescriptions": prescriptions,
    })

# Nurse Profile
def nurse_profile(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    return render(request, "nurse/nurse_profile.html", {"nurse": nurse})

#nurse functions end here


# Doctor functions start here

from django.shortcuts import render, get_object_or_404
from .models import Resident, Vitals, Doctor

def doctor_view_patients(request):
    # Assuming doctor_id is stored in session
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('login_view')

    doctor = Doctor.objects.get(id=doctor_id)
    patients = Resident.objects.filter(home=doctor.home)

    return render(request, 'doctor/list_patients.html', {
        'patients': patients
    })


from django.shortcuts import render, get_object_or_404
from .models import Resident, Vitals

from django.shortcuts import render, get_object_or_404
from .models import Resident, Vitals
from django.shortcuts import render, get_object_or_404
from .models import Resident, Vitals
from django.http import JsonResponse

def doctor_view_vitals(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    vitals_list = Vitals.objects.filter(resident=resident).order_by('created_at')

    if vitals_list.exists():
        last_vitals = vitals_list.last()

        # Extract systolic portion
        if last_vitals.blood_pressure and "/" in last_vitals.blood_pressure:
            systolic = int(last_vitals.blood_pressure.split("/")[0])
        else:
            systolic = 0

        blood_pressure = systolic
        blood_sugar = last_vitals.blood_sugar or 0
        heart_rate = last_vitals.heart_rate or 0   # ✔ pulse value
        oxygen_level = last_vitals.oxygen_level or 0

    else:
        last_vitals = None
        blood_pressure = 0
        blood_sugar = 0
        heart_rate = 0
        oxygen_level = 0

    return render(request, 'doctor/view_vitals.html', {
        'resident': resident,
        'vitals_list': vitals_list,
        'last_vitals': last_vitals,
        'blood_pressure': blood_pressure,
        'blood_sugar': blood_sugar,
        'heart_rate': heart_rate,        # ✔ added
        'oxygen_level': oxygen_level,
    })


def latest_vitals_json(request, resident_id):
    try:
        vitals = Vitals.objects.filter(resident_id=resident_id).latest('created_at')
        systolic = int(vitals.blood_pressure.split("/")[0]) if "/" in vitals.blood_pressure else 0

        data = {
            "blood_pressure": systolic,
            "blood_sugar": vitals.blood_sugar,
            "heart_rate": vitals.heart_rate,           # ✔ pulse here
            "oxygen_level": vitals.oxygen_level,
            "recorded_at": vitals.created_at.strftime("%Y-%m-%d %H:%M")
        }
    except Vitals.DoesNotExist:
        data = {
            "blood_pressure": 0,
            "blood_sugar": 0,
            "heart_rate": 0,
            "oxygen_level": 0,
            "recorded_at": ""
        }

    return JsonResponse(data)

# def doctor_view_profile(request, resident_id):
#     resident = get_object_or_404(Resident, id=resident_id)
#     return render(request, 'doctor/view_profile.html', {
#         'resident': resident
#     })



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resident, Prescription
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resident, Prescription
def add_prescription(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)

    if request.method == "POST":
        medicine_name = request.POST.get("medicine_name")
        dosage = request.POST.get("dosage")
        duration = request.POST.get("duration")
        notes = request.POST.get("additional_notes")

        if not all([medicine_name, dosage, duration]):
            messages.error(request, "All fields are required.")
            return redirect('doctor_view_vitals', resident_id=resident.id)

        Prescription.objects.create(
            resident=resident,
            medicine_name=medicine_name,
            dosage=dosage,
            duration=duration,
            additional_notes=notes
        )

        messages.success(request, "Prescription added successfully!")
        return redirect('doctor_view_vitals', resident_id=resident.id)

    return redirect('doctor_view_vitals', resident_id=resident_id)

from django.shortcuts import render, get_object_or_404
from .models import Resident, Vitals, Prescription
from django.shortcuts import render, get_object_or_404
from .models import Resident, Prescription



from django.shortcuts import render, get_object_or_404
from .models import Nurse, Doctor


# Doctor Profile
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, "doctor/doctor_profile.html", {"doctor": doctor})



# views.py
from django.shortcuts import render, redirect, get_object_or_404

# views.py
from .models import Doctor
def doctor_update_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        doctor.name = request.POST.get("name")
        doctor.email = request.POST.get("email")
        doctor.phone_number = request.POST.get("phone_number")
        doctor.place = request.POST.get("place")
        doctor.address = request.POST.get("address")
        doctor.specialization = request.POST.get("specialization")
        doctor.qualification = request.POST.get("qualification")
        doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("doctor_profile", doctor_id=doctor.id)

    return render(request, "doctor/update_profile.html", {"doctor": doctor})

def doctor_dashboard(request):
    if not request.session.get('doctor_id'):
        return redirect('login_view')

    doctor = Doctor.objects.get(id=request.session['doctor_id'])
    home = doctor.home

    return render(request, 'doctor/doctor_dashboard.html', {
        'doctor': doctor,
        'home': home
    })
