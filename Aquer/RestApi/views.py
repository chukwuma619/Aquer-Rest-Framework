from rest_framework import status
from .models import User, Category, Product
from .serializers import UserSerializers, LoginSerializer, ProductSerializer, CategorySerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser



# Create your views here.
class CategoryList(APIView):
    
    """
    List all snippets, or create a new category
    """

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    """
    Retrieve, update or delete a category instance.
    """

    def get(self, request, pk, format=None):
        categories = Category.objects.all()
        category = get_object_or_404(categories, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        categories = Category.objects.all()
        category = get_object_or_404(categories, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):

    """
    List all Users
    """
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data)


class UserDetails(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def get(self, request, pk, format=None):
        users = User.objects.all()
        user = get_object_or_404(users, pk=pk)
        serializer = UserSerializers(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        users = User.objects.all()
        user = get_object_or_404(users, pk=pk)
        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        users = User.objects.all()
        user = get_object_or_404(users, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostProduct(APIView):
    permission_classes = [IsAdminUser|IsAuthenticated] 
    parser_classes = [FormParser, MultiPartParser]   
    def post(self, request, format=None):
        serializer = ProductSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):
    permission_classes = [IsAuthenticated|IsAdminUser]
    parser_classes = [FormParser, MultiPartParser]
    def get(self, request, pk, format=None):
        products = Product.objects.all()
        product = get_object_or_404(products, pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        products = Product.objects.all()
        product = get_object_or_404(products, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk , format=None):
        products = Product.objects.all()
        product = get_object_or_404(products, pk=pk)
        serializer = ProductSerializer(product)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistration(APIView):
    permission_classes = [~IsAuthenticated]
    def post(self, request, format=None):
        print(request.data)
        serializer = UserSerializers(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serialized_user = serializer.save()
            user = authenticate(
                username= serialized_user.username,
                password = request.data.get('password')
                )
            
            if user is not None:
                login(request, user)
            return Response({'message': 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serialized_user = serializer.save()
            user = authenticate(
                username=serialized_user.validated_data['username'],
                password = serialized_user.validated_data['password']
                )
            if user is not None:
                login(request, user)
                return Response({'message': 'login successful', 
                                 'user': request.user}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutUser(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'logout successful'}, status=status.HTTP_202_ACCEPTED)
