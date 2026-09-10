from django.urls import path
from rest_framework_nested import routers
from . import views

# the basenames are to generate the name of the views(products-list, products-detail)
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.urls

# the product lookup is the product_pk extracted from the ReviewViewSet get_queryset and to access the review products/<id>/reviews
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')

# the cart lookup is the cart_pk extracted from the CartItemViewSet get_queryset and to access carts/<id>/items
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls