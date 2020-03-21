from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Vote
from django.utils import timezone

def home(request):
    products = Product.objects.all().order_by('-votes_total')
    # packing products and voted
    voted = []
    for product in products:
        if Vote.exists(product_id=product.id, user_id=request.user.id):
            voted.append(True)
        else:
            voted.append(False)
    products_and_voted = []
    for i in range(len(products)):
        products_and_voted.append({
            'product': products[i],
            'voted': voted[i],
        })
    return render(request, 'products/home.html', {'products_and_voted': products_and_voted})

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
    exists_vote = Vote.exists(product_id=product_id, user_id=request.user.id)
    return render(request, 'products/detail.html', {'product': product, 'exists_vote': exists_vote})

@login_required
def upvote(request, product_id):
    if request.method == 'POST':
        # check the existanse of vote
        user_id = request.user.id
        try:
            vote = Vote.objects.get(product_id=product_id, user_id=user_id)
            pass
        except Vote.DoesNotExist:
            # make vote
            vote = Vote()
            vote.product_id = product_id
            vote.user_id = user_id
            vote.save()
            product = get_object_or_404(Product, pk=product_id)
            product.votes_total += 1
            product.save()
        return redirect('/products/' + str(product_id))