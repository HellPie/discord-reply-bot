import json
import re
from os import path, getcwd
from random import randint
from typing import Union

from discord import User, Message, Embed, Server, Game, Permissions, Channel, PrivateChannel, ChannelType, HTTPException, Forbidden
from discord.ext.commands import Bot, Context, check

from bot.config import CONFIG
from bot.utils import build_embed, OpStatus

PARENTS = [
	'202163416083726338',  # _HellPie
	'225511609567543297',  # Kirei
	'210279248685039616'  # Amanda.
]
ADORABLE_PEOPLE = PARENTS + [
	'245997507606216704',  # sejin.
	'157725308127150081'  # Bjorn
]
ZANTOMODE_PEOPLE = ADORABLE_PEOPLE + [
	'172331493828460545',  # zanto
	'88792744587169792'  # SakuraJinkyu
]
MERCY_MAINS = [
	'210279248685039616',  # Amanda.
	'245997507606216704',  # sejin.
	'117349345296121864',  # Halo
	'296120625972379648',  # KrisPbaecon
	'186626292966359040'  # Pastelle
]
LESSER_CREATURES = [
	'228162606580367370',  # Sageth
	'280096430356430848'  # Pmik
]
GUILDS_BLACKLIST = []

REPLIES_STATUS = True

SIMULATE_USER = None
SIMULATE_COUNT = 0

SIMULATE_CONFIG = {
	'USER': None,
	'COUNT': 0
}

ZANTOCONF_PATH = path.join(path.realpath(getcwd()), 'assets', f'{CONFIG["STORAGE"]["ZANTOCONF"]}.json')
BRIDGECONF_PATH = path.join(path.realpath(getcwd()), 'assets', f'{CONFIG["STORAGE"]["BRIDGECONF"]}.json')

ZANTOCONF = {}
BRIDGECONF = {}

ZANTOCONF_BLACKLIST = [' ', '!', '?']

bot = Bot(CONFIG.get(section='BOT', option='PREFIX').split(' '), description=CONFIG['BOT']['DESCRIPTION'])


@bot.event
async def on_ready():
	print('\n#------------------------------------------------------------------------------#')
	print(f'\tLOGIN: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})')
	print('#------------------------------------------------------------------------------#\n')
	if not path.exists(ZANTOCONF_PATH):
		with open(ZANTOCONF_PATH, 'w') as zanto_conf:
			json.dump({}, zanto_conf)
	else:
		with open(ZANTOCONF_PATH, 'r') as zanto_conf:
			global ZANTOCONF
			ZANTOCONF = json.load(zanto_conf)
	if not path.exists(BRIDGECONF_PATH):
		with open(BRIDGECONF_PATH, 'w') as bridge_conf:
			json.dump({}, bridge_conf)
	else:
		with open(BRIDGECONF_PATH, 'r') as bridge_conf:
			global BRIDGECONF
			BRIDGECONF = json.load(bridge_conf)


@bot.event
async def on_command_error(*args):
	pass


