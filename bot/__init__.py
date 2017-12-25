import json
import re
from os import path, getcwd
from random import randint
from typing import Union

from discord import User, Message, Embed, Server, Game, Permissions, Channel, ChannelType, HTTPException, Forbidden, InvalidArgument, NotFound
from discord.ext.commands import Bot, Context, check

from bot.config import CONFIG
from bot.utils import build_embed, OpStatus, permissions

VERSION = '3.5'

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
GUILDS_BLACKLIST = [
	'291290703021998080'  # OW Road to Grandmaster+ (they disabled send msg perm for the bot, I wont waste CPU on reets)
]

REPLIES_STATUS = True

SIMULATE_USER = None
SIMULATE_COUNT = 0

SIMULATE_CONFIG = {
	'USER': None,
	'COUNT': 0
}

ZANTOCONF_PATH = path.join(path.realpath(getcwd()), 'assets', f'{CONFIG["STORAGE"]["ZANTOCONF"]}.json')
ZANTOCONF = {}

ZANTOCONF_BLACKLIST = [' ', '!', '?']

HACKERCONF_PATH = path.join(path.realpath(getcwd()), 'assets', f'{CONFIG["STORAGE"]["HACKERCONF"]}.json')
HACKERCONF = {}

LOG_LEVELS = {
	'LOG': '\N{PAGE FACING UP}',
	'INFO': '\N{BELL}',
	'SUCCESS': '\N{WHITE HEAVY CHECK MARK}',
	'WARNING': '\N{WARNING SIGN}',
	'ERROR': '\N{CROSS MARK}'
}

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
	if not path.exists(HACKERCONF_PATH):
		with open(HACKERCONF_PATH, 'w') as zanto_conf:
			json.dump({}, zanto_conf)
	else:
		with open(HACKERCONF_PATH, 'r') as zanto_conf:
			global HACKERCONF
			HACKERCONF = json.load(zanto_conf)


@bot.event
async def on_command_error(*args):
	pass


@bot.event
async def on_message(message: Message):
	def match(_expr):
		return re.compile(_expr, re.IGNORECASE).match(message.content)
	
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
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:.*Hug:\d+>'):
		hug_emote = '<:calvinHugged:367687722024042497>'
		if author.id in MERCY_MAINS:
			hug_emote = '<:valeHugged:367687799270408202>'
		final_emote = ''
		if author.id in PARENTS:
			final_emote = '<:nomyHeart:367687902433509397>'
		elif author.id in ADORABLE_PEOPLE:
			final_emote = '<:jay3Kiss:367687910436110336>'
		reply = f'<@{author.id}> {hug_emote} {final_emote}'
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:.*Hugged:\d+>'):
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
		c = c.upper()
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


@bot.command(pass_context=True)
@check(lambda ctx: ctx.message.server.id not in GUILDS_BLACKLIST)
async def hackermode(ctx, *sentence):
	message = ' '
	sentence = ' '.join(sentence)
	for c in sentence:
		c = c.upper()
		if c in HACKERCONF:
			message += f'{str(HACKERCONF[c])} '
	if message != ' ':
		return await bot.send_message(ctx.message.channel, message)
	return await bot.send_message(ctx.message.channel, 'Unable to hack message :(')


@bot.group()
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'] or ctx.message.author.id in PARENTS)
async def hime():
	pass


@hime.command(pass_context=True, aliases=['presence'])
async def status(ctx: Context, game: str = None, url: str = None) -> Message:
	is_empty = game is None or game.isspace() or len(game) < 1
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
	is_empty = nick is None or nick.isspace() or len(nick) < 1
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
async def invite(ctx: Context, dest: Union[Channel, Server], time: int = 0, use: int = 0, tmp: bool = False) -> Message:
	options = {
		'max_age': time,
		'max_uses': use,
		'temporary': tmp,
		'unique': True
	}
	try:
		created = await bot.create_invite(destination=dest, options=options)
	except HTTPException:
		if isinstance(dest, Server):
			has_permission = Permissions.create_instant_invite in dest.me.server_permissions
		elif isinstance(dest, Channel):
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
				'server' if isinstance(dest, Server) else 'channel',
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


@hime.group()
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'])
async def feature():
	pass


@feature.command(pass_context=True)
async def replies(ctx: Context, toggle: bool = not REPLIES_STATUS) -> Message:
	global REPLIES_STATUS
	REPLIES_STATUS = toggle
	return await bot.send_message(
		ctx.message.channel,
		embed=build_embed(ctx, f'{"Enabled" if toggle else "Disabled"} replies to messages.')
	)


@bot.group()
@check(lambda ctx: ctx.message.author.id == CONFIG['BOT']['OWNER'])
async def debug():
	pass


@debug.command(pass_context=True)
async def simulate(ctx: Context, user: User = None, count: int = 0) -> Message:
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
				)
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


