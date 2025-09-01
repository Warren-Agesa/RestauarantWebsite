from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Review, ContactMessage, Reservation, Order, OrderItem, Payment, EventBooking,HeroSlide, Event
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ReservationForm, CustomUserCreationForm, EventBookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .utils.mpesa import lipa_na_mpesa

def index(request):
    featured_dishes = MenuItem.objects.filter(available=True)[:3]
    special_menu = MenuItem.objects.filter(is_special=True, available=True).order_by('-created_at')[:3]
    top_selling = MenuItem.objects.filter(is_top_selling=True, available=True).order_by('-created_at')[:4]
    hero_slides = HeroSlide.objects.all().order_by('order')
    events = Event.objects.order_by('date')[:3]
    return render(request, 'restaurant/index.html', {
        'featured_dishes': featured_dishes,
        'special_menu': special_menu,
        'top_selling': top_selling,
        'hero_slides': hero_slides,
        'events': events

    })

def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True)

    query = request.GET.get('q')
    if query:
        menu_items = menu_items.filter(name__icontains=query)

    category = request.GET.get('category')
    if category and category != 'all':
        menu_items = menu_items.filter(category=category)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        menu_items = menu_items.order_by('price')
    elif sort == 'price_desc':
        menu_items = menu_items.order_by('-price')
    elif sort == 'name':
        menu_items = menu_items.order_by('name')
    else:  
        menu_items = menu_items.order_by('-created_at')

    paginator = Paginator(menu_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'sort': sort,
    }
    return render(request, 'restaurant/menu.html', context)


def about(request):
    return render(request, 'restaurant/about.html')


def menu_detail(request, slug):
    product = get_object_or_404(MenuItem, slug=slug)
    related_products = MenuItem.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:3]
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if user_name and rating and comment:
            Review.objects.create(
                menu_item=product,
                user_name=user_name,
                rating=rating,
                comment=comment
            )
    return render(request, 'restaurant/product_detail.html', {'product': product, 'related_products': related_products,})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=None,  
            recipient_list=['warrenfred98@gmail.com'],
            fail_silently=False,  
        )

        messages.success(request, "Your message was sent successfully!")
        return redirect('index')
    return render(request, 'restaurant/contact.html')


def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Reservation submitted successfully!')
            subject = f"New Reservation from {reservation.name}"
            message = (
                f"Name: {reservation.name}\n"
                f"Email: {reservation.email}\n"
                f"Phone: {reservation.phone}\n"
                f"Date: {reservation.date}\n"
                f"Time: {reservation.time}\n"
                f"Guests: {reservation.guests}\n"
                f"Special Requests: {reservation.message or 'None'}"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.OWNER_EMAIL])

            return redirect('index')
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reservation.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'restaurant/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'restaurant/profile.html')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    cart_items = []
    cart_total = 0

    for item_id, quantity in cart.items():
        try:
            item_id = int(item_id)
            quantity = int(quantity)
            product = MenuItem.objects.get(pk=item_id)
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
            cart_total += total_price
        except (ValueError, MenuItem.DoesNotExist):
            continue

    if request.method == 'POST':
        delivery_option = request.POST.get('delivery_option')
        delivery_address = request.POST.get('delivery_address', '')
        phone = request.POST.get('phone')

        if delivery_option == 'delivery' and not delivery_address:
            messages.error(request, "Please provide a delivery address.")
            return render(request, 'restaurant/checkout.html', {
                'cart_items': cart_items,
                'cart_total': cart_total,
            })

        if not phone:
            messages.error(request, "Please provide your Mpesa phone number.")
            return render(request, 'restaurant/checkout.html', {
                'cart_items': cart_items,
                'cart_total': cart_total,
            })
        response = lipa_na_mpesa(phone, cart_total)

        if isinstance(response, dict) and response.get("ResponseCode") == "0":
            order = Order.objects.create(
                user=request.user,
                delivery_option=delivery_option,
                delivery_address=delivery_address if delivery_option == 'delivery' else '',
                total=cart_total,
                phone=phone,
                status='paid'
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
            Payment.objects.create(
                order=order,
                mpesa_code=response.get("CheckoutRequestID", ""),
                status='pending'
            )
            request.session['cart'] = {} 
            messages.success(request, "Payment initiated. Check your phone to complete the payment.")
            return redirect('menu')
        else:
            error_message = response.get("errorMessage") or response.get("ResponseDescription") or "Unknown error"
            messages.error(request, f"Payment failed: {error_message}")

    return render(request, 'restaurant/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })
    
class CustomLoginView(LoginView):
    template_name = 'restaurant/login.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "Login successful! Welcome back.")
        return super().form_valid(form)
    

def add_to_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if not isinstance(cart, dict):
            cart = {}
        if 'quantity' in request.POST:
            cart[str(item_id)] = quantity
        else:
            cart[str(item_id)] = cart.get(str(item_id), 0) + quantity
        request.session['cart'] = cart
        from django.contrib import messages
        messages.success(request, "Item added to Cart!")
        return redirect('view_cart')
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def view_cart(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    cart_items = []
    cart_total = 0

    for item_id, quantity in cart.items():
        try:
            item_id = int(item_id)
            quantity = int(quantity)
            product = MenuItem.objects.get(pk=item_id)
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
            cart_total += total_price
        except (ValueError, MenuItem.DoesNotExist):
            continue

    return render(request, 'restaurant/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    item_id = str(item_id)
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@login_required
def process_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        cart = request.session.get('cart', {})
        cart_total = 0
        for item_id, quantity in cart.items():
            try:
                item_id = int(item_id)
                quantity = int(quantity)
                product = MenuItem.objects.get(pk=item_id)
                cart_total += product.price * quantity
            except (ValueError, MenuItem.DoesNotExist):
                continue

        if not phone or not cart:
            messages.error(request, "Invalid phone or empty cart.")
            return redirect('checkout')

        response = lipa_na_mpesa(phone, cart_total)
        if response.get("ResponseCode") == "0":
            messages.success(request, "Payment initiated. Check your phone.")
            return redirect('menu')
        else:
            error_message = response.get("errorMessage") or response.get("ResponseDescription", "Unknown error")
            messages.error(request, f"Payment failed: {error_message}")
            return redirect('checkout')
        
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'restaurant/order_success.html', {'order': order})

@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'restaurant/view_order.html', {'order': order})

def event_booking(request):
    if request.method == 'POST':
        form = EventBookingForm(request.POST)
        if form.is_valid():
            booking = EventBooking.objects.create(**form.cleaned_data)
            admin_email = getattr(settings, 'OWNER_EMAIL', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            if admin_email:
                send_mail(
                    subject=f"New Event Booking: {booking.event_type} by {booking.name}",
                    message=(
                        f"Name: {booking.name}\n"
                        f"Email: {booking.email}\n"
                        f"Phone: {booking.phone}\n"
                        f"Event Date: {booking.event_date}\n"
                        f"Guests: {booking.guests}\n"
                        f"Event Type: {booking.event_type}\n"
                        f"Message: {booking.message}"
                    ),
                    from_email=None,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
            messages.success(request, "Your event booking has been received! We'll contact you soon.")
            return redirect('event_booking')
    else:
        form = EventBookingForm()
    return render(request, 'restaurant/event_booking.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'restaurant/my_orders.html', {'orders': orders})