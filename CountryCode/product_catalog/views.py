from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import ProductSerializer
from django.db.models import F
from django.db.models import Q 



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        print(request,"search")
        query = request.query_params.get('q', '')
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )
        print(products,"productsproductsproductsproductsproductsproductsproductsproductsproductsproductsproductsproducts")
        serializer = self.get_serializer(products, many=True)
        if serializer is None:
            return Response(serializer.data)
        else:
            return Response({'error': f'No data found with  {query}  this keywords'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        print(request,"search")
        products = Product.objects.all()
        print(products,"product listing >>>>>>")
        serializer = ProductSerializer(products, many=True)
        if serializer is None:
            return Response(serializer.data)
        else:
            return Response({'error': f'No data found'}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['post'])
    def create_product(self, request):
        print("Request Data:", request.data)
        data = request.data.copy()
        category_id = data.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                print(category.id,"categorycategory")
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the category to the dataaaaaaaa
        data['category'] = category.id  
        serializer = ProductSerializer(data=data)
        print("Serializer:", serializer)
        if serializer.is_valid():
            print("Valid Data")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Invalid Data:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['put'])
    def update_products(self, request,pk=None):
        print("Request Data:", request.data)
        product = Product.objects.get(id=pk)
        print("Product:", product)
        serializer = ProductSerializer(product, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'inventory_count not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def partial_update_product(self, request, pk=None):
        print("Request Data:", request.data)
        product = Product.objects.get(id=pk)
        print("Product:", product)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        product = Product.objects.get(id=pk)
        print("Deleting Product:", product)
        product.delete()
        # Return a response indicating the product was successfully deleted
        return Response({'status': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)