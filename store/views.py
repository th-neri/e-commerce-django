from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet # ReadOnlyModelViewSet(only to read, cannot create, update or delete)
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

# PRODUCT CLASSES
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        # to get products of a specific collection
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # applied a filter so i can only see the reviews of the product i selected
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # to provide aditional data to the serializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
