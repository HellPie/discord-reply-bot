from enum import IntEnum
from discord import Embed, Permissions


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


def permissions(perms) -> str:
	def append(perm):
		return f'\n\t- `{perm}`'
	
	value = ''
	permission = Permissions(perms)
	if permission.administrator:
		value += append('administrator')
		return value
	if permission.manage_server:
		value += append('manage_server')
	if permission.manage_channels:
		value += append('manage_channels')
	if permission.manage_messages:
		value += append('manage_messages')
	if permission.manage_roles:
		value += append('manage_roles')
	if permission.manage_emojis:
		value += append('manage_emotes')
	if permission.manage_webhooks:
		value += append('manage_webhooks')
	if permission.view_audit_logs:
		value += append('view_audit_logs')
	if permission.ban_members:
		value += append('ban_members')
	if permission.kick_members:
		value += append('kick_members')
	if permission.create_instant_invite:
		value += append('create_instant_invite')
	if permission.change_nickname:
		value += append('change_nickname')
	if permission.manage_nicknames:
		value += append('manage_nicknames')
	if permission.read_messages:
		value += append('read_messages')
	if permission.read_message_history:
		value += append('read_message_history')
	if permission.send_messages:
		value += append('send_messages')
	if permission.mention_everyone:
		value += append('mention_everyone')
	if permission.add_reactions:
		value += append('add_reactions')
	if permission.embed_links:
		value += append('embed_links')
	if permission.attach_files:
		value += append('attach_files')
	if permission.external_emojis:
		value += append('external_emotes')
	return value
