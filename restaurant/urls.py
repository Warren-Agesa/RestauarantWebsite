from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'), 
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),    
    path('contact/', views.contact, name='contact'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('menu/<slug:slug>/', views.menu_detail, name='menu_detail'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/<int:order_id>/', views.view_order, name='view_order'),
    path('book-event/', views.event_booking, name='event_booking'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/order/<int:order_id>/update/', views.update_order_progress, name='update_order_progress'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
