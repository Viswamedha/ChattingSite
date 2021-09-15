from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Room, Message
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../../../../404')
    public_rooms = Room.objects.filter(private = False)
    private_rooms = request.user.private_rooms.all()
    return render(request, 'chat/index.html', {'public_rooms': public_rooms, 'private_rooms': private_rooms})


def room(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../../../../404')
    try:
        room = Room.objects.get(slug = room_name)
        if room.private:
            if request.user not in room.allowed.all():
                return HttpResponseRedirect('../../../../404')
    except:
        return HttpResponseRedirect('../../../../404')
    try:
        messages = Message.objects.filter(room = room)[-100:]
    except:
        messages = Message.objects.filter(room = room)
    return render(request, 'chat/chatroom.html', {
        'room': room,
        'messages': messages
    })



