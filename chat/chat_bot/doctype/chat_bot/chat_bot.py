# Copyright (c) 2024, The Commit Company and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _
from frappe.model.document import Document

from chat.ai.openai_client import get_open_ai_client
from chat.utils import get_chat_user


class ChatBot(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from chat.chat_ai.doctype.chat_bot_functions.chat_bot_functions import ChatBotFunctions

		allow_bot_to_write_documents: DF.Check
		bot_functions: DF.Table[ChatBotFunctions]
		bot_name: DF.Data
		debug_mode: DF.Check
		description: DF.SmallText | None
		dynamic_instructions: DF.Check
		enable_code_interpreter: DF.Check
		enable_file_search: DF.Check
		image: DF.AttachImage | None
		instruction: DF.LongText | None
		is_ai_bot: DF.Check
		is_standard: DF.Check
		module: DF.Link | None
		openai_assistant_id: DF.Data | None
		chat_user: DF.Link | None
	# end: auto-generated types

	def validate(self):
		if self.is_ai_bot and not self.instruction:
			frappe.throw(_("Please provide an instruction for this AI Agent."))

		self.validate_functions()

	def validate_functions(self):
		if not self.allow_bot_to_write_documents:
			for f in self.bot_functions:
				needs_write = frappe.db.get_value(
					"Chat AI Function", f.function, "requires_write_permissions"
				)
				if needs_write:
					frappe.throw(
						f"This agent is not allowed to write documents. Please remove the function {f.function} or allow the agent to write documents."
					)

	def on_update(self):
		"""
		When a bot is updated, create/update the Chat User for it

		TODO: Generate JSON files when a Standard Bot is created or updated
		"""
		if self.chat_user:
			chat_user = frappe.get_doc("Chat User", self.chat_user)
			chat_user.type = "Bot"
			chat_user.bot = self.name
			chat_user.full_name = self.bot_name
			chat_user.first_name = self.bot_name
			chat_user.user_image = self.image
			chat_user.enabled = 1
			chat_user.save()
		else:
			chat_user = frappe.new_doc("Chat User")
			chat_user.type = "Bot"
			chat_user.bot = self.name
			chat_user.full_name = self.bot_name
			chat_user.first_name = self.bot_name
			chat_user.user_image = self.image
			chat_user.enabled = 1
			chat_user.save()

			self.db_set("chat_user", chat_user.name)

		if self.is_ai_bot:
			if not self.openai_assistant_id:
				self.create_openai_assistant()
			else:
				self.update_openai_assistant()

	def before_insert(self):
		if self.is_ai_bot and not self.openai_assistant_id:
			self.create_openai_assistant()

	def on_trash(self):
		if self.openai_assistant_id:
			self.delete_openai_assistant()

		if self.chat_user:
			frappe.db.set_value("Chat User", self.chat_user, "bot", None)
			self.db_set("chat_user", None)
			frappe.delete_doc("Chat User", self.chat_user)

	def create_openai_assistant(self):
		# Create an OpenAI Assistant for the bot
		client = get_open_ai_client()

		# Sometimes users face an issue with the OpenAI API returning an error for "model_not_found"
		# This is usually because the user has not added funds to their OpenAI account.
		# We need to show this error to the user if the openAI API returns an error for "model_not_found"

		try:
			assistant = client.beta.assistants.create(
				instructions=self.instruction,
				model="gpt-4o",
				name=self.bot_name,
				description=self.description or "",
				tools=self.get_tools_for_assistant(),
			)
		except Exception as e:
			if "model_not_found" in str(e):
				frappe.throw(
					_(
						f"<strong>There was an error creating the agent in OpenAI.</strong><br/>It is possible that your OpenAI account does not have enough funds. Please add funds to your OpenAI account and try again.<br><br/>Error: {e}"
					)
				)
			else:
				frappe.throw(e)

		self.db_set("openai_assistant_id", assistant.id)

	def update_openai_assistant(self):
		# Update the OpenAI Assistant for the bot

		# Additional check because it is being used in Chat AI Function
		if not self.is_ai_bot:
			return

		client = get_open_ai_client()

		assistant = client.beta.assistants.update(
			self.openai_assistant_id,
			instructions=self.instruction,
			name=self.bot_name,
			description=self.description or "",
			tools=self.get_tools_for_assistant(),
			model="gpt-4o",
		)

	def get_tools_for_assistant(self):
		# Add the function to the assistant
		tools = []

		if self.enable_file_search:
			tools.append(
				{
					"type": "file_search",
				}
			)

		if self.enable_code_interpreter:
			tools.append(
				{
					"type": "code_interpreter",
				}
			)

		for f in self.bot_functions:
			function_def = frappe.db.get_value("Chat AI Function", f.function, "function_definition")
			if function_def:
				tools.append({"type": "function", "function": json.loads(function_def)})

		return tools

	def delete_openai_assistant(self):
		# Delete the OpenAI Assistant for the bot
		try:
			client = get_open_ai_client()
			client.beta.assistants.delete(self.openai_assistant_id)
		except Exception:
			frappe.log_error(
				f"Error deleting OpenAI Assistant {self.openai_assistant_id} for bot {self.name}"
			)

	# Chat Bot Methods

	def is_member(self, channel_id: str) -> None | str:
		"""
		Check if the bot is a member of the channel
		Returns None if the bot is not a member of the channel
		Returns the member_id if the bot is a member of the channel
		"""
		member_id = frappe.db.exists(
			"Chat Channel Member", {"channel_id": channel_id, "user_id": self.chat_user}
		)
		if member_id:
			return member_id
		return None

	def add_to_channel(self, channel_id: str) -> str:
		"""
		Add the bot to a channel as a member

		If the bot is already a member of the channel, this function does nothing

		Returns the member_id of the bot in the channel
		"""

		existing_member = self.is_member(channel_id)

		if not existing_member:
			chat_channel_member = frappe.get_doc(
				doctype="Chat Channel Member", user_id=self.chat_user, channel_id=channel_id
			)
			chat_channel_member.insert()
			return chat_channel_member.name
		else:
			return existing_member

	def remove_from_channel(self, channel_id: str) -> None:
		"""
		Remove the bot from a channel as a member
		"""

		existing_member = self.is_member(channel_id)
		if existing_member:
			frappe.delete_doc("Chat Channel Member", existing_member)

	def get_dm_channel_id(self, user_id: str) -> str | None:
		"""
		Get the channel_id of a Direct Message channel with a user
		"""
		# The User's Chat User ID
		user_chat_user = frappe.db.get_value("Chat User", {"user": user_id}, "name")
		if not user_chat_user:
			return None
		channel_name = frappe.db.get_value(
			"Chat Channel",
			filters={
				"is_direct_message": 1,
				"channel_name": [
					"in",
					[self.chat_user + " _ " + user_chat_user, user_chat_user + " _ " + self.chat_user],
				],
			},
		)
		if channel_name:
			return channel_name
		return None

	def send_message(
		self,
		channel_id: str,
		text: str = None,
		link_doctype: str = None,
		link_document: str = None,
		markdown: bool = False,
		notification_name: str = None,
	) -> str:
		"""
		Send a text message to a channel

		channel_id: The channel_id of the channel to send the message to

		You need to provide either text or link_doctype and link_document
		text: The text of the message in HTML format. If markdown is True, the text will be converted to HTML.

		Optional:
		link_doctype: The doctype of the document to link the message to
		link_document: The name of the document to link the message to
		markdown: If True, the text will be converted to HTML.

		Returns the message ID of the message sent
		"""

		if markdown:
			text = frappe.utils.md_to_html(text)
		doc = frappe.get_doc(
			{
				"doctype": "Chat Message",
				"channel_id": channel_id,
				"text": text,
				"message_type": "Text",
				"is_bot_message": 1,
				"bot": self.chat_user,
				"link_doctype": link_doctype,
				"link_document": link_document,
				"notification": notification_name,
			}
		)
		# Bots can probably send messages without permissions? Upto the end user to create bots.
		# Besides sending messages is not a security concern, unauthorized reading of messages is.
		doc.insert(ignore_permissions=True)
		return doc.name

	def create_direct_message_channel(self, user_id: str) -> str:
		"""
		Creates a direct message channel between the bot and a user

		If the channel already exists, returns the channel_id of the existing channel

		Throws an error if the user is not a Chat User
		"""
		channel_id = self.get_dm_channel_id(user_id)

		if channel_id:
			return channel_id
		else:
			# The user's chat_user document
			user_chat_user = get_chat_user(user_id)
			if not user_chat_user:
				frappe.throw(f"User {user_id} is not added as a Chat User")
			channel = frappe.get_doc(
				{
					"doctype": "Chat Channel",
					"channel_name": self.chat_user + " _ " + user_chat_user,
					"is_direct_message": 1,
				}
			)
			channel.flags.is_created_by_bot = True
			channel.insert()
			return channel.name

	def send_direct_message(
		self,
		user_id: str,
		text: str = None,
		link_doctype: str = None,
		link_document: str = None,
		markdown: bool = False,
		notification_name: str = None,
	) -> str:
		"""
		Send a text message to a user in a Direct Message channel

		user_id: The User's 'name' field to send the message to

		You need to provide either text or link_doctype and link_document
		text: The text of the message in HTML format. If markdown is True, the text will be converted to HTML.

		Optional:
		link_doctype: The doctype of the document to link the message to
		link_document: The name of the document to link the message to
		markdown: If True, the text will be converted to HTML.

		Returns the message ID of the message sent
		"""

		channel_id = self.create_direct_message_channel(user_id)

		if channel_id:
			return self.send_message(
				channel_id, text, link_doctype, link_document, markdown, notification_name
			)

	def get_last_message(self, channel_id: str = None, message_type: str = None) -> Document | None:
		"""
		Gets the last message sent by the bot
		"""
		filters = {"bot": self.name}
		if channel_id is not None:
			filters["channel_id"] = channel_id
		if message_type is not None:
			filters["message_type"] = message_type

		return frappe.get_last_doc("Chat Message", filters=filters, order_by="creation desc")

	def get_previous_messages(
		self, channel_id: str = None, message_type: str = None, date: str = None
	) -> list[str]:
		"""
		Gets the previous messages sent by the bot
		"""
		filters = {"bot": self.name}
		if channel_id is not None:
			filters["channel_id"] = channel_id
		if message_type is not None:
			filters["message_type"] = message_type
		if date is not None:
			filters["creation"] = [">", date]

		return frappe.get_all("Chat Message", filters=filters, order_by="creation desc", pluck="name")
