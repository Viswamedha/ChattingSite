from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from .models import *

def all_chats(request):

    context = {}
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../../../../404')
    public_rooms = Room.objects.filter(private = False)
    private_rooms = request.user.private_rooms.all()
    context = {'public_rooms': public_rooms, 'private_rooms': private_rooms}

    return render(request, template_name = 'chat/index.html', context = context)


def room(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../../../../404')
    try:
        room: Room = Room.objects.get(slug = room_name)
        if room.private:
            if request.user not in room.allowed.all():
                return HttpResponseRedirect('../../../../404')
    except:
        return HttpResponseRedirect('../../../../404')
    try:
        messages = Message.objects.filter(room = room)[-100:]
    except:
        messages = Message.objects.filter(room = room)
    return render(request, 'chat/all_chats.html', {
        'room': room,
        'messages': messages
    })


