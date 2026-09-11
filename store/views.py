from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet # ReadOnlyModelViewSet(only to read, cannot create, update or delete)
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework import status
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order, ProductImage
from .serializers import (ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, 
                          AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, 
                          CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer
                        )
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission, IsUserSelfPermission

# PRODUCT CLASSES
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().prefetch_related('images').order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter # to get products of a specific collection or price
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']  # to search specific fielders
    ordering_fields = ['unit_price', 'last_update'] # to order products using ascending or descending
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error: Product cannot be deleted because it is associated with an order item'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    # applied a filter to get the product ID from the URL so it only return the images of a particular product
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

    # extracting the product pk(product ID) from URL and using the context i will pass to the serializer 
    # and then the serializer will grab it and use to create a product image object
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# COLLECTION CLASSES
class CollectionViewSet(ModelViewSet):
    # annotating the collection and sending to the queryset
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
             return Response({'error: Collection cannot be deleted because it is associated with products'}, 
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)       
        return super().destroy(request, *args, **kwargs)

# REVIEW CLASS
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# CART CLASS
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
        # to only allow methods i want
        self.http_method_names = ['get', 'post', 'patch', 'delete']

        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            # to update is carts/<cart_id>/items/<product_id>
            return UpdateCartItemSerializer
        return CartItemSerializer

#CUSTOMER CLASS
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser] # only admin users are able to retrieve customer object

    # any user can retrieve customer object but only authenticated or admin users are able to update
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsUserSelfPermission])
    def me(self, request):
        # use request.user.id to check if the user is logged in or not
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

#ORDER CLASS
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # implemented a create method from scratch instead of rely on the create model mixin,
    # so i give the request data, validate the data, save the changes and create another serializer 
    # giving the order object from the save method
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        # first value(customer_id) is the object we reading and second is a boolean 
        # that indicates if the record was created or not
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
