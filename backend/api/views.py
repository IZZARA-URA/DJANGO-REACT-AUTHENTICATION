from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Q

from api.models import User, ChatMessage

from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer, ChatMessageSerializer

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
        
        message = ChatMessage.object.filter(
            id___in = Subquery(
                User.object.filter(
                    Q(sender__reciever = user_id) | Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id) | Q(reciever=OuterRef('id'), sender=user_id)
                        ).order_by('last_msg', flat=True).order_by('_id')
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
        
        return message
    