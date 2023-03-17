import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import RoomMessage, ChatRoom, ChatUser


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = RoomMessage.get_20_messages(data['room_id'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_messages(content)


    def new_message(self, data):

        message = data['message']
        username = data['username']
        room_id = data['room_id']
        author_user = ChatUser.objects.filter(username=username)[0] # must be a "ChatUser" instance[0]"<QuerySet [<ChatUser: user1>]>"

        message_from_db = RoomMessage.objects.create(room=ChatRoom(id=room_id), sender=author_user, body=message)

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message_from_db)}

        return self.send_message_to_group(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self, message):
        return {
            'sender': message.sender.username,
            'body': message.body,
            'published': (message.published).timestamp()
        }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)


    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    # from db send messages to WebSocket
    def send_messages(self, messages):
        self.send(text_data=json.dumps(messages))


        # send message to room group
    def send_message_to_group(self, data):
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat_message',
            'message': data,
        })


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # send message to WebSocket
        self.send(text_data=json.dumps(message))

        