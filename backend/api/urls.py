from rest_framework_simplejwt.views import TokenRefreshView 
from django.urls import path
from . import views

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name='token_obtian_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("test/", views.testEndPoint, name='test'),
    path("", views.getRoutes)
]
