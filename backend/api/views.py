from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Q

from api.models import User, ChatMessage, Profile

from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer, ChatMessageSerializer, ProfileSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() 
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    
@api_view(['GET'])
def getRoutes(request): 
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
    ]
    return Response(routes)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET': 
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST': 
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}' 
        return Response({'response': data}, status=status.HTTP_200_OK)
    
    return Response({''}, status=status.HTTP_400_BAD_REQUEST)




class MyInbox(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        
        message = ChatMessage.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__reciever = user_id) | Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id) | Q(reciever=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id',flat=True) 
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
        
        return message
    
class GetMessages(generics.ListAPIView): 
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id],
                                               reciever__in=[sender_id, reciever_id])
        return messages
    
class SendMessages(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    
class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
        
    
# Search User 
class SearchUser(generics.ListAPIView): 
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all() 
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs): 
        username = self.kwargs['username']
        logged_in_user = self.request.user 
        users = Profile.objects.filter(
            Q(user__username__icontains=username) | Q(full_name__icontains=username) | Q(user__email__icontains=username) & ~Q(user=logged_in_user)
        )
        
        if not users.exists(): 
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
        