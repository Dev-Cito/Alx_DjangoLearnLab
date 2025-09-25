from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# --- Step 4: Integrate the Custom User Model into Admin ---

# Define the admin class for the custom user model
class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # Use base forms if not customizing form fields heavily
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Custom fieldsets for the change user page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Add user fieldsets (for the add user page)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
    )
    
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Remove 'username' from fieldsets if it's been removed from the model
    # (The BaseUserAdmin references username, so we override to use 'email')
    
    # We must explicitly register the model
    # If the user model is set in settings.py, you need to use BaseUserAdmin's 
    # functionalities correctly.

# Re-register the model
admin.site.register(CustomUser, CustomUserAdmin)