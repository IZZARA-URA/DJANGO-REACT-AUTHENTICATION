from rest_framework_simplejwt.views import TokenRefreshView 
from django.urls import path
from . import views

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name='token_obtian_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("test/", views.testEndPoint, name='test'),
    path("", views.getRoutes),
    
    # Chat
    path(f"my-messages/<user_id>", views.MyInbox.as_view()),
    path(f"get-messages/<sender_id>/<reciever_id>", views.GetMessages.as_view()),
    path(f"send-messages/", views.SendMessages.as_view()),
    
    # Get / Filter Data 
    path(f"profile/<int:pk>/", views.ProfileDetail.as_view()),
    path(f"search/<username>/", views.SearchUser.as_view())
    
]
