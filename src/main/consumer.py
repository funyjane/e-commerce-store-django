from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from .models import AbstractBaseListing
from .utils import remove_tags


class AdConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        date = datetime.now()
        await self.send_json(
            content={
                "type": "message",
                "data": {
                    "author": self.scope["user"].username,
                    "color": "green",
                    "time": date.isoformat(),
                    "text": remove_tags(text_data),
                },
            }
        )
        date = datetime.now()
        if text_data[0] == "#":
            search_result = await database_sync_to_async(self.get_ad)(
                name=text_data[1:]
            )
            await self.send_json(
                content={
                    "type": "message",
                    "data": {
                        "author": "Bot",
                        "color": "blue",
                        "time": date.isoformat(),
                        "text": search_result,
                    },
                }
            )

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.send_json(
            content={
                "type": "message",
                "data": "closed",
            }
        )

    def get_ad(self, name):

        ad = AbstractBaseListing.objects.filter(
            title=name
        )  # get current child listing model
        if not ad.exists():
            return "Nothing has been found!"
        if ad[0].sold:
            result = "Sold!"
        local_fields = ad[0]._meta.local_fields[
            1:
        ]  # getting list of local fields in current model
        verbose_names = [model.verbose_name for model in local_fields]
        values = [
            str(ad[0].__getattribute__(item.name)) + "</div>" for item in local_fields
        ]  # getting local fields values
        output = (
            '<div class="d-flex flex-row"><div class="d-flex flex-column">'
            + 'Price: </div><div class="d-flex flex-column">'
            + str(ad[0].price)
            + "</div></div>"
        )
        for verbose_name, value in zip(verbose_names, values):
            output += (
                f'<div class="d-flex flex-row"><div class="d-flex flex-column">{verbose_name}: </div>"'
                + f'<div class="d-flex flex-column">{value}</div></div>'
            )
        return output
