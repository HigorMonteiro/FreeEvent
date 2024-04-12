from django.contrib import admin

from .models import Address, Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'date',
        'status',
    ]
    search_fields = ['title']
    list_filter = ['title', 'status']
    list_per_page = 50


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'address']
    search_fields = ['phone', 'address']
    list_filter = ['phone', 'address']
    list_per_page = 50

    exclude = [
        'id',
        'created_at',
        'updated_at',
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions',
        'last_login',
        'date_joined',
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'city', 'country', 'postal_code']
    search_fields = ['street', 'city', 'country', 'postal_code']
    list_filter = ['city', 'country']
    list_per_page = 50
