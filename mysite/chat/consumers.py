import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 방 떠나기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    

    # WebSocket 으로부터 메세지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 방 그룹에게 메세지 보내기
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 그룹에게 메세지 받기
    async def chat_message(self, event):
        message = event['message']

        # WebSocket으로 메세지 보내기
        await self.send(text_data=json.dumps({
            'message': message
        }))