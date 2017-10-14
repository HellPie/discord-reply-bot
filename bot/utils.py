from discord import Embed


def build_embed(ctx, desc: str, title: str = ''):
	name = ctx.message.server.me.nick if ctx.message.server.me.nick is not None else ctx.bot.user.name
	embed = Embed(
		title=title,
		description=desc
	)
	embed.set_author(name=name, icon_url=ctx.bot.user.avatar_url)
	return embed
