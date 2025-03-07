from chat.chat_channel_management.doctype.chat_channel_member.chat_channel_member import (
	on_doctype_update,
)


def execute():
	# Indexing all Chat Channel Members
	on_doctype_update()
