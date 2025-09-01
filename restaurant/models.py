from django.db import models
from datetime import time
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    ingredients = models.TextField(blank=True, null=True, help_text="List of ingredients used in the dish.")
    procedure = models.TextField(blank=True, null=True, help_text="Preparation procedure for the dish.")
    made_by = models.CharField(max_length=100, blank=True, null=True, help_text="Chef or cook who made the dish.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False, help_text="Is this a special menu item?")
    is_top_selling = models.BooleanField(default=False, help_text="Is this a top selling item?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField()
    guests = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.name} on {self.date}"
    
class Review(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='reviews', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class SiteSettings(models.Model):
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField(default="12:00")
    guests = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)  # Optional description field

    def __str__(self):
        return f"Reservation for {self.name} on {self.date} at {self.time}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    # Add more fields as needed, e.g. address, avatar, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_option = models.CharField(max_length=20, choices=[('eat_in', 'Eat In'), ('delivery', 'Delivery')])
    delivery_address = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    progress = models.CharField(
        max_length=30,
        choices=[
            ('received', 'Order Received'),
            ('preparing', 'Preparing'),
            ('ready', 'Ready for Pickup/Delivery'),
            ('delivered', 'Delivered'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='received'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
class EventBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_date = models.DateField()
    guests = models.PositiveIntegerField()
    event_type = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_type} on {self.event_date}"
    

class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero_slides/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # <-- add this

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # <-- add this

    def __str__(self):
        return self.title