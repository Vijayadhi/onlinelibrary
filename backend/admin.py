from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.forms import CustomUserCreationForm, CustomUserChangeForm
from backend.models import CustomUser, Categories, Books, Authors, IssuseNewBooks


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields':('email', 'username', 'full_name', 'mobile_no', 'date_of_birth', 'student_id', 'password1', 'password2', 'is_staff', 'is_active', 'status')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categories)
admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(IssuseNewBooks)





