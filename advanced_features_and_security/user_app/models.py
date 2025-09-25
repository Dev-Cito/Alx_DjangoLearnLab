from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- Step 3: Create User Manager for Custom User Model ---

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        The custom fields (date_of_birth, profile_photo) are also handled.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Set default values for custom fields if not provided for superuser creation
        # You might want to skip required checks on admin creation, or provide defaults.
        # For simplicity, we assume username, email, and password are sufficient
        # and non-required fields can be null/blank.

        return self.create_user(email, password, **extra_fields)


# --- Step 1: Set Up the Custom User Model ---

class CustomUser(AbstractUser):
    # Remove the username field (optional, but common for email-based auth)
    # If you want to keep username, you don't need to explicitly define it.
    # To remove it and use email as primary identifier:
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Custom fields to add:
    date_of_birth = models.DateField(null=True, blank=True)
    # Note: Requires Pillow (pip install Pillow) and MEDIA_ROOT/MEDIA_URL settings
    # to handle file uploads. Assuming a 'profile_photos' subdirectory.
    profile_photo = models.ImageField(
        _('Profile Photo'), 
        upload_to='profile_photos/', 
        null=True, 
        blank=True
    )

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    # Required fields when creating a user via createsuperuser command
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth'] 
    
    # Use the custom manager
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

# --- Step 5: Update Your Application to Use the Custom User Model ---
# Any other model that used to have a ForeignKey/OneToOneField to django.contrib.auth.models.User
# must be updated to use settings.AUTH_USER_MODEL. 
# Example:

# from django.conf import settings

# class Post(models.Model):
#     # Use settings.AUTH_USER_MODEL instead of 'auth.User' or 'CustomUser' directly
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE
#     )
#     title = models.CharField(max_length=255)
#     content = models.TextField()

#     def __str__(self):
#         return self.title