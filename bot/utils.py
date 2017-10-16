from enum import IntEnum
from discord import Embed


class OpStatus(IntEnum):
	SUCCESS = 0x2ECC71,
	FAILURE = 0xc0392B,
	WARNING = 0xf39C12,
	NONE = -1


def build_embed(ctx, desc: str, title: str = '', status: OpStatus = OpStatus.SUCCESS) -> Embed:
	name = ctx.message.server.me.nick if ctx.message.server.me.nick is not None else ctx.bot.user.name
	embed = Embed(
		title=title,
		description=desc,
		color=status.value if status is not None and status is not -1 else None if status is -1 else OpStatus.WARNING
	)
	embed.set_author(name=name, icon_url=ctx.bot.user.avatar_url)
	return embed
