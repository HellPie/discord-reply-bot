import re

from discord.ext.commands import Bot

import bot.database
from bot.config import CONFIG

bot = Bot(CONFIG.get(section='BOT', option='PREFIX').split(' '), description=CONFIG['BOT']['DESCRIPTION'])


@bot.event
async def on_message(message):
	if re.compile('^ay[y]+$', re.IGNORECASE).match(message.content):
		return await  bot.send_message(message.channel, 'lmao')
	elif re.compile('^wew$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'lad')
	elif re.compile('^dead$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'ass')
	elif re.compile('^suck$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'an egg @Rednah#2899')
	elif re.compile('^frigg$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'off')
	elif re.compile('^oh? ?shit$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'waddup')
	elif re.compile('^shut ?up!?( @.+#\d+!?)?$', re.IGNORECASE).match(message.content):
		return await bot.send_message(message.channel, 'wow, such a Sageth')
	else:
		await bot.process_commands(message)


@bot.group(check=lambda ctx: ctx.message.author.id == ctx.message.server.owner.id)
async def admin():
	pass


@admin.command(pass_context=True, aliases=['permissions', 'perms'])
async def perm(ctx, mention, action):
	if not action:
		return
	
	result = False
	for role_mention in ctx.message.role_mentions:
		if role_mention.mention == mention:
			result = True
			break
	if not result or not ctx.message.role_mentions:
		return
	
	server_id = int(ctx.message.server.id)
	role_id = int(ctx.message.role_mentions[0].id)
	if re.compile('^add$', re.IGNORECASE).match(action):
		print('Type: {} - Value: {}'.format(type(database.Permission.ADD.value), str(database.Permission.ADD.value)))
		database.add_permission(server_id, role_id, database.Permission.ADD.value)
	elif re.compile('^edit$', re.IGNORECASE).match(action):
		database.add_permission(server_id, role_id, database.Permission.EDIT.value)
	elif re.compile('^delete$', re.IGNORECASE).match(action):
		database.add_permission(server_id, role_id, database.Permission.DELETE.value)
	elif re.compile('^none$', re.IGNORECASE).match(action):
		database.del_permission(server_id, role_id)


def start():
	bot.run(CONFIG.get(section='LOGIN', option='TOKEN'))
