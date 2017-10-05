from os import path, getcwd
import json
import re
from random import randint

# noinspection PyPackageRequirements
from discord import Game, Embed, ChannelType
# noinspection PyPackageRequirements
from discord.ext.commands import Bot

from bot.config import CONFIG

PARENTS = [
	'202163416083726338',  # _HellPie
	'225511609567543297',  # Kirei
	'210279248685039616'  # Amanda.
]
ADORABLE_PEOPLE = [
	'202163416083726338',  # _HellPie
	'225511609567543297',  # Kirei
	'245997507606216704',  # sejin.
	'210279248685039616'  # Amanda.
]
ZANTOMODE_PEOPLE = ADORABLE_PEOPLE + [
	'172331493828460545',  # zanto
	'88792744587169792'  # SakuraJinkyu
]
MERCY_MAINS = [
	'245997507606216704',  # sejin.
	'117349345296121864',  # Halo
	'296120625972379648',  # KrisPbaecon
	'338851988785725441'  # Pastelle
]
LESSER_CREATURES = [
	'228162606580367370',  # Sageth
	'280096430356430848'  # Pmik
]
GUILDS_BLACKLIST = []

CHANCE_FACTOR = 1  # 20%

REPLIES_STATUS = True

SIMULATE_USER = None
SIMULATE_COUNT = 0

ZANTOCONF = {}
BRIDGECONF = {}

bot = Bot(CONFIG.get(section='BOT', option='PREFIX').split(' '), description=CONFIG['BOT']['DESCRIPTION'])


@bot.event
async def on_ready():
	print('\n#------------------------------------------------------------------------------#')
	print(f'\tLOGIN: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})')
	print('#------------------------------------------------------------------------------#\n')


@bot.event
async def on_message(message):
	def match(_expr):
		return re.compile(_expr, re.IGNORECASE).match(message.content)
	
	_file = path.join(path.realpath(getcwd()), 'assets', 'bridge_conf.json')
	if not path.exists(_file):
		with open(_file, 'w+') as bridge_conf:
			json.dump({}, bridge_conf)
	global BRIDGECONF
	with open(_file, 'r') as bridge_conf:
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
	global SIMULATE_USER
	global SIMULATE_COUNT
	if SIMULATE_USER is not None and SIMULATE_COUNT > 0:
		author = await bot.get_user_info(SIMULATE_USER)
		SIMULATE_COUNT -= 1
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
			reply = 'ily too sweetheart <:calvinLOVE:349646699897159682>'
		elif author.id in MERCY_MAINS:
			reply = 'cute angel main, ily too \\*-\\*'
		elif author.id == '157725308127150081':  # Bjorn
			reply = 'ily too darlin\' c:'
		elif author.id == '133006275305930753':  # Lotus
			reply = 'Same, but Id love you more if you switched off widow...'
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
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:calvinHug:\d+>'):
		final_emote = ''
		if author.id in PARENTS:
			final_emote = ' <:sinaLove:349646763860426752>'
		elif author.id in ADORABLE_PEOPLE:
			final_emote = ' <:moon2cute:316630780313075712>'
		reply = f'<@{author.id}> <:jay3hugged:332946887202308097>{final_emote}'
	elif match('^(((@?(Not)?Hime)|(<@!311154146969518083>))|(@auto-reply-bot#9347)) ?<:jay3hugged:\d+>'):
		final_emote = ''
		if author.id in PARENTS:
			final_emote = ' <:sinaLove:349646763860426752>'
		elif author.id in ADORABLE_PEOPLE:
			final_emote = ' <:moon2cute:316630780313075712>'
		reply = f'<@{author.id}> <:calvinHug:326950539524964352>{final_emote}'
	else:
		await bot.process_commands(message)
		return
	if reply is not None:
		return await bot.send_message(message.channel, reply)


@bot.command(pass_context=True)
async def zantoconf(ctx, *body):
	if ctx.message.server.id in GUILDS_BLACKLIST:
		return
	if ctx.message.author.id not in PARENTS and ctx.message.author.id not in ZANTOMODE_PEOPLE:
		return
	args = ' '.join(body).split(' as ')
	if len(args) < 2:
		return await bot.send_message(ctx.message.channel, 'Need something like \':$zantoconf <character> as <emote>\'')
	ZANTOCONF[args[0]] = args[1]
	with open(path.join(path.realpath(getcwd()), 'assets', 'zanto_conf.json'), 'w+') as zanto_conf:
		json.dump(ZANTOCONF, zanto_conf)
	return await bot.send_message(ctx.message.channel, f'{args[0]} => {args[1]} - Configured')


@bot.command(pass_context=True)
async def zantomode(ctx, *sentence):
	if ctx.message.server.id in GUILDS_BLACKLIST:
		return
	if ctx.message.author.id not in PARENTS and ctx.message.author.id not in ZANTOMODE_PEOPLE:
		return
	global ZANTOCONF
	_file = path.join(path.realpath(getcwd()), 'assets', 'zanto_conf.json')
	if not path.exists(_file):
		with open(_file, 'w+') as zanto_conf:
			json.dump({}, zanto_conf)
	with open(_file, 'r') as zanto_conf:
		ZANTOCONF = json.load(zanto_conf)
	# space = '<:regional_indicator_none:336187638514057226> '  # Custom emoji for an empty blue square
	space = '<:jay3thinking:332958429083729933> '
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
async def himemod():
	pass


@himemod.command(pass_context=True)
async def config(ctx, flag, value, *extras):
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
		global BRIDGECONF
		if value is not None:
			for args in extras:
				kvpair = args.split(':')
				if kvpair[0] == 'destination':
					BRIDGECONF[value] = kvpair[1]
				if kvpair[0] == 'stop' and value in BRIDGECONF:
					del BRIDGECONF[value]
			with open(path.join(path.realpath(getcwd()), 'assets', 'bridge_conf.json'), 'w+') as bridge_conf:
				json.dump(BRIDGECONF, bridge_conf)
	return await bot.send_message(
		ctx.message.channel,
		'Updated: `{}` to `{}`{}'.format(flag, value, f'with extras `{extras}`' if len(extras) > 0 else '')
	)


@himemod.command(pass_context=True)
async def debug(ctx, action, channel, *extras):
	async def log(_channel, _message):
		if isinstance(_channel, str):
			_channel = bot.get_channel(_channel)
		print(f'{_channel.server.name}{_channel.name} -> {_message}')
		return await bot.send_message(_channel, embed=Embed(description=_message))
	
	if ctx.message.author.id != '202163416083726338':  # HellPie
		return
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
