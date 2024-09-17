from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("logout_view", views.logout_view, name="logout"),
    path("register_doctor", views.register_doctor, name="register_doctor"),
    path("login_doctor", views.login_doctor, name="login_doctor"),
    path("doctor_details", views.doctor_details, name="doctor_details"),
    path("reviews",views.reviews, name="reviews"),
    path("book_appointment/<int:id>",views.book_appointment, name="book_appointment"),
    path("profile/<int:id>",views.profile, name="profile"),
    path("appointment",views.appointment, name="appointment"),
    path("cancel_appointment/<int:id>/",views.cancel_appointment, name="cancel_appointment"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("complete_appointment/<int:id>",views.complete_appointment,name="complete_appointment"),
    path("doctors",views.doctors, name="doctors"),
    path("invoice/<int:id>",views.invoice,name="invoice"),
    path("search",views.search, name="search"),
    path("edit_profile",views.edit_profile, name="edit_profile"),
    path("edit_dashboard",views.edit_dashboard, name="edit_dashboard"),
]