@bot.event
async def on_message(message: Message):
	def match(_expr):
		return re.compile(_expr, re.IGNORECASE).match(message.content)
	
	global BRIDGECONF
	with open(BRIDGECONF_PATH, 'r') as bridge_conf:
		BRIDGECONF = json.load(bridge_conf)
	if message.channel.id in BRIDGECONF:
		print('[{}] {}#{}@{}/{} ->\n{}\n{}\n'.format(
			message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
			message.author.name,
			message.author.discriminator,
			message.channel.server.name,
			message.channel.name,
			message.clean_content,
			[f'{attachment["filename"]} - {attachment["url"]}\n' for attachment in message.attachments]
		))
		if BRIDGECONF[message.channel.id] is not None:
			channel = bot.get_channel(BRIDGECONF[message.channel.id])
			if channel is not None:
				embed = Embed(
					type='rich',
					description=message.clean_content,
					timestamp=message.timestamp,
					colour=0xC9A864
				)
				embed.set_author(
					name=f'{message.author.name}#{message.author.discriminator}',
					icon_url=message.author.avatar_url
				)
				embed.set_footer(
					text=f'{message.channel.server.name}#{message.channel.name}',
					icon_url=message.channel.server.icon_url
				)
				for attachment in message.attachments:
					if attachment['filename'].split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
						embed.set_image(url=attachment['url'])
					else:
						embed.add_field(
							name=f'{attachment["filename"]} ({attachment["size"]}B)',
							value=attachment['url']
						)
				await bot.send_message(channel, embed=embed)
	if message.author.id == bot.user.id or message.author.bot or message.server.id in GUILDS_BLACKLIST:
		return
	if not REPLIES_STATUS and message.author.id not in ADORABLE_PEOPLE:  # Bypass disabled replies for the selected few
		await bot.process_commands(message)
		return
	author = message.author
	if SIMULATE_CONFIG['USER'] is not None and SIMULATE_CONFIG['COUNT'] > 0:
		author = SIMULATE_CONFIG['USER']
		SIMULATE_CONFIG['COUNT'] -= 1
	if match('^ay[y]+$'):
		reply = 'lmao'
	elif match('^wew$'):
		reply = 'lad'
	elif match('^dead$'):
		reply = 'ass'
	elif match('^frigg$'):
		reply = 'off'
	elif match('^oh? ?shit$'):
		reply = 'waddup'
	elif match('^shut ?up!?( @.+#\d+!?)?$') and author.id not in ADORABLE_PEOPLE:
		reply = 'wow, such a Sageth'  # Gone, but I like this too much to remove it
	elif match('^k( .*)?$') and author.id == '170985598297964544':  # DMX
		_random = randint(0, 3)
		if _random == 0:
			reply = 'fuck off DMX'
		elif _random == 1:
			reply = 'Wow... how original...'
		elif _random == 2:
			reply = 'https://cdn.discordapp.com/attachments/313911775500173313/344152842614865923/6e3.png'
		else:
			reply = 'k, nard'
	elif match('^fuck off( [a-z#0-9]+)?$'):
		reply = f'{author.name} has got work to do'
	elif match('^smokes$'):
		reply = 'let\'s go'
	elif match('^safety$'):
		reply = 'always off'
	elif match('^sh?leep ti(ght|te)(,? [a-z#0-9]+)?$'):
		reply = 'don\'t let the genjis bite'
	elif match('^i( ?(ly|((love|luv) (yo)?u))),? (@?(Not)?Hime|(@auto-reply-bot#9347|<@!311154146969518083>))!?$'):
		if author.id == '208286812089614337':  # Obi
			reply = 'ily too obi <3'
		elif author.id == '225511609567543297':  # Kirei
			reply = 'ily a lot mommy :two_hearts: :two_hearts: ^~^'
		elif author.id == '202163416083726338':  # _HellPie
			reply = 'ily too dad <3 <3 ^~^'
		elif author.id == '210279248685039616':  # Amanda.
			reply = 'ily too sweetheart <:valeLove:367687853720731658>'
		elif author.id == '157725308127150081':  # Bjorn
			reply = 'ily too darlin\' c:'
		elif author.id == '133006275305930753':  # Lotus
			reply = 'Same, but Id love you more if you switched off widow...'
		elif author.id in MERCY_MAINS:
			reply = 'cute angel main, ily too \\*-\\*'
		elif author.id in LESSER_CREATURES:
			reply = '1. wow, pedo 2. I have a boyfriend'
		else:
			reply = 'ty, have a nice day darlin\''
	elif match('^suc[ck] an? egg$') and message.author.id not in ADORABLE_PEOPLE:
		reply = 'no, you, eggsucker'
	elif match('^wo[ah]{2}!*$'):
		reply = 'WOW'
	elif match('^no((rmie)|(o+b))s?!*$'):
		reply = 'reeeeeeeeeeeeeeeeeeee, just like obi'
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:(calvin|vale)Hug:\d+>'):
		hug_emote = '<:calvinHugged:367687722024042497>'
		if author.id in MERCY_MAINS:
			hug_emote = '<:valeHugged:367687799270408202>'
		final_emote = ''
		if author.id in PARENTS:
			final_emote = '<:nomyHeart:367687902433509397>'
		elif author.id in ADORABLE_PEOPLE:
			final_emote = '<:jay3Kiss:367687910436110336>'
		reply = f'<@{author.id}> {hug_emote} {final_emote}'
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:(jay3|calvin|vale)Hugged:\d+>'):
		hug_emote = '<:calvinHug:326950539524964352>'
		if author.id in MERCY_MAINS:
			hug_emote = '<:valeHug:367687799488512010>'
		final_emote = ''
		if author.id in PARENTS:
			final_emote = '<:nomyHeart:367687902433509397>'
		elif author.id in ADORABLE_PEOPLE:
			final_emote = '<:jay3Kiss:367687910436110336>'
		reply = f'<@{author.id}> {hug_emote} {final_emote}'
	else:
		await bot.process_commands(message)
		return
	if reply is not None:
		return await bot.send_message(message.channel, reply)


