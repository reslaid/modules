from loader import (
    Module
)
import os


class Bloody(Module):
    """Trolling module Bloody for hayes-client"""

    def __init__(self) -> None:
        self.init()
        self.log = self.get_logger()
        self.gTTS = self.req('gtts').gTTS
        self.asyncio = self.req('asyncio', _importlib=True)
        self.random = self.req('random', _importlib=True)
        self.psutil = self.req('psutil', _importlib=True)
        self.platform = self.req('platform', _importlib=True)
        self.socket = self.req('socket', _importlib=True)
        self.aiohttp = self.req('aiohttp', _importlib=True)
        self.aiofiles = self.req('aiofiles', _importlib=True)
        self.datetime = self.req('datetime', _importlib=True)
        self.multiprocessing = self.req('multiprocessing', _importlib=True)

        self.directories: dict = {
            "data": 'bloody/data',
            "media": 'bloody/data/media',
            "cache": 'bloody/data/cache',
            "voice": 'bloody/data/voices',
            "inj": 'bloody/data/inj',
            "message": 'bloody/messages/'
        }

        self.template_file = os.path.join(self.directories["data"], "template.cfg")

        for directory in self.directories.values():
            os.makedirs(directory, exist_ok=True)

        self.video_file: str = os.path.join(self.directories["media"], "video.txt")
        self.photo_file: str = os.path.join(self.directories["media"], "photo.txt")
        self.logo_file: str = os.path.join(self.directories["media"], "logo.txt")

        open(self.video_file, "a").close()
        open(self.photo_file, "a").close()

        self.video_url: str = self.read_media_url(self.video_file)
        self.photo_url: str = self.read_media_url(self.photo_file)

        self.users = []
        self.status: bool = False
        self.delay: float = 0
        self.autorepond_header = ''
        self.mode = 'reply'
        self.old_header = ''
        self.chats = []
        self.chats_photo = []
        self.chats_video = []
        self.chats_typer = []
        self.chats_voice = []
        self.chats_tagger = []

        self.default_photo_url = 'https://telegra.ph/file/3ede6ee4a88ddff5d4b1f.jpg'

        if not os.path.isfile(self.logo_file):
            with open(self.logo_file, 'w') as file:
                file.write(self.default_photo_url)

        self.photo = []

        with open(self.logo_file, 'r') as file:
            for line in file:
                photo_url = line.strip()
                self.photo.append(photo_url)

        self.read_template_config()
        self.shablon_name = self.get_template_name()

        with open(os.path.join(self.directories["message"], self.shablon_name), "r", encoding='utf-8') as temp:
            self.template = temp.read().split("\n")

        self.the_file = None

        self.handlers()

    def read_media_url(self, file_path) -> str:
        with open(file_path, "r") as f:
            return f.read()

    def read_template_config(self):
        if not os.path.exists(self.template_file):
            with open(self.template_file, "w") as tempconfig:
                tempconfig.write("words.txt")

    def get_template_name(self) -> str:
        if os.path.exists(self.template_file) and os.path.getsize(self.template_file) > 0:
            with open(self.template_file, "r") as setting_tcfg:
                thetcfg = setting_tcfg.read()
                return thetcfg
        return ""

    def handlers(self):
        @self.watcher
        async def rwatcher(event):
            if event.sender_id in self.users:
                if self.mode == "reply":
                    await self.asyncio.sleep(float(self.delay))
                    await event.reply(self.autorepond_header + " " + self.random.choice(self.template), file=self.the_file)
                    self.log.debug(f"Reply to a user's message: {event.sender_id} [Mode: {self.mode}] [File: {self.the_file}]")

                elif self.mode == "send":
                    await self.asyncio.sleep(float(self.delay))
                    await event.respond(self.autorepond_header + " " + self.random.choice(self.template), file=self.the_file)
                    self.log.debug(f"Reply to a user's message: {event.sender_id} [Mode: {self.mode}] [File: {self.the_file}]")

        @self.strict_owner_command
        async def bladd(event):
            """reply -> start auto-reply"""
            try:
                reply_message = await event.get_reply_message()
                if reply_message:
                    user_id = int(reply_message.from_id.user_id) if reply_message.from_id else reply_message.from_id
                    self.users.append(user_id)
                    self.log.debug(f"You have added a user to the list, id: {user_id}")
                    await event.edit("<b>User added to the list</b>", parse_mode='html')
                else:
                    await event.edit("<b>Where is the reply on the User's message?</b>", parse_mode='html')
            except Exception as e:
                print(f"An error occurred: {e}")

        @self.strict_owner_command
        async def blclear(event):
            """clears all autoresponder targets"""

            self.log.debug("The list has been completely cleared.")
            self.users = []
            await event.edit("<b>Users cleared</b>", parse_mode='html')

        @self.strict_owner_command
        async def blremove(event):
            """reply or user id -> remove a person from the autoresponder list"""

            reply = await event.get_reply_message()

            if not reply:
                args = int(
                    " ".join(
                        await self.get_args(event, maxsplit=1)
                    )
                )

                if args in self.users:
                    self.users.remove(args)
                    user = await self.client.get_entity(args)
                    await event.edit(f"<b>User {user.first_name} has been removed from the list</b>\n<b>ID</b>: <code>{args}</code>", parse_mode='html')
                else:
                    await event.edit("<b>The user was not on the list</b>", parse_mode='html')

            if reply:
                reply_id = reply.sender_id
                if reply_id in self.users:
                    self.users.remove(reply_id)
                    reply_user = await self.client.get_entity(reply_id)
                    await event.edit(f"<b>User {reply_user.first_name} has been removed from the list</b>\n<b>ID</b>: <code>{reply_id}</code>", parse_mode='html')

                else:
                    await event.edit("<b>The user was not on the list</b>", parse_mode='html')

        @self.strict_owner_command
        async def blstop(event):
            """erase the current conference from the list of goals"""

            args = int(
                " ".join(
                    await self.get_args(event, maxsplit=1)
                )
            )

            if args in self.chats:
                self.chats.remove(args)

            elif args in self.chats_voice:
                self.chats_voice.remove(args)

            elif args in self.chats_photo:
                self.chats_photo.remove(args)

            elif args in self.chats_video:
                self.chats_video.remove(args)

            elif args in self.chats_tagger:
                self.chats_tagger.remove(args)

            elif args in self.chats_typer:
                self.chats_typer.remove(args)

        @self.strict_owner_command
        async def blrheader(event):
            """header -> Change header / del -> Removing the header"""

            args = await self.get_args(event, maxsplit=1)

            if args == "del":
                self.autorepond_header = ''
                await event.edit("<b>Header removed</b>.", parse_mode='html')

            if args != "del":
                self.old_header = self.autorepond_header
                self.autorepond_header = args
                if self.old_header == "":
                    self.old_header = "No"

            await event.edit(f"<b>The header has been changed to: <code>{self.autorepond_header}</code>\nOld hat: <code>{self.old_header}</code></b>", parse_mode='html')

        @self.strict_owner_command
        async def blrdelay(event):
            """delay -> setting the sending delay"""

            args = await self.get_args(event, maxsplit=1)

            self.delay = float(args)

            self.log.debug(f"Auto-responder delay: {self.delay}")
            await event.edit(f"Delay: {self.delay}")

        @self.strict_owner_command
        async def blmmode(event):
            """vid / ph / txt -> select media"""
            args = await self.get_args(event, maxsplit=1)

            if args == "ph":
                self.the_file = self.photo_url
                prew = 'Texts + Photo'

            elif args == "vid":
                self.the_file = self.video_url
                prew = 'Texts + Video'

            elif args == "txt":
                self.the_file = None
                prew = 'Texts'

            self.log.debug(f"Auto-responder media: {prew}")
            await event.edit(f"Mode: {prew}")

        @self.strict_owner_command
        async def blmode(event):
            """reply / send -> changing the sending mode"""
            args = await self.get_args(event, maxsplit=1)

            if args == "reply" or args == "send":
                self.mode = args
                await event.edit(f"Mode: {'Send to replay' if self.mode == 'reply' else 'Regular send'}")
                self.log.debug(f"Auto Answer Mode: {self.mode}")
            else:
                await event.edit("You specified an invalid mode.Available modes: 'reply', 'send'")

        @self.strict_owner_command
        async def blsetfile(message):
            """file.txt: change template"""

            args = await self.get_args(message, maxsplit=1)
            template_dir = self.directories["message"]
            template_file = os.path.join(template_dir, "template.txt")
            template_files = os.listdir(template_dir)

            if args in template_files:
                if self.shablon_name != args:
                    self.log.debug(f"New selected template: {args}")
                    await message.edit(f"<b>Template selected</b>: <code>{args}</code>", parse_mode='html')

                    with open(template_file, "w", encoding='utf-8') as write_template:
                        write_template.write(args)

                    self.shablon_name = args

                    os.remove(template_file)
                    self.write_template_config(args)

                    with open(os.path.join(template_dir, self.shablon_name), "r", encoding='utf-8') as temp:
                        self.template = temp.read().splitlines()
            else:
                self.log.debug(f"Pattern not found: {args}")
                await message.edit(f"<b>File [<code>{args}</code>] not found</b>", parse_mode='html')

        @self.strict_owner_command
        async def blfiles(message):
            """list of installed templates"""

            templates = os.listdir(self.directories["message"])

            if not templates:
                text = "<b>The template directory is empty.</b>"
            else:
                result = '\n'.join([f"<code>{template}</code>" for template in templates])
                current_shablon = self.templon_name or "not selected"
                text = f"<b>Available template files:</b>\n\n{result}\n\n<b>Current template: </b><code>{current_shablon}</code>"

            await message.edit(text, parse_mode='html')

        @self.strict_owner_command
        async def blupload(event):
            """reply: get link to file"""

            reply = await event.get_reply_message()

            if not reply:
                await event.edit("Where is the reply?")
                return None

            if reply.photo or reply.video:
                await event.delete()

                media = reply.photo if reply.photo else reply.video
                media_type = 'image' if reply.photo else 'video'

                filename = await self.client.download_media(media, self.directories["cache"])

                url = 'https://telegra.ph/upload'

                async with self.aiohttp.ClientSession() as session:
                    async with self.aiofiles.open(filename, 'rb') as file:
                        files = {'file': ('{}.{}'.format(media_type, filename.split('.')[-1]), file)}
                        async with session.post(url, data=files) as response:
                            if response.status != 200:
                                return

                            result_json = await response.json()
                            link = 'https://telegra.ph' + result_json[0]['src']
                            await event.respond(f'<b>Link</b>: <code>{link}</code>', parse_mode='html')

        @self.strict_owner_command
        async def blqload(event):
            """reply: get link to file + auto-apply"""

            reply = await event.get_reply_message()

            if not reply:
                await event.edit("Where is the replay?")
                return

            if reply.photo or reply.video:
                media_type = "photo" if reply.photo else "video"

                await event.edit(f"<b>Loading {media_type}</b>...", parse_mode="html")

                filename = await self.client.download_media(reply.media, self.directories["cache"])

                url = 'https://telegra.ph/upload'
                file_field_name = 'file'

                async with self.aiohttp.ClientSession() as session:
                    async with self.aiohttp.FormData() as form:
                        form.add_field(file_field_name, open(filename, 'rb'))
                        async with session.post(url, data=form) as response:
                            if response.status != 200:
                                return

                            json_data = await response.json()
                            link = 'https://telegra.ph' + json_data[0]['src']

                            media_file = os.path.join(self.directories["media"], media_type)

                            os.remove(media_file) if os.path.exists(media_file) else None

                            with open(media_file, "w") as f:
                                f.write(link)

                            if media_type == "video":
                                self.video_url = link
                            elif media_type == "photo":
                                self.photo_url = link

                            await event.edit(
                                f"<b>Link</b>: <code>{link}</code>\n\n<b>File Type</b>: <code>{media_type.capitalize()}</code>",
                                parse_mode='html'
                            )

        @self.strict_owner_command
        async def blch(event):
            """clear cache"""

            folder_path = self.directories["cache"]
            file_list = os.listdir(folder_path)
            total_size = 0

            for path, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(path, file)
                    total_size += os.path.getsize(file_path)

            megabytes = round(total_size / (1024 * 1024), 2)

            for file_name in file_list:
                file_path = os.path.join(self.directories["cache"], file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

                await event.edit(f"<b>Ready, cache data has been cleared, freed</b>: <code>{megabytes} MB</code> / <code>{round(total_size)} Bytes</code>", parse_mode='html')

        @self.strict_owner_command
        async def blsetvd(event):
            """url: uploads your video to the config"""

            try:
                args = await self.get_args(event, maxsplit=1)

                async with self.aiohttp.ClientSession() as session:
                    try:
                        async with session.get(args) as response:
                            response.raise_for_status()
                    except self.aiohttp.ClientError:
                        return await event.edit(f"<b>Invalid link:</b> <code>{args}</code>", parse_mode='html')

                self.video_file = os.path.join(self.directories["media"], "video.txt")
                if os.path.exists(self.video_file):
                    os.remove(self.video_file)

                async with self.aiofiles.open(self.video_file, mode="w") as vd:
                    await vd.write(args)

                self.log.debug(f"New video applied: {args}")
                self.video_url = args
                await event.edit(f"<b>Video loaded, link</b>: <code>{args}</code>", parse_mode='html')

            except Exception as e:
                await event.edit(f"<b>Error:</b> <code>{e}</code>", parse_mode='html')

        @self.strict_owner_command
        async def blsetph(event):
            """url: uploads your photo to the config"""

            try:
                args = await self.get_args(event, maxsplit=1)

                async with self.aiohttp.ClientSession() as session:
                    try:
                        async with session.get(args) as response:
                            response.raise_for_status()
                    except self.aiohttp.ClientError:
                        return await event.edit(f"<b>Invalid link:</b> <code>{args}</code>", parse_mode='html')

                self.photo_file = os.path.join(self.directories["media"], "photo.txt")
                if os.path.exists(self.photo_file):
                    os.remove(self.photo_file)

                async with self.aiofiles.open(self.photo_file, mode="w") as ph:
                    await ph.write(args)

                self.log.debug(f"New photo applied: {args}")
                self.photo_url = args
                await event.edit(f"<b>Photo uploaded, link</b>: <code>{args}</code>", parse_mode='html')

            except Exception as e:
                await event.edit(f"<b>Error:</b> <code>{e}</code>", parse_mode='html')

        @self.strict_owner_command
        async def blinc(event):
            """delay -> start flooder"""
            args: list = await self.get_args(event)
            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = event.chat_id
            await event.edit("Arguments accepted.")
            self.chats.append(chat_id)
            self.log.debug(f"{chat_id} is now in the target list!")

            while event.chat_id in self.chats:
                await self.client.send_message(chat_id, header + " " + self.random.choice(self.template))
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blinj(message):
            """delay -> start flooder (optimization)"""
            args = await self.get_args(message)
            reply = await message.get_reply_message()
            file = reply if reply and reply.file else None

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.chats.append(chat_id)
            self.log.debug(f"{chat_id} is now in the target list!")

            while message.chat_id in self.chats:
                await self.client.send_message(chat_id, header + " " + self.random.choice(self.template), file=file)
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blinm(message):
            """delay -> start flooder (music)"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.chats_voice.append(chat_id)
            self.log.debug(f"{chat_id} is now in the target list!")

            while message.chat_id in self.chats_voice:
                tts = self.gTTS(self.random.choice(self.template), lang='ru')
                ttd = os.join.path(self.directories["voice"], "rage.mp3")
                tts.save(ttd)
                await self.client.send_message(chat_id, header, file=ttd)
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blinv(message):
            """delay -> start flooder (voice)"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.chats_voice.append(chat_id)
            self.log.debug(f"{chat_id} is now in the target list!")

            while chat_id in self.chats_voice:
                tts = self.gTTS(self.random.choice(self.template), lang='ru')
                ttd = os.join.path(self.directories["voice"], "rage.mp3")
                tts.save(ttd)
                await self.client.send_file(chat_id, ttd, caption=header, voice_note=True)
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blint(message):
            """delay -> start flooder (typing)"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            reply = await message.get_reply_message()
            file = reply if reply and reply.file else None

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.chats_typer.append((chat_id))
            self.log.debug(f"{chat_id} is now in the target list!")

            while chat_id in self.chats_typer:
                async with self.client.action(chat_id, "typing"):
                    await self.asyncio.sleep(1)
                    await self.client.send_message(chat_id, header + " " + self.random.choice(self.template), file=file)

                await self.asyncio.sleep(delay)

        @self.strict_owner_command
        async def blins(message):
            """delay -> start media flooder (reliability)"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            reply = await message.get_reply_message()

            if reply and reply.file:
                file = await reply.download_media(file=os.path.join(self.directories["inj", "inject_photo.jpg"]) if reply.file.mime_type.startswith("image/") else "media/inject_video.mp4")

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.chats.append(chat_id)
            self.log.debug(f"{chat_id} is now in the target list!")

            while message.chat_id in self.chats:
                await self.client.send_message(chat_id, header + " " + self.random.choice(self.template), file=file)
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blschedule(message):
            """delay in minutes + conference ID -> fill your calendar with pending messages"""
            reply = await message.get_reply_message()
            file = reply if reply and reply.file else None

            try:
                args = await self.get_args(message)

                delay = int(args[0])
                chat_id = args[1]
                header_list = args[2:]
                header = " ".join(header_list) if header_list else ""

                await message.edit("Arguments accepted.")
                self.log.debug(f"Snooze messages for chat: {chat_id}")
                self.chats.append(chat_id)

            except Exception as e:
                await message.edit(f"<b>Error reading arguments</b>.\n<u>Error</u>: <i><code>{e}</code></i>",
                                   parse_mode='html')
                self.log.error(e)
                print(f"{args} : {type(args)}")

            original_time = delay

            for i in range(100):
                try:
                    await self.client.send_message(
                        entity=int(chat_id),
                        message=header + " " + self.random.choice(self.template) if header else self.random.choice(self.template),
                        schedule=self.datetime.timedelta(minutes=delay),
                        file=file
                    )
                    delay += original_time
                    await self.asyncio.sleep(0.1)

                except Exception as error:
                    self.log.error(error)
                    break

        @self.strict_owner_command
        async def bltag(message):
            """delay + user ID -> tagger start"""

            reply = await message.get_reply_message()
            file = reply if reply and reply.file else None

            try:
                args = await self.get_args(message)
                delay = int(args[0])
                user_target = args[1]
                header_list = args[2:]
                header = " ".join(header_list) if header_list else ""

                await message.edit("Arguments accepted.")
                self.log.debug(f"Snooze messages for chat: {message.chat_id}")
                self.chats_tagger.append((message.chat_id))

            except Exception as e:
                await message.edit(f"<b>Error reading arguments</b>.\n<u>Error</u>: <i><code>{e}</code></i>",
                                   parse_mode='html')

            while message.chat_id in self.chats_tagger:
                await self.client.send_message(
                    message.chat_id,
                    f"<a href='tg://user?id={user_target}'>{header + ' ' if header else ''}{self.random.choice(self.template)}</a>",
                    file=file,
                    parse_mode='html'
                )
                await self.asyncio.sleep(delay)

        @self.strict_owner_command
        async def blload(event):
            """reply: downloads template to directory templates"""

            directory = self.directories["message"]
            os.makedirs(directory, exist_ok=True)

            try:
                replied_msg = await event.get_reply_message()
                if replied_msg.media:
                    file_path = os.path.join(directory, replied_msg.file.name)
                    downloaded_file = await self.client.download_media(replied_msg.media, file=file_path)
                    self.log.debug(f"The file {downloaded_file} was downloaded!")
                    await event.edit(f"<b>Downloaded</b>: <code>{downloaded_file}</code>", parse_mode='html')
                else:
                    await event.edit("<b>Reply media not found</b>.", parse_mode="html")

            except Exception as ex:
                await event.edit(f"**Error**:\n```{ex}```", parse_mode="markdown")

        @self.strict_owner_command
        async def blrsv(message):
            """delay -> start flooder + video"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.log.debug(f"{chat_id} is now in the target list! [File: {self.video_url}]")
            self.chats_video.append(chat_id)

            while message.chat_id in self.chats_video:
                await self.client.send_file(
                    chat_id,
                    self.video_url,
                    caption=header + " " + self.random.choice(self.template)
                )
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blrsp(message):
            """delay -> start flooder + photo"""
            args = await self.get_args(message)

            delay = args[0]
            header_list = args[1:]
            header = " ".join(header_list) if header_list else ""

            chat_id = message.chat_id
            await message.edit("Arguments accepted.")
            self.log.debug(f"{chat_id} is now in the target list! [File: {self.photo_url}]")
            self.chats_photo.append(chat_id)

            while True:
                await self.client.send_file(chat_id, self.photo_url, caption=header + " " + self.random.choice(self.template))
                await self.asyncio.sleep(float(delay))

        @self.strict_owner_command
        async def blstate(message):
            """bot statuses"""
            await message.edit(f"<b>Flooders:\n<b>Chats [Text]</b>: <u>{self.chats}</u>\n<b>Chats [Photo]</b >: <u>{self.chats_photo}</u>\n<b>Chats [Video]</b>: <u>{self.chats_video}</u>\n<b>Chats [Tagger]</b>: <u>{self.chats_tagger}</u>\n<b>Erase the current conference from the list of goals</b>: <code>.blstop</code>\n<b>Erase the conference from the list targets by ID</b>: <code>.blstop</code> + chat_id\n<b>Erase all targets</b>: <code>.blstopall</code>\n\n<b>Auto responders</b>:\n<b>Users</b>: <u>{self.users}</u>\n<b>To remove a user from the target list</b>: <code>.blremove</code> + <i>reply to user</i>\n<b>For inline removal</b>: <code>.blremove</code> + <b>user_id</b>\n<b>To clear the entire list</b>: <code>.blclear</code>", parse_mode='html')

        @self.strict_owner_command
        async def blstopall(message):
            """erase all targets"""
            self.chats = []
            self.chats_photo = []
            self.chats_video = []
            self.chats_tagger = []
            self.chats_typer = []
            self.log.debug("All chats cleared from target list")
            await message.edit("<b>Ready</b>", parse_mode='html')


Bloody()
