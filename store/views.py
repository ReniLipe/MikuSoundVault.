# pyrefly: ignore [missing-import]
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import DetailView
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import ProductForm

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:8]
    return render(request, 'store/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def product_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'store/product_list.html', {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
    })

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(available=True)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart_detail.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, "Prodotto esaurito!")
        return redirect('product_detail', slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{product.name} aggiunto al carrello.")
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    item.delete()
    return redirect('cart_detail')

@login_required
@transaction.atomic
def checkout(request):
    cart = get_object_or_404(Cart, customer=request.user)
    items = cart.items.all()
    
    if not items:
        messages.error(request, "Il carrello è vuoto.")
        return redirect('product_list')
    
    # Verifica stock
    for item in items:
        if item.product.stock < item.quantity:
            messages.error(request, f"Stock insufficiente per {item.product.name}.")
            return redirect('cart_detail')
    
    # Crea ordine
    total = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(customer=request.user, total_price=total)
    
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # Sottrai dal magazzino
        item.product.stock -= item.quantity
        item.product.save()
    
    # Svuota carrello
    items.delete()
    
    messages.success(request, f"Ordine #{order.id} effettuato con successo!")
    return render(request, 'store/order_success.html', {'order': order})

# GESTIONALE ADMIN
def is_admin(user):
    return user.is_authenticated and user.role == 'manager'

@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/admin_orders.html', {'orders': orders})

@user_passes_test(is_admin)
def admin_inventory(request):
    products = Product.objects.all().order_by('category', 'name')
    return render(request, 'store/admin_inventory.html', {'products': products})

@user_passes_test(is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f"Stato ordine #{order.id} aggiornato.")
    return redirect('admin_orders')

# --- 1. MIXIN PER I PERMESSI DEL MANAGER ---
class ManagerRequiredMixin(UserPassesTestMixin):
    """
    Verifica che l'utente sia un manager.
    Se è un cliente normale, mostra un messaggio di errore e lo reindirizza.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'manager'

    def handle_no_permission(self):
        # Soddisfa il requisito del feedback chiaro per permessi mancanti
        messages.error(self.request, "Accesso negato: area riservata agli Store Manager.")
        return redirect('home')


# --- 2. VISTE CRUD PER IL PRODOTTO ---

class ProductCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm  # Usiamo il form con la tendina
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_inventory')

    def form_valid(self, form):
        messages.success(self.request, "Prodotto creato con successo!")
        return super().form_valid(form)

class ProductUpdateView(ManagerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm  # Usiamo il form con la tendina
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('admin_inventory')

    def form_valid(self, form):
        messages.success(self.request, "Prodotto aggiornato con successo!")
        return super().form_valid(form)

class ProductDeleteView(ManagerRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('admin_inventory')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Prodotto eliminato definitivamente.")
        return super().delete(request, *args, **kwargs)