@debug.command(pass_context=True)
async def log(ctx: Context, dest: str, message: str, level: str = 'INFO') -> Message:
	dest = bot.get_channel(dest)
	if dest is None:
		for server in bot.servers:
			if dest in server.members:
				dest = server.get_member(dest)
				break
	level = level.upper()
	if level not in LOG_LEVELS.keys():
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			f'Log level can be one of: `{LOG_LEVELS.keys()}`',
			status=OpStatus.FAILURE
		))
	prefix = LOG_LEVELS[level]
	if message.isspace() or len(message) < 1:
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			'Cannot send an empty message',
			status=OpStatus.FAILURE
		))
	try:
		await bot.send_message(dest, embed=build_embed(ctx, f'{prefix} - {message}'))
	except InvalidArgument:
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			f'Channel `{dest.name if "name" in dest else "N/A"}` ({dest}) is not a valid destination.',
			status=OpStatus.FAILURE
		))
	except NotFound:
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			f'Channel `{dest.name}` (<#{dest.id}>) could not be found.',
			status=OpStatus.FAILURE
		))
	except Forbidden:
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			'Permission `Send Messages` not granted on server `{}` at channel `{}` (<#{}>).'.format(
				dest.server.name,
				dest.name,
				dest.id
			),
			status=OpStatus.FAILURE
		))
	except HTTPException:
		return await bot.send_message(ctx.message.channel, embed=build_embed(
			ctx,
			'Message operation was denied by the Discord API.',
			status=OpStatus.FAILURE
		))
	return await bot.send_message(ctx.message.channel, embed=build_embed(
		ctx,
		'Send message to server `{}` on channel `{}` (<#{}>).\n\n{}'.format(
			dest.server.name,
			dest.name,
			dest.id,
			message
		)
	))


@debug.command(pass_context=True)
async def broadcast(ctx: Context, message: str, level: str = 'log') -> Message:
	count = 0
	for server in bot.servers:
		for channel in server.channels:
			if channel.type not in [ChannelType.text, ChannelType.group]:
				continue
			if 'general' in channel.name or 'off-topic' in channel.name:
				await log(ctx, channel, message, level)
				count += 1
	return await bot.send_message(
		ctx.message.channel,
		embed=build_embed(ctx, f'Broadcasted message to `{count}` servers.\n\n{message}', status=OpStatus.WARNING)
	)


@debug.group(name='list')
async def data():
	pass


@data.command(pass_context=True)
async def servers(ctx: Context) -> Message:
	name = ctx.message.server.me.nick if ctx.message.server.me.nick is not None else bot.user.name
	template = Embed().set_author(name=name, icon_url=bot.user.avatar_url).to_dict()
	first = template.copy()
	first['title'] = 'List of servers'
	first['description'] = f'Counting `{len(bot.servers)}` servers for this Bot instance.'
	await bot.send_message(ctx.message.channel, embed=Embed.from_data(first))
	embed = Embed.from_data(template)
	for server in bot.servers:
		value = f'- Owner: `{server.owner.name}` ({server.owner.mention} - `{server.owner.id}`)'
		value += f'\n- Created: `{server.created_at.strftime("%Y-%m-%d %H:%M:%S")}`'
		value += f'\n- Icon: `{server.icon_url}`\n'
		value += f'\n- Region: {server.region if isinstance(server.region, str) else server.region.value}'
		value += f'\n- Channels: `{len(server.channels)}`\n- Members: `{len(server.members)}`'
		if len(server.features) > 0:
			value += f'\n- Features: `{server.features}`'
			if 'INVITE_SPLASH' in server.features:
				value += f'- Splash: `{server.splash}`\n- Splash URL: `{server.splash_url}`'
		value += f'\n- Permissions:{permissions(server.me.server_permissions.value)}'
		embed.add_field(name=f'(`{server.id}`) - {server.name}', value=value)
		if len(embed.fields) == 25 or len(str(embed.to_dict())) > 5000:
			await bot.send_message(ctx.message.channel, embed=embed)
			embed = Embed.from_data(template)
	if len(embed.fields) > 0:
		await bot.send_message(ctx.message.channel, embed=embed)
		return await bot.send_message(ctx.message.channel, embed=build_embed(ctx, 'Listed all servers with details.'))


@data.command(pass_context=True)
async def channels(ctx: Context, server_id: str) -> Message:
	server = bot.get_server(server_id)
	name = ctx.message.server.me.nick if ctx.message.server.me.nick is not None else bot.user.name
	template = Embed().set_author(name=name, icon_url=bot.user.avatar_url).to_dict()
	first = template.copy()
	first['title'] = f'List of channels for server `{server.name}` (`{server.id}`)'
	first['description'] = f'Counting `{len(server.channels)}` channels for this server.'
	await bot.send_message(ctx.message.channel, embed=Embed.from_data(first))
	embed = Embed.from_data(template)
	for channel in server.channels:
		embed.add_field(
			name=f'`{channel.name}` ({channel.mention} - `{channel.id}`',
			value=f'{channel.topic}\n\nPermissions:{permissions(channel.permissions_for(server.me).value)}'
		)
		if len(embed.fields) == 25 or len(str(embed.to_dict())) > 5000:
			await bot.send_message(ctx.message.channel, embed=embed)
			embed = Embed.from_data(template)
	if len(embed.fields) > 0:
		await bot.send_message(ctx.message.channel, embed=embed)
		return await bot.send_message(ctx.message.channel, embed=build_embed(ctx, 'Listed all channels with details.'))


def start():
	bot.run(CONFIG.get(section='LOGIN', option='TOKEN'))
