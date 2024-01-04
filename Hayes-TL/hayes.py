import loader
import os


class hLoader(loader.Module):
    """built-in hayesLoader module"""

    def __init__(self) -> None:
        self.strings: dict = {
            "Errors": {
                "IsADirectory": "The command does not accept the directory",
                "FileNotFound": "The {} is not installed or cannot be removed"
            }
        }

        self.init()
        self.log = self.get_logger()
        self.loader = loader.Loader()
        self.files = self.Utils.Files
        self.hashlib = self.req('hashlib', _importlib=True)
        self.asyncio = self.req('asyncio', _importlib=True)
        self.handle()

    def handle(self):
        @self.strict_owner_command
        async def lm(event) -> None:
            """install module"""
            reply = await event.get_reply_message()
            if reply and reply.file:
                file_name = reply.file.name
                if any(file_name.lower().endswith(ext) for ext in self.loader.valid_extensions):
                    file_path = os.path.join("modules", file_name)
                    await self.client.download_media(reply, file_path)
                    self.log.debug(f"Module '{self.loader.get_module_name(file_name)}' installed")
                    await self.loader.hook_module_adv(file_name)

                    await event.edit('<b>Loading.</b>', parse_mode='html')
                    await event.edit('<b>Loading..</b>', parse_mode='html')
                    await self.asyncio.sleep(0.4)
                    await event.edit('<b>Loading...</b>', parse_mode='html')

                    with open(file_path, "rb") as file:
                        content = file.read()

                    await event.edit(
                        f"<b>Module with file name '{file_name}' is updated</b>\n"
                        f"<b>The module can be viewed in <code>.mods</code></b>\n",
                        parse_mode="html"
                    )
                else:
                    await event.edit(f"<b>Invalid file extension</b>: <code>{file_name}</code>", parse_mode="html")
                    self.log.error(f"Invalid file extension: {file_name}")

            elif event.media:
                file_name = event.file.name

                if any(file_name.lower().endswith(ext) for ext in self.loader.valid_extensions):
                    await event.download_media(os.path.join("modules", file_name))
                    self.log.debug(f"Module '{self.loader.get_module_name(file_name)}' installed")
                    await self.loader.hook_module_adv(file_name)

                    await event.edit('<b>Loading.</b>', parse_mode='html')
                    await event.edit('<b>Loading..</b>', parse_mode='html')
                    await self.asyncio.sleep(0.4)
                    await event.edit('<b>Loading...</b>', parse_mode='html')

                    await event.edit(
                        f"<b>Module with file name '{file_name}' is updated</b>\n"
                        f"<b>The module can be viewed in <code>.mods</code></b>\n",
                        parse_mode="html"
                    )
                else:
                    await event.edit(f"<b>Invalid file extension</b>: <code>{file_name}</code>", parse_mode="html")
                    self.log.error(f"Invalid file extension: {file_name}")

            else:
                await event.edit("<b>Reply to file or file with caption .lm not found</b>.", parse_mode="html")
                self.log.error("Reply to file or file with caption .lm not found.")

        @self.strict_owner_command
        async def rawlm(event) -> None:
            """filename + url -> download the module from any source"""
            args: list = await self.get_args(event)
            file_name = args[0]
            url = ' '.join(args[1:])

            file_path = os.path.join(self.loader.module_folder, file_name)
            file_module_name = self.loader.get_module_name(file_name)
            content = await self.loader.get_content(url=url)
            await self.files.save_content_to_file(content=content, file_path=file_path)
            self.log.debug(f"Module '{file_module_name}' installed")
            await self.loader.hook_module_adv(file_name)

            await event.edit('<b>Loading.</b>', parse_mode='html')
            await event.edit('<b>Loading..</b>', parse_mode='html')
            await self.asyncio.sleep(0.4)
            await event.edit('<b>Loading...</b>', parse_mode='html')

            await event.edit(
                f"<b>Module with file name '{file_name}' is updated</b>\n"
                f"<b>The module can be viewed in <code>.mods</code></b>\n",
                parse_mode="html"
            )

        @self.strict_owner_command
        async def pblm(event) -> None:
            """filename + key -> download module from pastebin"""
            args: list = await self.get_args(event)
            file_name = args[0]
            past_key = ' '.join(args[1:])

            raw_pastebin_url = await self.loader.generate_raw_pastebin_url(past_key)
            content = await self.loader.get_content(raw_pastebin_url)

            file_path = os.path.join(self.loader.module_folder, file_name)
            file_module_name = self.loader.get_module_name(file_name)

            await self.files.save_content_to_file(content=content, file_path=file_path)
            self.log.debug(f"Module '{file_module_name}' installed")
            await self.loader.hook_module_adv(file_name)

            await event.edit('<b>Loading.</b>', parse_mode='html')
            await event.edit('<b>Loading..</b>', parse_mode='html')
            await self.asyncio.sleep(0.4)
            await event.edit('<b>Loading...</b>', parse_mode='html')

            await event.edit(
                f"<b>Module with file name '{file_name}' is updated</b>\n"
                f"<b>The module can be viewed in <code>.mods</code></b>\n",
                parse_mode="html"
            )

        @self.strict_owner_command
        async def gitlm(event) -> None:
            """module -> download module from github"""
            args: list = await self.get_args(event)
            module_name: str = args[0]
            modules_repo: str = self.Utils.Config.modules_repo

            if modules_repo.endswith('/'):
                modules_repo = modules_repo[:-1]

            if module_name.startswith('/'):
                module_name = module_name[1:]

            content = await self.loader.get_content(f"{modules_repo}/{module_name}")

            file_path = os.path.join(self.loader.module_folder, module_name)
            file_module_name = self.loader.get_module_name(module_name)

            await self.files.save_content_to_file(content=content, file_path=file_path)
            self.log.debug(f"Module '{file_module_name}' installed")

            print(self.loader.hooked_modules)
            await self.loader.hook_module_adv(module_name)

            await event.edit('<b>Loading.</b>', parse_mode='html')
            await event.edit('<b>Loading..</b>', parse_mode='html')
            await self.asyncio.sleep(0.4)
            await event.edit('<b>Loading...</b>', parse_mode='html')

            await event.edit(
                f"<b>Module with file name '{module_name}' is updated</b>\n"
                f"<b>The module can be viewed in <code>.mods</code></b>\n",
                parse_mode="html"
            )

        @self.strict_owner_command
        async def gitum(event) -> None:
            """module -> update module, source: github"""
            args: list = await self.get_args(event)
            module_name: str = args[0]
            modules_repo: str = self.Utils.Config.modules_repo

            if modules_repo.endswith('/'):
                modules_repo = modules_repo[:-1]

            if module_name.startswith('/'):
                module_name = module_name[1:]

            github_content = await self.loader.get_content(f"{modules_repo}/{module_name}")

            file_path = os.path.join(self.loader.module_folder, module_name)
            file_module_name = self.loader.get_module_name(module_name)

            file_hash = self.hashlib.sha256(await self.files.read_file(file_path)).hexdigest()
            github_hash = self.hashlib.sha256(github_content).hexdigest()

            if file_hash != github_hash:
                await self.loader.unhook_module(module_name)

                await self.files.save_content_to_file(content=github_content, file_path=file_path)
                self.log.debug(f"Module '{file_module_name}' reinstalled")
                await self.loader.hook_module_adv(module_name)

                await event.edit('<b>Loading.</b>', parse_mode='html')
                await event.edit('<b>Loading..</b>', parse_mode='html')
                await self.asyncio.sleep(0.4)
                await event.edit('<b>Loading...</b>', parse_mode='html')

                await event.edit(
                    f"<b>Module with file name '{module_name}' is updated</b>\n"
                    f"<b>The module can be viewed in <code>.mods</code></b>\n",
                    parse_mode="html"
                )

            else:
                await event.edit(
                    f"<b>No updates found for module '{self.loader.get_module_name(module_name)}'</b>",
                    parse_mode='html'
                )

        @self.strict_owner_command
        async def delm(event) -> None:
            """mdl_filename -> remove module"""
            try:
                module_file = ' '.join(event.text.split(" ", maxsplit=1)[1:])
                module_name = self.loader.get_module_name(module_file)
                hayes_module_file = self.Utils.Dictionary.get_key_by_subkey(self.loader.hooked_modules, self._name)
                hayes_module_name = self.loader.get_module_name(hayes_module_file)

                if module_file != self.Utils.Dictionary.get_key_by_subkey(self.loader.hooked_modules, self._name):
                    await self.loader.unhook_module(module_file)
                    os.remove(os.path.join(self.loader.module_folder, module_file))
                    await event.edit(f"<b>Module '{module_name}' Unloaded</b>", parse_mode="html")
                    self.log.debug(f"Module '{module_name}' Unloaded")

                else:
                    await event.edit(f"<b>Error when removing built-in module ('{hayes_module_name}')</b>", parse_mode="html")

            except FileNotFoundError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('FileNotFound').format('module')}```", parse_mode="markdown")

            except IsADirectoryError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('IsADirectory')}```", parse_mode="markdown")

            except Exception as err:
                self.log.error(f"Failed to unload module '{module_name}': {err}")
                await event.edit(f"**An unhandled error occurred**:\n```{err}```", parse_mode="markdown")

        @self.strict_owner_command
        async def mdrop(event):
            """mdl_filename -> drop module"""
            try:
                module_file = ' '.join(event.text.split(" ", maxsplit=1)[1:])
                module_path = os.path.join(self.loader.module_folder, module_file)

                if os.path.exists(module_path):
                    await event.delete()
                    await event.respond(
                        f"<b>The module will be dropped:</b> <code>{str(module_path)}</code>",
                        parse_mode='html',
                        file=module_path
                    )

                    self.log.debug(f"Module '{self.loader.get_module_name(module_file)}' Dropped in chat")
                else:
                    await event.edit(f"**Module file not found**:\n```{module_file}```", parse_mode="markdown")
                    self.log.error(f"Module file not found: {module_file}")

            except FileNotFoundError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('FileNotFound').format('module')}```", parse_mode="markdown")

            except IsADirectoryError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('IsADirectory')}```", parse_mode="markdown")

            except Exception as err:
                self.log.error(f"Failed to drop module '{self.loader.get_module_name(module_file)}': {err}")
                await event.edit(f"**An unhandled error occurred**:\n```{err}```", parse_mode="markdown")

        @self.strict_owner_command
        async def plist(event):
            """shows a list of installed plugins"""
            await event.edit(f"<b>Loaded <code>{self.count_plugins()}</code> {'plugin' if self.count_plugins() == 1 else 'plugins'}</b>:\n\n{self.plugin_list()}", parse_mode="html")

        @self.strict_owner_command
        async def pdrop(event):
            """plug_filename -> drop plugin"""
            filename = ' '.join(event.text.split(" ", maxsplit=1)[1:])
            try:
                plugin_path = os.path.join(self.loader.plugin_folder, str(filename))

                if os.path.exists(plugin_path):
                    await event.delete()
                    await event.respond(
                        "<b>Plugin dropped</b>",
                        parse_mode='html',
                        file=plugin_path
                    )

                    self.log.debug(f"Plugin '{self.loader.get_module_name(filename)}' Dropped in chat")
                else:
                    await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('FileNotFound').format('plugin')}```", parse_mode="markdown")
                    self.log.warning(f"Plugin file not found: {filename}")

            except IsADirectoryError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('IsADirectory')}```", parse_mode="markdown")

            except Exception as err:
                self.log.error(f"Failed to drop plugin '{self.loader.get_module_name(filename)}': {err}")
                await event.edit(f"**An unhandled error occurred**:\n```{err}```", parse_mode="markdown")

        @self.strict_owner_command
        async def lp(event) -> None:
            """install plugin"""
            reply = await event.get_reply_message()
            if reply and reply.file:
                file_name = reply.file.name

                if any(file_name.lower().endswith(ext) for ext in self.loader.valid_extensions):
                    await self.client.download_media(reply, os.path.join(self.loader.plugin_folder, file_name))

                    await self.files.append_text_if_not_exists(
                        os.path.join(
                            self.loader.plugin_folder,
                            self.loader.init_file
                        ),
                        f'import {self.loader.plugin_folder}.{self.loader.get_module_name(module_file=file_name)}'
                    )

                    self.log.debug(f"Plugin {self.loader.plugin_folder}.{self.loader.get_module_name(file_name)} loaded")
                    await event.edit(f"<b>Plugin <code>{self.loader.plugin_folder}.{self.loader.get_module_name(file_name)}</code> loaded</b>", parse_mode="html")
                else:
                    await event.edit(f"<b>Invalid file extension</b>: <code>{file_name}</code>", parse_mode="html")
                    self.log.error(f"Invalid file extension: {file_name}")
            else:
                await event.edit("<b>No file attached to the reply</b>.", parse_mode="html")
                self.log.error("No file attached to the reply.")

        @self.strict_owner_command
        async def delp(event) -> None:
            """remove plugin"""
            filename = ' '.join(event.text.split(" ", maxsplit=1)[1:])
            try:
                await self.files.remove_text(
                    file_path=os.path.join(
                        self.loader.plugin_folder,
                        self.loader.init_file
                    ),
                    text_to_remove=f"import {self.loader.plugin_folder}.{self.loader.get_module_name(module_file=filename)}"
                )
                os.remove(os.path.join(self.loader.plugin_folder, str(filename)))
                self.log.debug(f"Plugin '{self.loader.get_module_name(filename)}' Unloaded")
                await event.edit(f"<b>Plugin '{self.loader.get_module_name(filename)}' was successfully unloaded</b>", parse_mode="html")

            except FileNotFoundError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('FileNotFound').format('plugin')}```", parse_mode="markdown")

            except IsADirectoryError:
                await event.edit(f"**Error**:\n```{self.strings.get('Errors', {}).get('IsADirectory')}```", parse_mode="markdown")

            except Exception as err:
                self.log.error(f"Failed to unload plugin '{self.loader.get_module_name(filename)}': {err}")
                await event.edit(f"**An unhandled error occurred**:\n```{err}```", parse_mode="markdown")


class hMem(loader.Module):
    """built-in hayesMemory module"""

    def __init__(self) -> None:
        self.strings: dict = {
            "cachelogs": {
                "archiving": "Archiving, current files: {}",
                "archived": "[{}] Archived"
            },
            "delcache": {
                "cleaning": "Cleaning, current files: {}",
                "cleared": "[{}] Folder cleared"
            },
            "directory": {
                "size_calculated": "[{}] Directory size calculated, current size: {}"
            }
        }

        self.init()
        self.log = self.get_logger()
        self.loader = loader.Loader()
        self.handle()

    def handle(self):
        @self.strict_owner_command
        async def cachelogs(event):
            """caches logs in a .zip archive"""
            await event.delete()

            before_size: int = await self.Utils.Files.get_folder_size_async(
                folder_path=self.loader.logs_folder
            )

            self.log.debug(self.strings.get("directory", {}).get("size_calculated").format(self.loader.logs_folder, before_size))

            full_log_folder = os.path.join(os.getcwd(), self.loader.logs_folder)
            files = os.listdir(full_log_folder)

            self.log.debug(self.strings.get('cachelogs', {}).get("archiving").format(files))

            for file in files:
                await self.Utils.Files.archive_file(
                    file_path=os.path.join(
                        full_log_folder,
                        file
                    ),
                    timestamp=True
                )

            self.log.debug(self.strings.get('cachelogs', {}).get('archived').format(self.loader.logs_folder))

            after_size: int = await self.Utils.Files.get_folder_size_async(
                folder_path=self.loader.logs_folder
            )
            self.log.debug(self.strings.get("directory", {}).get("size_calculated").format(self.loader.logs_folder, after_size))

            await event.respond(
                f"<b>The logs are successfully cached in the archive</b>\n"
                f"<b>Size before caching</b>: <code>{before_size}</code> <b>bytes</b>\n"
                f"<b>Size after caching</b>: <code>{after_size}</code> <b>bytes</b>\n"
                f"<b>Size difference</b>: <code>{abs(before_size - after_size)}</code> <b>bytes</b>\n",
                parse_mode='html'
            )

        @self.strict_owner_command
        async def delcache(event):
            """deletes the __pycache__ folder"""
            await event.delete()

            before_size: int = await self.Utils.Files.get_folder_size_async(
                folder_path=self.loader.pycache_folder
            )

            self.log.debug(self.strings.get("directory", {}).get("size_calculated").format(self.loader.pycache_folder, before_size))

            full_pycache_folder = os.path.join(os.getcwd(), self.loader.pycache_folder)
            files = os.listdir(full_pycache_folder)

            self.log.debug(self.strings.get('delcache', {}).get("cleaning").format(files))

            for file in files:
                os.remove(
                    path=os.path.join(
                        full_pycache_folder,
                        file
                    )
                )

            self.log.debug(self.strings.get('delcache', {}).get('cleared'))

            after_size: int = await self.Utils.Files.get_folder_size_async(
                folder_path=self.loader.pycache_folder
            )

            self.log.debug(self.strings.get("directory", {}).get("size_calculated").format(self.loader.pycache_folder, after_size))

            await event.respond(
                f"<b>The cache folder is successfully cleared</b>\n"
                f"<b>Size before cleaning</b>: <code>{before_size}</code> <b>bytes</b>\n"
                f"<b>Size after cleaning</b>: <code>{after_size}</code> <b>bytes</b>\n"
                f"<b>Size difference</b>: <code>{abs(before_size - after_size)}</code> <b>bytes</b>\n",
                parse_mode='html'
            )


class hayes(loader.Module):
    """built-in hayes module"""

    def __init__(self) -> None:
        self.init()

        self.inline_state = True
        self.inline_result = []

        self.log = self.get_logger()
        self.html = self.req('html', _importlib=True)
        self.asyncio = self.req('asyncio', _importlib=True)
        self.subprocess = self.req('subprocess', _importlib=True)

        self.handle()

    def handle(self) -> None:
        @self.strict_owner_command
        async def uptime(event):
            """shows the bot\'s operating time"""
            results = await self.client.inline_query("@hayes_inlinebot", "Uptime")
            await results[0].click(event.chat_id)
            await event.delete()

        @self.inline_query()
        async def inline(event):
            buttons = [self.Btn.inline("Update", b'show_callback')]
            result = await event.builder.article(
                title='Uptime',
                text=f'<b>Uptime:</b> <code>{self.uptime()}</code>',
                parse_mode='html',
                buttons=buttons
            )
            if self.inline_state is True:
                self.inline_state = False
                self.inline_result.append(result)

            await event.answer(self.inline_result, cache_time=0)

        @self.callback_query()
        async def callback(event):
            if event.data == b'show_callback':
                await event.edit(
                    f'<b>Uptime:</b> <code>{self.uptime()}</code>',
                    parse_mode='html',
                    buttons=[[self.Btn.inline("Update", b'show_callback')]]
                )

        @self.strict_owner_command
        async def mods(event) -> None:
            """shows a list of installed mods"""
            args: list = await self.get_args(event)
            if len(args) > 0:
                args = ' '.join(args[0:])
                if self.module_commands != "None":
                    await event.edit(f"<b>Module</b>: <code>{args}</code>\n<b>Description</b>: <b><i>{self.get_mdl_description(args)}</i></b>\n\n{self.module_commands(args)}", parse_mode='html')
                else:
                    await event.edit(f'<b>Module</b>: <code>{args}</code>: Not found', parse_mode='html')
            else:
                args = None
                await event.edit(f"<b>Loaded <code>{self.count_modules()}</code> {'module' if self.count_modules() < 2 else 'modules'}</b>:\n\n{self.module_list()}", parse_mode="html")

        @self.strict_owner_command
        async def restart(event) -> None:
            """causes the loader to restart"""
            await event.edit("<b>Restarting loader</b>...", parse_mode="html")
            self.log.debug("Restarting loader...")
            await event.edit("<b>Loader restarted!</b>", parse_mode="html")
            self.log.debug("Loader restarted!")
            self.restart()

        @self.strict_owner_command
        async def close(event) -> None:
            """causes bot threads to close"""
            self.log.debug("Closing a thread...")
            await event.edit("<b>Closing a thread</b>...", parse_mode="html")
            self.log.debug("Stream closed!")
            await event.edit("<b>Stream closed!</b>", parse_mode="html")
            self.exit()

        @self.strict_owner_command
        async def id(event) -> None:
            """shows unique chat ID"""
            await event.edit(f"<b>ID</b>: <code>{event.chat_id}</code>", parse_mode="html")

        @self.strict_owner_command
        async def execute(event):
            """command -> execute command internally"""
            args: list = await self.get_args(event)
            command = " ".join(args)

            if 'sudo' in args:
                await event.edit('**Error**:\n```.execute command does not support sudo, use .execbash command```', parse_mode='markdown')
                return

            await event.delete()

            try:
                result = self.subprocess.run(command, shell=True, capture_output=True, text=True)
                result_code = os.system(command=command)

                await event.reply(f"**Input**:\n```{command}```", parse_mode='markdown')
                await event.reply(f"**Output**:\n```{result.stdout if result.stdout else 'None'}```\n\n**Result Code**:\n```{result_code}```", parse_mode='markdown')

            except Exception as err:
                await event.reply(f"**Error**:\n```{err if err else 'None'}```", parse_mode='markdown')

        @self.strict_owner_command
        async def execbash(event):
            """command -> execute bash command internally"""
            args: list = await self.get_args(event)
            command: str = " ".join(args)

            await event.delete()

            try:
                process = await self.asyncio.create_subprocess_shell(
                    command,
                    stdout=self.asyncio.subprocess.PIPE,
                    stderr=self.asyncio.subprocess.PIPE
                )

                return_code = await process.wait()

                std_output = await process.stdout.read()
                stderr_output = await process.stderr.read()

                if return_code == 0:
                    await event.reply("**Executed**", parse_mode='markdown')
                    self.log.debug(f"Executed [{std_output=}, {stderr_output=}, {return_code=}]")
                else:
                    await event.reply(f"**Error**:\n```{stderr_output.decode() if stderr_output.decode() else 'None'}```", parse_mode='markdown')

            except Exception as err:
                await event.reply(f"**Error**:\n```{err if err else 'None'}```", parse_mode='markdown')


hLoader()
hMem()
hayes()
