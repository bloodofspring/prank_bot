from client_handlers.base import *


class Start(BaseHandler):
    FILTER = command("start")

    async def func(self, client: Client, request: request_type):
        await request.reply("start message")

        if not self.de_database.config[0].is_authorized:
            await request.reply("subscribe to this channels!")
            await request.reply("links: https://t.me/")

            return

        await request.reply("main and help")
