from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from .models import Product, ProductImage, ProductSize, ProductColor, MyUser, Cart, CartItem, Order, PromoCode, Address, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from django.contrib import messages

# Create your views here.
from django.contrib.auth import get_user_model
# User = get_user_model()

from django.db.models import Q

from django.forms import Form, CharField, EmailField, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth import login


from django.utils.crypto import get_random_string


from django.views.decorators.http import require_http_methods
import json


from django.core.mail import send_mail

import base64
from django.core.files.base import ContentFile

from django.http import JsonResponse

from django.core.paginator import Paginator

from .models import GOVERNORATE_CHOICES







def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message') 
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        subject = 'Contact Form'
        from_email = 'Aroratextiles.net@gmail.com'
        recipient_list = ['Aroratextiles.net@gmail.com']
        
        send_mail(subject, message, from_email, recipient_list)
        # Send confirmation email to user
        subject = 'Thanks for contacting us'
        message = f'Dear {name},\n\nThank you for contacting us. We have received your inquiry and will get back to you as soon as possible.\n\nBest regards,\nAroratextiles Team'
        from_email = 'Aroratextiles.net@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        
        return render(request, 'contact.html')

def Return(request):
    return render(request, 'Return.html')

def show_products(request, category=None, subcategory=None):
    products = Product.objects.all()
    if category:
        categories = category.split(';')
        products = products.filter(Q(category__name__in=categories))
    if subcategory:
        products = products.filter(subcategory=subcategory)

    paginator = Paginator(products, 15) # Show 15 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'categories': Product.CATEGORY_CHOICES}
    return render(request, 'products.html', context)




def design_save(request):
    if request.method == 'POST':
        # Get the image data from the request body
        data = json.loads(request.body)
        image_data = data.get('image')
        product_id = data.get('product_id')
        # Decode the image data and create a new Image object
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        product = Product.objects.get(id=product_id)
        image = Product.objects.create(image=data, user=request.user, product=product )
        image.save()
        # Return a JSON response
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Product, ProductImage
from datetime import date
#from selenium import webdriver

