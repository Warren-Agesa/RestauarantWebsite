from django.contrib import admin
from .models import MenuItem, Reservation, ContactMessage

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'available', 'is_vegan', 'is_gluten_free', 'is_spicy',
        'created_at', 'made_by'
    )
    list_filter = ('category', 'available', 'is_vegan', 'is_gluten_free', 'is_spicy')
    search_fields = ('name', 'description', 'short_description', 'ingredients', 'made_by')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'guests')
    list_filter = ('date',)
    search_fields = ('name', 'email', 'phone')
    
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'message', 'created_at')
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)

    def has_change_permission(self, request, obj=None):
        # Prevent editing of contact messages
        return False

    def has_add_permission(self, request):
        # Prevent adding contact messages from admin
        return False

admin.site.register(ContactMessage, ContactMessageAdmin)