@bot.command(pass_context=True)
@check(lambda ctx: ctx.message.server.id not in GUILDS_BLACKLIST and ctx.message.author.id in ZANTOMODE_PEOPLE)
async def zantoconf(ctx: Context, character: chr, emote: str):
	if character in ZANTOCONF_BLACKLIST:
		return await bot.send_message(ctx.message.channel, f'{character} is special and cannot be changed.')
	ZANTOCONF[str(character)] = emote
	with open(ZANTOCONF_PATH, 'w') as zanto_conf:
		json.dump(ZANTOCONF, zanto_conf)
	return await bot.send_message(ctx.message.channel, f'{character} => {emote} - Configured')


@bot.command(pass_context=True)
@check(lambda ctx: ctx.message.server.id not in GUILDS_BLACKLIST and ctx.message.author.id in ZANTOMODE_PEOPLE)
async def zantomode(ctx, *sentence):
	global ZANTOCONF
	with open(ZANTOCONF_PATH, 'r') as zanto_conf:
		ZANTOCONF = json.load(zanto_conf)
	space = '<:jay3Thinking:368487066755006465> '
	message = ' '
	sentence = ' '.join(sentence)
	for c in sentence:
		c = c.lower()
		if c in ZANTOCONF:
			message += f'{str(ZANTOCONF[c])} '
		elif c == ' ':
			message += space
		elif c == '?':
			message += ':question: '
		elif c == '!':
			message += ':exclamation: '
		elif re.compile('[a-z]', re.IGNORECASE).match(c):
			message += f':regional_indicator_{c.lower()}: '
	if message != ' ':
		return await bot.send_message(ctx.message.channel, message)
	return await bot.send_message(ctx.message.channel, 'Unable to emojify message :(')


@bot.group()
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'] or ctx.message.author.id in PARENTS)
async def hime():
	pass


@hime.command(pass_context=True, aliases=['presence'])
async def status(ctx: Context, game: str = None, url: str = None) -> Message:
	is_empty = game is None or game.isspace()
	is_stream = not is_empty and url is not None and len(url) > 0 and not url.isspace()
	await bot.change_presence(game=None if is_empty else Game(
		name=game,
		type=1 if is_stream else 0,
		url=url if is_stream else None
	))
	return await bot.send_message(ctx.message.channel, embed=build_embed(ctx, '{} status{}{}.'.format(
		'Cleaned' if is_empty else 'Changed',
		'' if is_empty else f' to: `{"Streaming" if is_stream else "Playing"} {game}`',
		f'at `{url}`' if is_stream else ''
	)))


