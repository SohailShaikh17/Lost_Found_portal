from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, ProfileForm, ItemForm, ClaimForm
from .models import Item, Category, ClaimRequest
from .utils import get_matching_items

def home(request):
    recent_items = Item.objects.select_related('category','user')[:6]
    return render(request, 'portal/home.html', {'recent_items': recent_items})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('dashboard')
    return render(request, 'portal/register.html', {'form': form})

@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Profile updated.')
        return redirect('profile')
    return render(request, 'portal/profile.html', {'form': form})

@login_required
def dashboard(request):
    my_items = Item.objects.filter(user=request.user)
    incoming_claims = ClaimRequest.objects.filter(item__user=request.user)
    my_claims = ClaimRequest.objects.filter(claimant=request.user)
    return render(request, 'portal/dashboard.html', locals())

def item_list(request):
    items = Item.objects.select_related('category','user').all()
    q = request.GET.get('q','')
    item_type = request.GET.get('type','')
    category = request.GET.get('category','')
    location = request.GET.get('location','')
    if q: items = items.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(location__icontains=q))
    if item_type: items = items.filter(item_type=item_type)
    if category: items = items.filter(category_id=category)
    if location: items = items.filter(location__icontains=location)
    categories = Category.objects.all()
    return render(request, 'portal/item_list.html', {'items': items, 'categories': categories})

@login_required
def item_create(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False); item.user = request.user; item.save()
        messages.success(request, 'Item posted successfully.')
        return redirect(item)
    return render(request, 'portal/item_form.html', {'form': form, 'title': 'Post Item'})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    opposite_type = 'FOUND' if item.item_type == 'LOST' else 'LOST'
    suggestions = get_matching_items(item, Item.objects.filter(item_type=opposite_type).exclude(pk=item.pk))
    already_claimed = request.user.is_authenticated and ClaimRequest.objects.filter(item=item, claimant=request.user).exists()
    return render(request, 'portal/item_detail.html', {'item': item, 'suggestions': suggestions, 'already_claimed': already_claimed})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Item updated.')
        return redirect(item)
    return render(request, 'portal/item_form.html', {'form': form, 'title': 'Edit Item'})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete(); messages.success(request, 'Item deleted.')
        return redirect('dashboard')
    return render(request, 'portal/item_delete_confirm.html', {'item': item})

@login_required
def claim_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user == request.user:
        messages.error(request, 'You cannot claim your own item.')
        return redirect(item)
    form = ClaimForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        claim = form.save(commit=False); claim.item = item; claim.claimant = request.user
        try:
            claim.save(); messages.success(request, 'Claim request submitted.')
        except Exception:
            messages.error(request, 'You already submitted a claim for this item.')
        return redirect(item)
    return render(request, 'portal/claim_form.html', {'form': form, 'item': item})

@login_required
def manage_claim(request, claim_id, action):
    claim = get_object_or_404(ClaimRequest, id=claim_id, item__user=request.user)
    if action == 'approve':
        claim.status = 'APPROVED'
        claim.item.status = 'CLAIMED'
        claim.item.save()
    elif action == 'reject':
        claim.status = 'REJECTED'
    claim.save()
    messages.success(request, f'Claim {action}d.')
    return redirect('dashboard')
