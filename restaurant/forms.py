from django import forms
from .models import Reservation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests, allergies, or notes?',
                'rows': 3
            }),
        }

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    phone = forms.CharField(max_length=20, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["full_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Save phone to Profile model
            Profile.objects.create(user=user, phone=self.cleaned_data["phone"])
        return user

class EventBookingForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_date = forms.DateField(label="Event Date", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    guests = forms.IntegerField(label="Number of Guests", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    event_type = forms.ChoiceField(
        label="Event Type",
        choices=[
            ('', 'Select Event Type'),
            ('birthday', 'Birthday'),
            ('wedding', 'Wedding'),
            ('corporate', 'Corporate'),
            ('private', 'Private Party'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Additional Requests",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Let us know any special requests...'})
    )