@hime.command(pass_context=True, aliases=['nick'])
async def nickname(ctx: Context, nick: str = None) -> Message:
	is_empty = nick is None or nick.isspace()
	try:
		await ctx.bot.change_nickname(member=ctx.message.server.me, nickname=None if is_empty else nick[:32])
	except Forbidden:
		return await bot.send_message(
			ctx.message.channel,
			embed=build_embed(ctx, 'Permission `Change Nickname` not granted on this server.', status=OpStatus.FAILURE)
		)
	except HTTPException:
		return await bot.send_message(
			ctx.message.channel,
			embed=build_embed(ctx, 'Nickname change denied by the Discord API.', status=OpStatus.FAILURE)
		)
	return await bot.send_message(ctx.message.channel, embed=build_embed(ctx, '{} nickname{}.'.format(
		'Cleaned' if is_empty else 'Changed',
		'' if is_empty else f' to `{nick[:32]}`'
	)))


@hime.command(pass_context=True)
async def invite(ctx: Context, dest: Union[Channel, Server], timer: int = 0, uses: int = 0, temp: bool = False):
	options = {
		'max_age': timer,
		'max_uses': uses,
		'temporary': temp,
		'unique': True
	}
	try:
		created = await bot.create_invite(destination=dest, options=options)
	except HTTPException:
		if dest.__class__ == Server:
			has_permission = Permissions.create_instant_invite in dest.me.server_permissions
		elif dest.__class__ == Channel or dest.__class__ == PrivateChannel:
			has_permission = Permissions.create_instant_invite in dest.permissions_for(dest.server.me)
		else:
			return await bot.send_message(ctx.message.channel, embed=build_embed(
				ctx,
				f'Destination (`{dest}`) is not a valid channel or server.',
				status=OpStatus.FAILURE
			))
		if has_permission:
			return await bot.send_message(
				ctx.message.channel,
				embed=build_embed(ctx, 'Invite creation denied by the Discord API.', status=OpStatus.FAILURE)
			)
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			'Permission `Create Instant Invite` not granted on {} `{}`'.format(
				'server' if dest.__class__ == Server else 'channel',
				dest.name
			),
			status=OpStatus.FAILURE
		))
	return await bot.send_message(ctx.message.channel, embed=build_embed(
		ctx,
		'Created invite: {} to `{}` (can be used `{}` times and expires in `{}` seconds).'.format(
			created.url,
			dest.name,
			created.max_uses,
			created.max_age
		)
	))


@bot.group()
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'])
async def debug():
	pass


@debug.command(pass_context=True)
async def simulate(ctx: Context, user: User = None, count: int = 0):
	if user is None or count < 1:
		if user is not None:
			count = 1
			await bot.send_message(ctx.message.channel, embed=build_embed(
				ctx,
				'Simulation mode will be enabled for one message.',
				status=OpStatus.WARNING
			))
		else:
			user = SIMULATE_CONFIG['USER']
			count = SIMULATE_CONFIG['COUNT']
			SIMULATE_CONFIG['USER'] = None
			SIMULATE_CONFIG['COUNT'] = 0
			if user is None:
				return await bot.send_message(
					ctx.message.channel,
					embed=build_embed(ctx, 'No simulation running.', status=OpStatus.FAILURE)
				)
			return await bot.send_message(ctx.message.channel, embed=build_embed(
				ctx,
				'Stopped simulating user `{}` ({}) with `{}` messages left.'.format(
					user.name,
					user.mention,
					count
				),
				status=OpStatus.SUCCESS
			))
	SIMULATE_CONFIG['USER'] = user
	SIMULATE_CONFIG['COUNT'] = count
	return await bot.send_message(ctx.message.channel, embed=build_embed(
		ctx,
		'Simulating user `{}` ({}) for the next `{}` messages. Use `{}debug simulate` to end prematurely.'.format(
			user.name,
			user.mention,
			count,
			bot.command_prefix[0]
		),
		status=OpStatus.WARNING
	))


@bot.group()
async def himemod():
	pass


