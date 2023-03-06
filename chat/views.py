from exchange import serializers
from exchange.lib import request_client
from django.shortcuts import render
from django.contrib.auth import get_user_model

from exchange.models import LevelFee
from .models import (
    ChatSession, ChatSessionMessage, deserialize_user
)
from exchange.serializers import AdminChatSerializer, LevelFeeSerializer
from rest_framework import status
from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

class ChatSessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        if not 'email' in request.data:
            user = request.user
        else: 
            email= request.data['email']
        if not 'email' in request.data:
            chats =  ChatSession.objects.filter(owner = request.user)
        else:
            chats =  ChatSession.objects.filter(email = email)
        for item in chats :
            item.delete()
        if not 'email' in request.data:
            chat_session = ChatSession.objects.create(owner=user)
        else:
            chat_session = ChatSession.objects.create(email=email)
        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })
    
    def patch(self, request, *args, **kwargs):
        """Add a user to a chat session."""
        User = get_user_model()
        print(kwargs['uri'])
        uri = kwargs['uri']
        username = request.user.username
        user = User.objects.get(username=username)

        chat_session = ChatSession.objects.get(uri=uri)

        return Response ({
            'status': 'SUCCESS',
        })


class ChatSessionMessageView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json() 
            for chat_session_message in chat_session.messages.all()]
        notseen = 0
        for item in chat_session.messages.all():
            if not item.seen:
                notseen = notseen + 1
        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages, 'notseen' : notseen
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']
        if not 'email' in request.data:
            user = request.user
        else: 
            email= request.data['email']
        chat_session = ChatSession.objects.get(uri=uri)
            
        if not 'email' in request.data:
            if request.user.is_staff:
                ChatSessionMessage.objects.create(
                    user=user, chat_session=chat_session, message=message, aseen=True
                )
            else:
                ChatSessionMessage.objects.create(
                    user=user, chat_session=chat_session, message=message, seen=True
                )
        else:
            ChatSessionMessage.objects.create(
                email=email, chat_session=chat_session, message=message, seen=True
            )
        if not 'email' in request.data:
            return Response ({
                'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
                'user': deserialize_user(user)
            })
        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
            'user': email
        })

class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        if 'email' in request.data :
            user = ChatSession.objects.get(email = request.data['email'])
            return Response({'uri' : user.uri , 'username' : user.email})
        else :
            if request.user.is_authenticated:
                if not ChatSession.objects.filter(owner = request.user):
                    return Response({'data': 'not found'}, status=status.HTTP_404_NOT_FOUND)
                user = ChatSession.objects.get(owner = request.user)
                return Response({'uri' : user.uri , 'username' : request.user.username})
            return Response({'uri' : 0})

class seen(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    def get(self, request, uri, *args, **kwargs):
        if request.user.is_staff:
            chat_session = ChatSession.objects.get(uri=uri)
            messages = chat_session.messages.all()
            for item in messages:
                item.aseen = True
                item.save()
            return Response(True)
        chat_session = ChatSession.objects.get(uri=uri)
        messages = chat_session.messages.all()
        for item in messages:
            item.seen = True
            item.save()
        return Response(True)

class adminchat(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        user = ChatSession.objects.all()
        serializer = AdminChatSerializer(user , many=True)
        return Response(serializer.data)


