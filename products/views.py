from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

def home(request):
    products = Product.objects.all().order_by('-votes_total')
    return render(request, 'products/home.html', {'products': products})

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['title']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # pk is primary key
    return render(request, 'products/detail.html', {'product': product})

@login_required
def upvote(request, product_id):
    if request.method == 'POST':
        # check the existanse of vote
        user_id = request.user.id
        product = get_object_or_404(Product, pk=product_id)
        if user_id in product.voters.all():
            pass
        else:
            product.voters.add(request.user)
            product.votes_total += 1
            product.save()
        return redirect('/products/' + str(product_id))

@login_required
def delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.hunter:
        return redirect('/products/' + str(product_id))
    if request.method == 'POST':
        if product is not None:
            product.delete()
        return redirect('home')

@login_required
def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user != product.hunter:
        return redirect('/products/' + str(product_id))
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url']:
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            if request.FILES.get('icon'):
                product.icon = request.FILES['icon']
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'products/edit.html', {'product': product})