import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
import requests
from django.utils.html import strip_tags
import json

#fungsi helper
def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.all()
    
    #filter berdasarkan tipe produk
    filter_type = request.GET.get("filter", "All-Product")
    if filter_type == "My-Product" and request.user.is_authenticated:
        products = products.filter(user=request.user)
    
    #agar saat diklik apparel, jersey dan jaket ikut terfilter
    CATEGORY_GROUPS = {
        'apparel': ['jersey', 'jaket']
    }

    #filter berdasarkan kategori
    category = request.GET.get("category", "All-Categories")
    if category and category != "All-Categories":
        category = category.strip().lower()
        if category in CATEGORY_GROUPS:
            products = products.filter(category__in=CATEGORY_GROUPS[category])
        else:
            products = products.filter(category=category)

    context = {
        'nama_aplikasi': 'Arabgokstore',
        'nama': 'Muhammad Hafizh',
        'kelas': 'PBP D',
        'product_list': products,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }
    
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

@never_cache
def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'price': product.price,
            'stock': product.stock,
            'rating': product.rating,
            'brand': product.brand,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        for product in product_list
    ]
    resp = JsonResponse(data, safe=False)
    resp['Cache-Control'] = 'no-store'
    return resp

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'price': product.price,
            'stock': product.stock,
            'rating': product.rating,
            'brand': product.brand,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
   
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            redirect_url = reverse('main:login')
            if _is_ajax(request):
                return JsonResponse({"ok": True, "redirect_url": redirect_url}, status=201)

            return HttpResponseRedirect(redirect_url)
        if _is_ajax(request): #invalid
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            redirect_url = reverse("main:show_main")
            if _is_ajax(request):
                resp = JsonResponse({"ok": True, "redirect_url": redirect_url}, status=200)
                resp.set_cookie('last_login', str(datetime.datetime.now()))
                return resp

            response = HttpResponseRedirect(redirect_url)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        if _is_ajax(request): #invalid
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    price = request.POST.get("price")
    stock = request.POST.get("stock")
    brand = request.POST.get("brand")
    user = request.user

    new_product = Product(
        name=name, 
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        price=price,
        stock=stock,
        brand=brand,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def edit_product_entry_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)

    product.name        = request.POST.get("name")
    product.description = request.POST.get("description")
    product.category    = request.POST.get("category")
    product.thumbnail   = request.POST.get("thumbnail")
    product.is_featured = request.POST.get("is_featured") == 'on'
    product.price = request.POST.get("price")
    product.stock = request.POST.get("stock")
    product.brand = request.POST.get("brand")
    product.save()

    data = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "thumbnail": product.thumbnail,
        "is_featured": product.is_featured,
        "price": str(product.price) if product.price is not None else None,
        "stock": product.stock,
        "brand": product.brand,
    }
    
    return JsonResponse(data, status=200)

@csrf_exempt
@require_POST
def delete_product_entry_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "detail": "Unauthorized"}, status=401)

    product = get_object_or_404(Product, pk=id)

    # batasi hanya pemilik yang boleh hapus
    if product.user_id != request.user.id:
        return JsonResponse({"ok": False, "detail": "Forbidden"}, status=403)

    product.delete()
    return JsonResponse({"ok": True, "id": str(id)}, status=200)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        price = data.get("price", 0)
        stock = data.get("stock", 0)
        brand = data.get("brand", "")
        user = request.user
        
        new_product = Product(
            name=name, 
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            price=price,
            stock=stock,
            brand=brand,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@login_required(login_url='/login')
def show_json_my_products(request):
    product_list = Product.objects.filter(user=request.user)
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'product_views': product.product_views,
            'price': product.price,
            'stock': product.stock,
            'rating': product.rating,
            'brand': product.brand,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
        }
        for product in product_list
    ]
    
    return JsonResponse(data, safe=False)