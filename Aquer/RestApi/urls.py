from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from RestApi import views
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView


urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetails.as_view()),
    path('products/', views.ProductList.as_view()),
    path('product/post/', views.PostProduct.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),

    path("user/register/", views.UserRegistration.as_view(), name="rest_register"),
    path("user/login/", LoginView.as_view(), name="rest_login"),
    path("user/logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details")

]

urlpatterns = format_suffix_patterns(urlpatterns)

