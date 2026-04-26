from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from base.models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        
        'GET /api/messages',
        'GET /api/message/:id',
        'POST /api/create-message/:room_id',
        'DELETE /api/message_id/delete-message'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    search = request.GET.get('search', '')
    topic = request.GET.get('topic', '')
    
    rooms = Room.objects.filter(
        Q(name__icontains=search) |
        Q(topic__name__icontains=search)
    )
    
    if topic:
        rooms = rooms.filter(topic__name__icontains=topic)
    
    serializer = RoomSerializer(rooms, many=True)
    data = {
        "count": rooms.count(),
        "rooms": serializer.data
    }
    return Response(data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMessage(request, id):
    message = Message.objects.get(id=id)
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createMessage(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    
    if not request.user.is_authenticated:
        return Response("Auth Required")
    
    data = {
        'user': user.id,
        'room': room.id,
        'body': request.data.get('body')
    }
    serializer = MessageSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteMessage(request, message_id):
    message = Message.objects.get(id=message_id)
    user = request.user
    
    if not request.user.is_authenticated:
        return Response("Auth Required")
    
    message.delete()
    return Response("message deleted")