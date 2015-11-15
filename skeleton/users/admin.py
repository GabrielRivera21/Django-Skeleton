from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class MyUserAdmin(UserAdmin, admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('is_admin', 'is_active',)

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()

    fieldsets = ((None, {'fields': ('email', 'password')}),
                 ('Personal Information', {'fields': ('first_name', 'last_name')}),
                 ('Permissions', {'fields': ('is_active', 'is_admin')}),)
    add_fieldsets = ((None, {'fields': ('email', 'password1', 'password2')}),
                     ('Personal Information', {'fields': ('first_name', 'last_name')}),
                     ('Permissions', {'fields': ('is_active', 'is_admin')}),)

admin.site.register(User, MyUserAdmin)
