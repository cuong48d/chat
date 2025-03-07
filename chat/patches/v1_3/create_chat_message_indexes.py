from chat.chat_messaging.doctype.chat_message.chat_message import on_doctype_update


def execute():
	# Indexing all Chat Messages
	on_doctype_update()
