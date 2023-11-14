import json
from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Groups , ChatsRoom


class MySyncConsumer(SyncConsumer):
    group_name = 'default_group'

    def websocket_connect(self , event):
        print("websocket connect" , event)
        print('channel layer',self.channel_layer)
        print('channel name',self.channel_name)
        global group_name # making this variable global to access accross the function
        group_name = self.scope['url_route']['kwargs']['group_name']

        self.group_name = 'chat_' + self.group_name  # Use a unique name for each group

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.send(
            {
                "type" : "websocket.accept"
            }
        )
        
    # def websocket_receive(self , event):
    #     print("websocket receive" , event['text'])
    #     data = json.loads(event['text'])
    #     group = Groups.objects.get(group_name = self.group_name)
    #     chat = ChatsRoom(content = data['message'] , group = group)
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.group_name,{
    #             "type" : "chat.message",
    #             "message" : event['text']
    #         }
    #     )
    def websocket_receive(self, event):
        print("websocket receive", event['text'])
        data = json.loads(event['text'])

        try:
            group = Groups.objects.get(group_name=self.group_name)
        except Groups.DoesNotExist:
            # Handle the case when the group doesn't exist
            print(f"Group '{self.group_name}' does not exist. Creating it.")
            group = Groups(group_name=self.group_name)
            group.save()

        # Create a new ChatsRoom instance and set its fields
        chat = ChatsRoom(content=data['message'], group=group)
        chat.save()  # Save the chat message to the database

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                "type": "chat.message",
                "message": event['text']
            }
        )

    def chat_message(self , event):
        print("chat message" , event)
        self.send(
            {
                "type" : "websocket.send",
                "text" : event['message']
            }
        )

    def websocket_disconnect(self , event):
        print("websocket disconnect" , event)
        print('channel layer',self.channel_layer)
        print('channel name',self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name ,self.channel_name
        )
        raise StopConsumer()