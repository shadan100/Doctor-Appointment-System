from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.files.storage import FileSystemStorage
from .models import CustomUser, Doctor, Appointment, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa
from datetime import datetime

User = get_user_model()


@login_required(login_url="login")
def home(request):
    return render(request, "main/home.html")


@login_required(login_url="login")
def doctors(request):
    doctor = Doctor.objects.all()
    return render(request, "main/doctors.html", {"doctor": doctor})


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "main/login.html")


def login_doctor(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "main/login_doctor.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "main/login_doctor.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        address = request.POST["address"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "main/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, phone=phone, dob=dob, address=address)
            user.save()
        except IntegrityError:
            return render(request, "main/register.html", {
                "message": "Username already taken."
            })
        auth_login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "main/register.html")


def register_doctor(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        address = request.POST["address"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "main/register_doctor.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, phone=phone, dob=dob, address=address)
            user.save()
        except IntegrityError:
            return render(request, "main/register_doctor.html", {
                "message": "Username already taken."
            })
        auth_login(request, user)
        return HttpResponseRedirect(reverse("doctor_details"))
    else:
        return render(request, "main/register_doctor.html")


def doctor_details(request):
    if request.method == "GET":
        return render(request, "main/doctor_details.html")
    else:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        url = fs.url(filename)
        details = Doctor(
            user=request.user,
            designation=request.POST["designation"],
            speciality=request.POST["speciality"],
            experience=request.POST["experience"],
            info=request.POST["info"],
            fee=request.POST["fee"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
            profile_image=url
        )
        details.save()
        return HttpResponseRedirect(reverse("login_doctor"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="login")
def reviews(request):
    if request.method == 'POST':
        id = request.POST['id']
        review = request.POST['review']
        user = request.user
        review = Review(doctor=Doctor.objects.filter(
            id=id).first(), user=user, review=review)
        review.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'id': id}))


@login_required(login_url="login")
def book_appointment(request, id):
    if request.method == "POST":
        doctor = Doctor.objects.get(id=id)
        date = request.POST['date']
        time = request.POST['time']
        selected_time = datetime.strptime(time, '%H:%M').time()
        if doctor.start_time <= selected_time <= doctor.end_time:
            appointment = Appointment(
                doctor=doctor, user=request.user, date=date, time=time)
            appointment.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'id': id}))
        else:
            return render(request, "main/profile.html", {"message": "Appointment must be booked during working hours", "doctor": doctor})


@login_required(login_url="login")
def profile(request, id):
    if request.method == "GET":
        doctor = Doctor.objects.filter(id=id).first()
        appointment = Appointment.objects.filter(doctor=doctor)
        review = doctor.review_set.all()
        context = {
            'doctor': doctor,
            'appointment': appointment,
            'review': review
        }
        return render(request, "main/profile.html", context)


@login_required(login_url="login")
def appointment(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, "main/appointment.html", {'appointments': appointments})


@login_required(login_url="login")
def cancel_appointment(request, id):
    doctor = Doctor.objects.get(id=id)
    cancel = Appointment.objects.filter(
        user=request.user, doctor=doctor).first()
    cancel.delete()
    return HttpResponseRedirect(reverse(appointment))


@login_required(login_url="login")
def user_profile(request):
    user = request.user
    return render(request, "main/user_profile.html", {'user': user})


@login_required(login_url="login")
def dashboard(request):
    doctor = Doctor.objects.get(user=request.user)
    appointment = Appointment.objects.filter(doctor=doctor)
    reviews = doctor.review_set.all()
    context = {
        "doctor": doctor,
        "appointment": appointment,
        "reviews": reviews,
    }
    return render(request, "main/dashboard.html", context)


@login_required(login_url="login")
def complete_appointment(request, id):
    if request.method == 'GET':
        confirm = Appointment.objects.get(id=id)
        if confirm.status == "Pending":
            confirm.status = "Completed"
            confirm.save()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url="login")
def invoice(request, id):
    appoint = Appointment.objects.get(id=id)
    return render(request, "main/invoice.html", {"appoint": appoint})


@login_required(login_url="login")
def search(request):
    if request.method == "POST":
        name = request.POST.get("query")
        try:
            user = CustomUser.objects.get(username=name)
            doctor = Doctor.objects.filter(user=user)
            context = {'doctor': doctor}
        except CustomUser.DoesNotExist:
            context = {'message': 'No Doctor Found'}
        return render(request, "main/search.html", context)
    else:
        return HttpResponse("Invalid request method", status=405)


@login_required(login_url="login")
def edit_profile(request):
    if request.method == 'GET':
        return render(request, "main/edit_details.html")

    profile = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        # Update the profile instance
        profile.username = username
        profile.phone = phone
        profile.email = email
        profile.dob = dob
        profile.address = address
        profile.save()

        return HttpResponseRedirect('user_profile')
    return render(request, "main/edit_details.html")


@login_required(login_url="login")
def edit_dashboard(request):
    if request.method == 'GET':
        doctor = Doctor.objects.get(user=request.user)
        return render(request, "main/edit_dashboard.html", {"doctor": doctor})

    if request.method == 'POST':
        id = request.POST.get('id')
        profile = Doctor.objects.get(id=id)
        user = profile.user

        # update user fields
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()

        # update doctor's fields
        profile.designation = request.POST.get('designation')
        profile.speciality = request.POST.get('speciality')
        profile.experience = request.POST.get('experience')
        profile.save()

        return HttpResponseRedirect('dashboard')
    return render(request, "main/edit_dashboard.html")
