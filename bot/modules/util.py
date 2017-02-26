import logging

from ..consts import PREFIX
from .module import Module

logging.basicConfig(level=logging.INFO)

class UtilModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        self._initialise_commands()

        logging.info('UtilModule: Initialised!')

    def _initialise_commands(self):
        command = self._modules['command']

        command.register_command(
            'help', self._help,
            '`' + PREFIX + 'help <command>`',
            '`Show help text for <command>`')
        command.register_command(
            'whoami', self._whoami,
            '`' + PREFIX + 'whoami`',
            '`Show user and user bot role`')

    async def _help(self, message, args):
        command = self._modules['command']

        registered_commands = command.registered_commands
        if len(args) == 1:
            command_names = ', '.join([x for x in registered_commands])
            await self.send_message(message, '`Prefix: {}\nCommands: {}`'.format(PREFIX, command_names))
        elif len(args) > 1:
            auth_text = ''
            permissions = command.permissions[args[1]]
            if len(permissions['users']) > 0:
                auth_text += '\nAllowed users: `{}`'.format(', '.join(permissions['users']))
            if len(permissions['roles']) > 0:
                auth_text += '\nAllowed roles: `{}`'.format(', '.join(permissions['roles']))
            await self.send_message(message, '{}:\n{}{}'.format(args[1], registered_commands[args[1]].help(), auth_text))

    async def _whoami(self, message, args):
        display_name = message.author.display_name
        author = str(message.author)
        server_roles = ', '.join([str(x.name) for x in message.author.roles[1:]])
        await self._client.send_message(
            message.channel,
            'You are `{}` \n\nUser: `{}` \nRoles: `{}`'.format(display_name, author, server_roles))

    async def send_message(self, message, args):
        return await self._client.send_message(message.channel, args, tts=message.tts)

    async def edit_message(self, message, args):
        return await self._client.edit_message(message, args)

    async def delete_message(self, message):
        return await self._client.delete_message(message)