def create_product(request):
    if request.method == 'POST':
        # Get the selected t-shirt side (front or back)
        tshirt_side = request.POST.get('tshirt-side')

        # Get the selected size
        size = request.POST.get('size')

        # Get the selected design URL
        tshirt_design = request.POST.get('tshirt-design')

        # Get the selected t-shirt color
        tshirt_color = request.POST.get('tshirt-color')

        # Get the uploaded custom picture for the front and back sides
        front_custom_picture = request.FILES.get('front-custom-picture')
        back_custom_picture = request.FILES.get('back-custom-picture')

        # Get the entered text for the front and back sides
        front_text = request.POST.get('front-text')
        back_text = request.POST.get('back-text')

        # Get the selected font type
        font_type = request.POST.get('fontFamilySelect')

        # Get the selected text color
        text_color = request.POST.get('text-color')

        # Get the quantity
        quantity = request.POST.get('cloth_quantity')

        # Initialize a web driver (Assuming you're using Chrome)
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(chrome_options=options)
        
        # Navigate to the t-shirt design page (replace with your URL)
        driver.get(tshirt_design)

        # Capture a screenshot of the t-shirt design
        screenshot_path = 'path/to/save/screenshot.png'
        driver.save_screenshot(screenshot_path)

        # Create a new product
        product_name = f"{request.user.username}'s Design"
        product = Product(
            product_name=product_name,
            price=0,  # You can set the initial price here
            pub_date=date.today(),
            description=f"Front Text: {front_text}, Back Text: {back_text}, Font Type: {font_type}, Text Color: {text_color}",
            path=screenshot_path,  # Set the path to the screenshot
        )
        product.save()

        # Create a new product image for the back
        back_product_image = ProductImage(
            product=product,
            image=back_custom_picture,
            path="path/to/back/image",  # Provide a default path for the back image
            color=tshirt_color,
            side='back',
            text=back_text,
        )
        back_product_image.save()

        # Process other customization data as needed

        # Close the web driver
        driver.quit()
        """
        return redirect('/success/url/')  # Redirect to a success page after processing

    return render(request, 'create_product.html')

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Product, ProductImage
from django.core.files.storage import FileSystemStorage

def create_product(request):
    if request.method == 'POST':
        # Get the text inputs
        user_name = request.POST.get('user_name')
        product_name = f"{user_name}'s Design"

        # Get the image inputs
        front_image = request.FILES['front_image']
        back_image = request.FILES['back_image']

        # Save the images to your media root
        fs = FileSystemStorage()
        front_image_path = fs.save(front_image.name, front_image)
        back_image_path = fs.save(back_image.name, back_image)

        # Create a new product
        product = Product(product_name=product_name)
        product.save()

        # Create new product images and link them to the new product
        front_product_image = ProductImage(product=product, image=front_image_path)
        front_product_image.save()

        back_product_image = ProductImage(product=product, image=back_image_path)
        back_product_image.save()

        return HttpResponseRedirect('/success/url/')

    return render(request, 'create_product.html')


def send_order_confirmation_email(first_name, email, order):
    subject = 'Order Confirmation'
    message = f'Thank you for your order, {first_name}! Your order number is {order.order_number}. Your order is being processed'
    from_email = 'Aroratextiles.net@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)





from .models import FrontCanva, BackCanva





import base64
from django.core.files.base import ContentFile
from django.utils import timezone
from django.contrib.auth import get_user_model

def create_canvas_object(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('cloth_quantity', 1))
        color = request.POST.get('color')
        size = request.POST.get('size')
        data = json.loads(request.body)

        # Convert front and back image data URLs to ImageFields
        format, imgstr = data['front_image_data_url'].split(';base64,')
        ext = format.split('/')[-1]
        front_image = ContentFile(base64.b64decode(imgstr), name='front.' + ext)

        format, imgstr = data['back_image_data_url'].split(';base64,')
        ext = format.split('/')[-1]
        back_image = ContentFile(base64.b64decode(imgstr), name='back.' + ext)

        # Create a CanvasObject for the front canvas
        front_canvas = FrontCanva(
            image=front_image,
            url=data['front_image_data_url'],  # Save the data URL
        )
        front_canvas.save()

        # Create a CanvasObject for the back canvas
        back_canvas = BackCanva(
            image=back_image,
            url=data['back_image_data_url'],  # Save the data URL
        )
        back_canvas.save()

        # Get the user
        User = get_user_model()
        try:
            user = User.objects.get(username=request.user.username)
            product_name = f"{user.username}'s Custom Product"
        except User.DoesNotExist:
            product_name = "Customized Product"

        # Create a new Product
        customized_product = Product(
            product_name=product_name,
            price=499.98,
            FrontCanva=front_canvas,
            BackCanva=back_canvas,
            customized=True,
            pub_date=timezone.now(),
            # Add other fields as necessary
        )
        customized_product.save()

        
        # Return the id of the customized product
        return JsonResponse({'product_id': customized_product.id})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




def index(request):
    # Get the list of recently viewed product IDs from the session
    recently_viewed_product_ids = request.session.get('recently_viewed_products', [])

    # Get the Product objects for the recently viewed products
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed_product_ids)

    # Get all products
    products = Product.objects.all()[:10]

    # Render the template with the products and recently viewed products
    return render(request, 'index.html', {
        'products': products,
        'recently_viewed_products': recently_viewed_products,
    })


def product_detail(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = cart_item.objects.get_or_create(
            cart=request.cart,
            product=product,
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart_detail')
    # Get the product
    else:

        """
        try:
            # retrieve the CartItem objects for the anonymous user's cart
            CartItems = CartItem.objects.filter(cart=cart)
        except:
            CartItems = []
        """
        product = get_object_or_404(Product, id=product_id)


        # Add the product ID to the list of recently viewed products in the session
        recently_viewed_product_ids = request.session.get('recently_viewed_products', [])
        if product_id not in recently_viewed_product_ids:
            recently_viewed_product_ids.append(product_id)
            request.session['recently_viewed_products'] = recently_viewed_product_ids
        images = ProductImage.objects.filter(product=product)
        sizes = ProductSize.objects.filter(product=product)
        colors = ProductColor.objects.filter(product=product)

    # Render the template with the product
    return render(request, 'product.html', {'product': product, 'images': images, 'sizes': sizes, 'colors': colors})





from django.http import JsonResponse

def customized_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'PUT':
        # Get the product

        # Check if the product is customized
        if product.customized:
            # Get the data URLs of the front and back images
            front_image_data_url = product.FrontCanva.url
            back_image_data_url = product.BackCanva.url

            # Return a JSON response with the image data URLs
            return JsonResponse({
                'front_image_data_url': front_image_data_url,
                'back_image_data_url': back_image_data_url
            })

    elif request.method == 'GET':
        sizes = ['S', 'M', 'L', 'XL', 'XXL', '3XL']
        colors = ProductColor.objects.filter(product=product)


        return render(request, 'customize2.html', {'product_id': product_id, 'sizes': sizes, 'colors':colors, 'customized': True})




def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            # User has successfully logged in
            # Retrieve session cart
            session_key = request.session.session_key
            if session_key:
                session_cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)
                # Get or create user's Cart object
                cart, created = Cart.objects.get_or_create(user=user)
                # Iterate over session cart items
                for item in CartItem.objects.filter(cart=session_cart):
                    product = item.product
                    quantity = item.quantity
                    size = item.size  # Retrieve size from session cart item
                    color = item.color  # Retrieve color from session cart item
                    # Check if CartItem already exists for given product and cart
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                    if created:
                        # CartItem did not exist, set its quantity, size, and color
                        cart_item.quantity = int(quantity)
                        cart_item.size = size  # Assign size to CartItem object
                        cart_item.color = color  # Assign color to CartItem object
                        cart_item.save()
                    else:
                        # CartItem already exists, check if it has been customized
                        if not cart_item.customized:
                            # Increase its quantity and update its size and color
                            cart_item.quantity += int(quantity)
                            cart_item.size = size  # Update size of CartItem object
                            cart_item.color = color  # Update color of CartItem object
                            cart_item.save()
                # Clear session cart
                CartItem.objects.filter(cart=session_cart).delete()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid email/phone and/or password."},
            )
    else:
        return render(request, "login.html")



# A view function that displays the register form and handles the registration
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        # Get form data from POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        
        # Check if user already exists
        if MyUser.objects.filter(username=email).exists():
            messages.error(request, "An account with this email address already exists. Please log in instead.")
            return HttpResponseRedirect(reverse("login"))
        
        # Create user
        user = MyUser.objects.create_user(first_name=first_name, phone=phone_number, username=email, last_name=last_name, email=email, password=password)
        
        # Copy cart items from session cart to user cart
        session_key = request.session.session_key
        if session_key:
            session_cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)
            cart, created = Cart.objects.get_or_create(user=user)
            for item in CartItem.objects.filter(cart=session_cart):
                product = item.product
                quantity = item.quantity
                size = item.size  # Retrieve size from session cart item
                color = item.color  # Retrieve color from session cart item
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = int(quantity)
                    cart_item.size = size  # Assign size to CartItem object
                    cart_item.color = color  # Assign color to CartItem object
                    cart_item.save()
                else:
                    if not cart_item.customized:
                        cart_item.quantity += int(quantity)
                        cart_item.size = size  # Update size of CartItem object
                        cart_item.color = color  # Update color of CartItem object
                        cart_item.save()
            CartItem.objects.filter(cart=session_cart).delete()
        
        # Log in user and redirect to index page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def cart(request):
    if request.method == "GET":
        existing_options = [
        {'value': 1, 'label': '1'},
        {'value': 2, 'label': '2'},
        {'value': 3, 'label': '3'},
        {'value': 4, 'label': '4'},
        {'value': 5, 'label': '5'},
        {'value': 6, 'label': '6'},
        {'value': 7, 'label': '7'},
        {'value': 8, 'label': '8'},
        {'value': 9, 'label': '9'},
        {'value': 10, 'label': '10'},
        ]

        
    if request.user.is_authenticated:
        # Handle authenticated user
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # Handle the case where the cart does not exist
            cart = Cart.objects.create(user=request.user)
        CartItems = CartItem.objects.filter(cart=cart)
        discount = cart.discount

        # check if authenticated user has applied a promo code
        if cart.coupon:
            promo_code = cart.coupon.code
        else:
            promo_code = False
        context = {'promocode': promo_code, 'existing_options': existing_options,
                   'cart': CartItems, 'user_cart': cart, 'discount': discount}
    else:
        # Handle anonymous user
        # create or retrieve a Cart object for anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

        # retrieve the CartItem objects for the anonymous user's cart
        CartItems = CartItem.objects.filter(cart=cart)
        discount = cart.discount

        # check if anonymous user has applied a promo code
        if cart.coupon:
            promo_code = cart.coupon.code
        else:
            promo_code = False
        context = {'promocode': promo_code, 'existing_options': existing_options,
                   'cart': CartItems, 'user_cart': cart, 'discount': discount}

    return render(request, 'cart.html', context)


def checkout(request):
    if request.method == 'POST':
        # Get the form data
        email = request.POST['email']
        payment_method = request.POST['payment_method']
        address_id = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        if payment_method == "COD":
            fees = 12
        else:
            fees = 0
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the user and cart information
            user = request.user
            cart = Cart.objects.get(user=user)

            # Create a new Order instance for the authenticated user
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                coupon=cart.coupon,
                address=request.POST['address'],
                city=request.POST['city'],
                governorate = request.POST['governorate'],
                payment_method=payment_method,
                shipping_cost=cart.shipping_cost,
                final_price=cart.final_price + fees  # Set the final price of the order to the final price of the cart
            )

            # Create OrderItem instances for each item in the cart
            for item in CartItem.objects.filter(cart=cart):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    customized=item.customized,
                                        size = item.size,
                    color = item.color,
                )

            # Save the order
            order.save()

            # Clear the cart for authenticated users
            CartItem.objects.filter(cart=cart).delete()
            cart.coupon = None
            cart.save()
        else:
            # Handle anonymous user
            # create or retrieve a Cart object for anonymous users
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

            # Create a new Order instance for the anonymous user without setting the user field
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=request.POST['address'],
                phone=phone,
                city=request.POST['city'],
                governorate = request.POST['governorate'],
                payment_method=payment_method,
                shipping_cost=cart.shipping_cost,
                final_price=cart.final_price + fees  # Set the final price of the order to the final price of the anonymous cart
            )

            # Create OrderItem instances for each item in the anonymous cart
            for item in CartItem.objects.filter(cart=cart):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    size = item.size,
                    color = item.color,
                    customized=item.customized
                )

            # Save the order
            order.save()

            # Clear the cart for anonymous users
            CartItem.objects.filter(cart=cart).delete()
            cart.coupon = None
            cart.save()

        # Redirect to the order confirmation page
        send_order_confirmation_email(first_name, email, order)
        return render(request, 'orderconfirm.html', {"order_number": order.order_number, "email":email})
    else:
        governorates = GOVERNORATE_CHOICES
        
        if request.user.is_authenticated:
            # Handle authenticated user
            cart = Cart.objects.get(user=request.user)
            CartItems = CartItem.objects.filter(cart=cart)
            if float(cart.total_price) > 500:
                cart.shipping_cost = 0
                cart.save()
            try:
                # Try to get the last order made by the user
                last_order = Order.objects.filter(user=request.user).latest('id')
                address = last_order.address
                city = last_order.city
                last_governorate = last_order.governorate
            except Order.DoesNotExist:
                # Handle case when the user has not made any orders
                address = 'Street Address'
                city = 'eg. Maadi'
                last_governorate = None
            context = {'cart': CartItems, 'user_cart': cart,'last_governorate': last_governorate, 'city': city, 'address':address, 'governorates': governorates}

        else:
            # Handle anonymous user
            # create or retrieve a Cart object for anonymous users
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

            # retrieve the CartItem objects for the anonymous user's cart
            CartItems = CartItem.objects.filter(cart=cart)
            if float(cart.total_price) > 500:
                cart.shipping_cost = 0
                cart.save()
            address = 'Street Address'
            city = 'eg. Maadi'
            last_governorate = None
            context = {'cart': CartItems, 'user_cart': cart,'last_governorate': last_governorate, 'city': city, 'address':address, 'governorates': governorates}

        return render(request, 'checkout.html', context)
        

    




#@require_http_methods(["POST", "PUT"])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET' or request.method == 'POST':
        print("post")
        quantity = int(request.POST.get('cloth_quantity', 1))
        color = request.POST.get('color')
        print(color)
        size = request.POST.get('size')
        print(size)
        # create or retrieve a Cart object for both authenticated and anonymous users
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

        # create or retrieve a CartItem object for the specified product, color, and size
        a_cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                              product=product, color=color,
                                                              size=size)

        if not created:
            a_cart_item.quantity += quantity
        else:
            a_cart_item.quantity = quantity
        a_cart_item.save()

        return redirect('cart')

    elif request.method == 'PUT':
        print("put")
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        Product_size = ProductSize.objects.filter(product=product)
        Product_color = ProductColor.objects.filter(product=product)
        color = data.get('color', Product_color[0].color)
        size = data.get('size', Product_size[0].size)
        # create or retrieve a Cart object for both authenticated and anonymous users
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

        # create or retrieve a CartItem object for the specified product, color, and size
        a_cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                              product=product, color=color,
                                                              size=size)

        if created:
            # if the cart item was created (i.e. the product was not already in the cart), set the quantity to 1
            a_cart_item.quantity = 1
        else:
            if quantity == 0:
                a_cart_item.quantity += 1
            else:
                a_cart_item.quantity = quantity
        a_cart_item.save()
        total = a_cart_item.total
        total_price = cart.total_price
        total_price_before_discount = cart.total_price_before_discount

        # calculate discount
        discount = float(total_price_before_discount) - float(total_price)

        return JsonResponse({'success': True,'cart_total': total_price, 'total': "{:.2f}".format(total),
                              'discount': "{:.2f}".format(discount), 'cart_total_before_discount': total_price_before_discount, 'product_name': product.product_name})








def profile(request):
    return render(request, 'profile.html')


#Unmaitained

def remove_from_cart(request, product_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        color = data.get('color')
        size = data.get('size')

        
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            # Handle authenticated user
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart, product=product, color=color, size=size).delete()
            cart_total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
            discount = float(total_price_before_discount) - float(cart_total_price)
        else:
            # Handle anonymous user
            # create or retrieve a Cart object for anonymous users
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

            # delete the specified CartItem object for the anonymous user's cart
            CartItem.objects.filter(cart=cart, product=product, color=color, size=size).delete()
            cart_total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
            discount = float(total_price_before_discount) - float(cart_total_price)

        return JsonResponse({'cart_total': cart_total_price,'discount': "{:.2f}".format(discount), 'cart_total_before_discount': total_price_before_discount})

    else:
        # Handle other request methods (e.g. GET) as before
        ...

#Unmaintained
def edit_profile(request):
    return render(request, 'edit_profile.html')

def change_password(request):
    return render(request, 'change_password.html')




@require_http_methods(["PUT"])
def apply_coupon(request):
    data = json.loads(request.body)
    promo_code = data.get('promo_code')
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)

    
    promo = PromoCode.objects.filter(code=promo_code).first()
    if promo:
        if request.user.is_authenticated:
            # check if code is already applied
            if cart.applied_coupons.filter(code=promo_code).exists():
                return JsonResponse({'error': 'You have already applied this code before'}, status=400)
            if cart.coupon and cart.coupon.code == promo_code:
                return JsonResponse({'error': 'Code already applied'}, status=400)
            
            # remove old coupon if applied
            if cart.coupon:
                cart.coupon = None
            
            # apply the new promo code
            cart.coupon = promo
            cart.applied_coupons.add(promo)
            cart.save()
            
            # recalculate cart total with discount applied
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount

        
        # calculate discount
        discount = float(total_price_before_discount) - float(total_price)

        return JsonResponse({'error': False, 'cart_total': total_price, 'discount': "{:.2f}".format(discount)})
    else:
        return JsonResponse({'error': 'Invalid promo code'}, status=400)
    
@require_http_methods(["PUT"])
def remove_coupon(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        # remove coupon if applied
        if cart.coupon:
            cart.applied_coupons.remove(cart.coupon)

            cart.coupon = None

            cart.save()
            
            # recalculate cart total with discount removed
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
    
    return JsonResponse({'error': False, 'cart_total': total_price})


def orders(request):
    # User is viewing their order history
    if request.user.is_authenticated:
        # Get the orders for the authenticated user
        orders = Order.objects.filter(user=request.user)
    else:
        orders = []
    if request.method == 'POST':
        
        # User is looking up an order using an order number
        order_number = request.POST.get('order_number')
        try:
            # Try to get the order with the given order number
            order = Order.objects.get(order_number=order_number)
            # Return the order details page
            # Calculate the width of each progress bar segment
            segment_width = 100 / order.items.count()
            return render(request, 'order.html', {'order': order, 'orders': orders, 'segment_width': segment_width})
        except Order.DoesNotExist:
            # Order with the given order number does not exist
            # Display an error message
            messages.error(request, 'Order not found.')

    return render(request, 'order.html', {'orders': orders})



def customize(request):
    sizes = ['S', 'M', 'L', 'XL', 'XXL', '3XL']
    product = Product.objects.first()
    if product is None:
        return JsonResponse({'error': 'No product found'}, status=404)
    colors = ProductColor.objects.filter(product=product)
    return render(request, 'customize2.html',{'sizes': sizes, 'colors':colors})



@require_http_methods(["PUT"])
def update_images(request, product_id):
    if request.method == 'PUT':
        # Get the selected color from the request body
        data = json.loads(request.body)
        selected_color = data.get('color')

        # Get the images with the selected color for the specified product
        images = ProductImage.objects.filter(product_id=product_id, color=selected_color)

        # Serialize the images and return them as a JSON response
        images_data = [{'path': image.path} for image in images]
        return JsonResponse({'images': images_data})


@require_http_methods(["PUT"])
def add_to_favorites(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        # Add the product to the authenticated user's favorites
        profile = MyUser.objects.get(email =request.user.email)
        profile.favorites.add(product)
    else:
        # Add the product to the anonymous user's session-based favorites
        favorites = request.session.get('favorites', [])
        favorites.append(product_id)
        request.session['favorites'] = favorites
    return JsonResponse({'product_name': product.product_name})


@require_http_methods(["PUT"])
def remove_from_favorites(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    if request.user.is_authenticated:
        # Remove the product from the authenticated user's favorites
        profile = MyUser.objects.get(email =request.user.email)
        profile.favorites.remove(product_id)
    else:
        # Remove the product from the anonymous user's session-based favorites
        favorites = request.session.get('favorites', [])
        if product_id in favorites:
            favorites.remove(product_id)
            request.session['favorites'] = favorites
    return JsonResponse({'status': 'success'})

def favorites(request):
    if request.user.is_authenticated:
        # Get the favorite products for the authenticated user
        profile = MyUser.objects.get(email =request.user.email)
        
        favorite_products = profile.favorites.all()
    else:
        # Get the favorite products for the anonymous user
        favorite_product_ids = request.session.get('favorites', [])
        favorite_products = Product.objects.filter(pk__in=favorite_product_ids)

    context = {'favorites': favorite_products}
    return render(request, 'favorites.html', context)