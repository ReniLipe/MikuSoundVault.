from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # GESTIONALE ADMIN / MANAGER
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin-orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),

    # ROTTE CRUD PER I PRODOTTI
    path('admin-inventory/product/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('admin-inventory/product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('admin-inventory/product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]