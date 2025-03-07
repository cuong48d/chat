# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ChatUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from chat.chat.doctype.chat_pinned_channels.chat_pinned_channels import ChatPinnedChannels

		availability_status: DF.Literal["", "Available", "Away", "Do not disturb", "Invisible"]
		bot: DF.Link | None
		chat_style: DF.Literal["Simple", "Left-Right"]
		custom_status: DF.Data | None
		enabled: DF.Check
		first_name: DF.Data | None
		full_name: DF.Data
		last_mention_viewed_on: DF.Datetime | None
		pinned_channels: DF.Table[ChatPinnedChannels]
		type: DF.Literal["User", "Bot"]
		user: DF.Link | None
		user_image: DF.AttachImage | None
	# end: auto-generated types

	def autoname(self):
		if self.type == "Bot":
			self.name = self.bot
		else:
			self.name = self.user

	def before_validate(self):
		if self.user:
			self.type = "User"
		if not self.full_name:
			self.full_name = self.first_name

	def validate(self):
		if self.type == "Bot" and not self.bot:
			frappe.throw(_("Bot is mandatory"))

		if self.type == "User" and not self.user:
			frappe.throw(_("User is mandatory"))

	def before_insert(self):
		if self.type != "Bot":
			self.update_photo_from_user()

	def after_insert(self):
		self.invalidate_user_list_cache()

	def on_update(self):
		self.invalidate_user_list_cache()

	def on_trash(self):
		"""
		Remove the Chat User from all channels
		"""
		frappe.db.delete("Chat Channel Member", {"user_id": self.user})

	def after_delete(self):
		"""
		Remove the Chat User role from the user.
		"""
		if self.user:
			user = frappe.get_doc("User", self.user)
			user.flags.ignore_permissions = True
			user.flags.deleting_chat_user = True
			user.remove_roles("Chat User")
			user.save()

		self.invalidate_user_list_cache()

	def invalidate_user_list_cache(self):

		from chat.api.chat_users import get_users

		get_users.clear_cache()

	def update_photo_from_user(self):
		"""
		We need to create a new File record for the user image and attach it to the Chat User record.
		Why not just copy the URL from the User record? Because the URL is not accessible to the Chat User,
		and Frappe creates a duplicate file in the system (that is public) but does not update the URL in the field.
		"""
		user_image = frappe.db.get_value("User", self.user, "user_image")
		if user_image and not self.user_image:
			image_file = frappe.get_doc(
				{
					"doctype": "File",
					"file_url": user_image,
					"attached_to_doctype": "Chat User",
					"attached_to_name": self.user,
					"attached_to_field": "user_image",
					"is_private": 1,
				}
			).insert(ignore_permissions=True)
			self.user_image = image_file.file_url


def add_user_to_chat(doc, method):
	# called when the user is inserted or updated
	# If the auto-create setting is set to True, check if the user is a System user. If yes, then create a Chat User record for the user.
	# Else, check if the user has a Chat User role. If yes, then create a Chat User record for the user if not already created.

	# If the user is already added to Chat, do nothing.
	if not doc.flags.deleting_chat_user:
		if frappe.db.exists("Chat User", {"user": doc.name}):
			# Check if the role is still present. If not, then inactivate the Chat User record.
			has_chat_role = False
			for role in doc.get("roles"):
				if role.role == "Chat User":
					has_chat_role = True
					break

			if has_chat_role:
				chat_user = frappe.get_doc("Chat User", {"user": doc.name})
				if not doc.full_name:
					chat_user.full_name = doc.first_name
				chat_user.enabled = doc.enabled
				chat_user.save(ignore_permissions=True)
			else:
				chat_user = frappe.get_doc("Chat User", {"user": doc.name})
				if not doc.full_name:
					chat_user.full_name = doc.first_name
				chat_user.enabled = 0
				chat_user.save(ignore_permissions=True)
		else:
			# Chat user does not exist.
			# Only create chat user if it exists in the system.
			if frappe.db.exists("User", doc.name):
				# Check if the user is a system user.
				auto_add = False
				if doc.user_type == "System User":
					auto_add = frappe.db.get_single_value("Chat Settings", "auto_add_system_users")

				if auto_add or "Chat User" in [d.role for d in doc.get("roles")]:
					doc.append("roles", {"role": "Chat User"})
					# Create a Chat User record for the user.
					chat_user = frappe.new_doc("Chat User")
					chat_user.user = doc.name
					if not doc.full_name:
						chat_user.full_name = doc.first_name
					chat_user.enabled = doc.enabled
					chat_user.insert(ignore_permissions=True)


def remove_user_from_chat(doc, method):
	# called when the user is deleted
	# If the user is deleted, then delete the Chat User record for the user.
	if frappe.db.exists("Chat User", {"user": doc.name}):
		chat_user = frappe.get_doc("Chat User", {"user": doc.name})
		chat_user.delete(ignore_permissions=True)
