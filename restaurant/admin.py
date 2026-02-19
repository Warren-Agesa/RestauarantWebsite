from django.contrib import admin
from .models import MenuItem, Reservation, ContactMessage, Review, Order, OrderItem, Payment, EventBooking, HeroSlide, Event, Profile

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'subtitle')
    ordering = ('order', 'created_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-date', 'created_at')

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
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Review)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'progress', 'created_at')
    list_filter = ('status', 'progress', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'event_date', 'guests', 'created_at')
    search_fields = ('name', 'email', 'event_type')
    list_filter = ('event_type', 'event_date', 'created_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'full_name')

admin.site.register(Profile, ProfileAdmin)