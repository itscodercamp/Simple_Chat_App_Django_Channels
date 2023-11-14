from django.shortcuts import get_object_or_404, render
from .models import *
from django.shortcuts import HttpResponse

def index(request , group_name):
    print("Group Name : " ,group_name)
    group = get_object_or_404(Groups, group_name=group_name)
    
    # Retrieve associated chat messages
    chats = []
    if group:
        chats = ChatsRoom.objects.filter(group = group)

    else:
        group = Groups(group_name = group_name)
        group.save()

    return render(request, 'index.html', {'group_name' : group_name , 'chats' : chats})