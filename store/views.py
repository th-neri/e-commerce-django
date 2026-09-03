from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet # ReadOnlyModelViewSet(only to read, cannot create, update or delete)
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework import status
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination

# PRODUCT CLASSES
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter # to get products of a specific collection or price
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']  # to search specific fielders
    ordering_fields = ['unit_price', 'last_update'] # to order products using ascending or descending

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error: Product cannot be deleted because it is associated with an order item'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# COLLECTION CLASSES
class CollectionViewSet(ModelViewSet):
    # annotating the collection and sending to the queryset
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
             return Response({'error: Collection cannot be deleted because it is associated with products'}, 
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)       
        return super().destroy(request, *args, **kwargs)

# REVIEW CLASS
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # applied a filter so i can only see the reviews of the product i selected
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # to provide aditional data to the serializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    # applied a filter so i can only see the items of the cart i selected
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    # to add a product to the cart
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    

