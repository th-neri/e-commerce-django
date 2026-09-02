from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet # ReadOnlyModelViewSet(only to read, cannot create, update or delete)
from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework import status
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter

# PRODUCT CLASSES
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter # to get products of a specific collection or price
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