@himemod.command(pass_context=True)
async def config(ctx, flag, value=None, *extras):
	if ctx.message.author.id != '202163416083726338':  # HellPie
		return
	if flag == 'STATUS':
		await bot.change_presence(game=Game(
			name=value if value is not None else '',
			url=extras[0] if len(extras) > 0 and extras[0] is not None else '',
			type=1 if len(extras) > 1 and extras[1] == 'STREAM' else 0
		))
	elif flag == 'SIMULATE':
		if value is not None or value is not 'None':
			global SIMULATE_USER
			SIMULATE_USER = value
			user = await bot.get_user_info(SIMULATE_USER)
			value = f'{user.name}#{user.discriminator}'
		for args in extras:
			kvpair = args.split(':')
			global SIMULATE_COUNT
			if kvpair[0] == 'count':
				SIMULATE_COUNT = int(kvpair[1])
			elif kvpair[0] == 'stop':
				SIMULATE_COUNT = 0
	elif flag == 'REPLIES':
		global REPLIES_STATUS
		if value is None or value is '' or value == 'TOGGLE':
			value = 'OFF' if REPLIES_STATUS else 'ON'
		if value == 'ON':
			REPLIES_STATUS = True
		elif value == 'OFF':
			REPLIES_STATUS = False
	elif flag == 'BRIDGE':
		if value is not None:
			for args in extras:
				kvpair = args.split(':')
				if kvpair[0] == 'destination':
					BRIDGECONF[value] = kvpair[1]
				if kvpair[0] == 'stop' and value in BRIDGECONF:
					del BRIDGECONF[value]
			with open(BRIDGECONF_PATH, 'w+') as bridge_conf:
				json.dump(BRIDGECONF, bridge_conf)
	elif flag == 'INVITE':
		options = {
			'max_age': 24,
			'max_uses': 1,
			'temporary': False,
			'unique': False
		}
		try:
			if value is not None:
				for args in extras:
					kvpair = args.split(':')
					options[kvpair[0]] = kvpair[1]
			invite = await bot.create_invite(
				destination=bot.get_channel(value) if value is not None else ctx.message.channel,
				options=options
			)
			return await bot.send_message(ctx.message.channel, 'Generated invite: {}'.format(invite.url))
		except HTTPException as exception:
			return await bot.send_message(ctx.message.channel, 'Unable to create invite: {}'.format(exception))
	return await bot.send_message(
		ctx.message.channel,
		'Updated: `{}` to `{}`{}'.format(flag, value, f'with extras `{extras}`' if len(extras) > 0 else '')
	)


@himemod.command(pass_context=True, alias=['debug'])
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'])
async def old_debug(ctx, action, channel, *extras):
	async def log(_channel, _message):
		if isinstance(_channel, str):
			_channel = bot.get_channel(_channel)
		print(f'{_channel.server.name}{_channel.name} -> {_message}')
		return await bot.send_message(_channel, embed=Embed(description=_message))
	
	if action == 'broadcast':
		return await log(channel, f':bell: - Broadcast message: `{" ".join(extras)}`')
	elif action == 'warn':
		return await log(channel, f':warning: - {" ".join(extras)}')
	elif action == 'error':
		return await log(channel, f':x: - {" ".join(extras)}')
	elif action == 'success':
		return await log(channel, f':white_check_mark: - {" ".join(extras)}')
	elif action == 'wait':
		return await log(channel, f':hourglass_flowing_sand: - {" ".join(extras)}')
	if action == 'log':
		message = ''
		if channel == 'servers':
			for server in bot.servers:
				message += f'**{server.name} (`{server.id}`)**\n'
				for item in server.channels:
					if item.type != ChannelType.voice:
						message += f'* `{item.id}` -> {item.name}\n'
		parsed = ''
		for line in message.split('\n'):
			if len(parsed + line) > 2000:
				await bot.send_message(ctx.message.channel, parsed)
				parsed = f'{line}\n'
			else:
				parsed += f'{line}\n'
		if parsed != '':
			return await bot.send_message(ctx.message.channel, parsed)


def start():
	bot.run(CONFIG.get(section='LOGIN', option='TOKEN'))
