from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Appointment, Review
# Register your models here.

# admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Review)

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # add_form = CustomUserCreationForm
#     # form = CustomUserChangeForm
#     list_display = ('username', 'email', 'phone', 'dob', 'location', 'is_staff')
#     search_fields = ('email', 'username', 'phone')
#     ordering = ('email',)

admin.site.register(CustomUser)