from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from RestApi import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('user/register/', views.UserRegistration.as_view()),
    path('user/login/', views.UserLogin.as_view()),
    path('user/logout/', views.LogoutUser.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetails.as_view()),
    path('products/', views.ProductList.as_view()),
    path('product/post/', views.PostProduct.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

