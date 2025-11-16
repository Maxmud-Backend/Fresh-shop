from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from shop.forms import RegisterForm, LoginForm
from shop.models import Contact, SubCategory, Category, Product, Like


# Create your views here.
def index(request):
    subcategories = SubCategory.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 8)  # har sahifada 8 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        "title":"Freeshop",
        "subcategories":subcategories,
        "categories":categories,
        "productss":products,
        'page_obj': page_obj,
        'products': page_obj.object_list,
    }
    return render(request,"shop/index.html",context)
from .forms import CommentForm
from .models import Product, Comment
from django.shortcuts import redirect

def Detail(request, pk):
    products = Product.objects.all()
    product = Product.objects.get(pk=pk)
    featured_products = Product.objects.all()
    comments = product.comments.all().order_by('-created_at')
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('Detail', pk=pk)

    context = {
        "title": "Detail",
        "product": product,
        "products": products,
        "featured_products": featured_products,
        "comments": comments,
        "form": form
    }
    return render(request, "shop/detail.html", context)



def Register(request):
    forms = RegisterForm(data=request.POST or None)
    if request.method == "POST":
        if forms.is_valid():
            forms.save()
            return redirect("Login")
    context = {
        "title":"register",
        "forms": forms
    }
    return render(request,"shop/Register.html",context)

def Login(request):
    forms = LoginForm(data=request.POST or None)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email,password=password)
        if user:
            login(request, user)
        return redirect("home")
    context = {
        "title":"Sign in",
        "forms":forms
    }
    return render(request,"shop/Signin.html",context)

def Logout(request):
    logout(request)
    return redirect("Login")

def About(request):

    context = {
        "title":"About Us"
    }
    return render(request,"shop/about.html",context)

def Views_Contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Contact.objects.create(first_name=first_name,email=email,subject=subject,message=message)
    return render(request,"shop/Contact.html")

def Views_Gallery(request):

    context = {
        "title":"Gallery"
    }
    return render(request,"shop/Gallery.html",context)


def Carusel(request):
    context = {
        "title":"Carusel"

    }
    return render(request,"shop/carusel.html",context)

def Views_shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    query = request.GET.get("q")
    if query:
        products = products.filter(title__icontains=query)

    selected_category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if selected_category:
        products = products.filter(category__id=selected_category)


    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'popularity':
        products = products.order_by('-sold')
    else:
        products = products.order_by('-id')
    context = {
        'categories':categories,
        'products': products,
        'query':query,
        "selected_category": selected_category,
        "min_price": min_price,
        "max_price": max_price,
        "sort":sort
    }
    return render(request,"shop/shop.html",context)

def user_like(request, pk):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(pk=pk)
    if user:
        user_products = Like.objects.filter(user=user)
        if product in [like.product for like in user_products]:
            like_product = Like.objects.filter(user=user, product=product)
            like_product.delete()
        else:
            Like.objects.create(user=user, product=product)
    next_page = request.META.get("HTTP_REFERER",'home')
    return redirect(next_page)

def likes(request):
    user = request.user if request.user.is_authenticated else None
    likes = Like.objects.filter(user=user)
    products = [like.product for like in likes]
    context = {
        "products":products
    }
    return render(request,"shop/likes.html",context)


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8)  # har sahifada 8 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
    }
    return render(request, 'shop/index.html', context)

