from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission


from .forms import UserCreationForm, UserChangeForm
from .models import User, EmailVerificationToken


class FSUserAdmin(UserAdmin): 
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'email_verified', 'username','full_name','religion','gender','date_of_birth','is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser',)
    list_filter = ('email','email_verified', 'username','is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)
    fieldsets = (
        ('FS_USERS_INFO', {'fields': ('email',  'username', 'full_name', 'religion','password','gender', 'date_of_birth', 'email_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Add New backend', {
            'classes': ('wide',),
            'fields': ('email','username', 'full_name','religion', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email','username', 'religion', 'gender','date_of_birth', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)
    ordering = ('email','username', 'religion', 'gender', 'date_of_birth', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)




admin.site.register(User, FSUserAdmin)


@admin.register(EmailVerificationToken)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'token', 'verified','created_at')