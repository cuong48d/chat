import frappe


def track_channel_visit(channel_id, user=None, commit=False, publish_event_for_user=False):
	"""
	Track the last visit of the user to the channel.
	If the user is not a member of the channel, create a new member record
	"""

	if not user:
		user = frappe.session.user

	# Get the channel member record
	channel_member = get_channel_member(channel_id, user)

	now = frappe.utils.now()

	if channel_member:
		# Update the last visit
		frappe.db.set_value("Chat Channel Member", channel_member["name"], "last_visit", now)

	# Else if the user is not a member of the channel and the channel is open, create a new member record
	elif frappe.get_cached_value("Chat Channel", channel_id, "type") == "Open":
		frappe.get_doc(
			{
				"doctype": "Chat Channel Member",
				"channel_id": channel_id,
				"user_id": frappe.session.user,
				"last_visit": now,
			}
		).insert()

	# Need to commit the changes to the database if the request is a GET request
	if commit:
		frappe.db.commit()  # nosempgrep

	if publish_event_for_user:
		frappe.publish_realtime(
			"chat:unread_channel_count_updated",
			{"channel_id": channel_id, "sent_by": frappe.session.user, "last_message_timestamp": now},
			user=user,
		)


# Workspace Members
def get_workspace_members(workspace_id: str):
	"""
	Gets all members of a workspace from the cache
	"""
	cache_key = f"chat:workspace_members:{workspace_id}"

	data = frappe.cache().get_value(cache_key)
	if data:
		return data

	members = frappe.db.get_all(
		"Chat Workspace Member",
		filters={"workspace": workspace_id},
		fields=["name", "user", "is_admin"],
	)

	data = {member.user: member for member in members}
	frappe.cache().set_value(cache_key, data)
	return data


def delete_workspace_members_cache(workspace_id: str):
	cache_key = f"chat:workspace_members:{workspace_id}"
	frappe.cache().delete_value(cache_key)


def get_workspace_member(workspace_id: str, user: str = None) -> dict:
	"""
	Get the workspace member ID
	"""
	if not user:
		user = frappe.session.user

	return get_workspace_members(workspace_id).get(user, None)


def is_workspace_member(workspace_id: str, user: str = None) -> bool:
	"""
	Check if a user is a member of a workspace
	"""
	if not user:
		user = frappe.session.user

	all_members = get_workspace_members(workspace_id)

	return user in all_members


def get_channel_members(channel_id: str):
	"""
	Gets all members of a channel from the cache as a map - also includes the type of the user
	"""
	cache_key = f"chat:channel_members:{channel_id}"

	data = frappe.cache().get_value(cache_key)
	if data:
		return data

	chat_channel_member = frappe.qb.DocType("Chat Channel Member")
	chat_user = frappe.qb.DocType("Chat User")

	query = (
		frappe.qb.from_(chat_channel_member)
		.join(chat_user)
		.on(chat_channel_member.user_id == chat_user.name)
		.select(
			chat_channel_member.name,
			chat_channel_member.user_id,
			chat_channel_member.is_admin,
			chat_channel_member.allow_notifications,
			chat_user.type,
		)
		.where(chat_channel_member.channel_id == channel_id)
	)

	members = query.run(as_dict=True)

	data = {member.user_id: member for member in members}
	frappe.cache().set_value(cache_key, data)
	return data


def delete_channel_members_cache(channel_id: str):
	cache_key = f"chat:channel_members:{channel_id}"
	frappe.cache().delete_value(cache_key)

	frappe.publish_realtime(
		"channel_members_updated",
		{"channel_id": channel_id},
		room="all",
		after_commit=True,
	)


def get_channel_member(channel_id: str, user: str = None) -> dict:
	"""
	Get the channel member ID
	"""

	if not user:
		user = frappe.session.user

	all_members = get_channel_members(channel_id)

	return all_members.get(user, None)


def is_channel_member(channel_id: str, user: str = None) -> bool:
	"""
	Check if a user is a member of a channel
	"""
	if not user:
		user = frappe.session.user

	return user in get_channel_members(channel_id)


def get_chat_user(user_id: str) -> str:
	"""
	Get the Chat User ID of a user
	"""
	# TODO: Run this via cache
	return frappe.db.get_value("Chat User", {"user": user_id}, "name")


def get_thread_reply_count(thread_id: str) -> int:
	"""
	Get the number of replies in a thread
	"""
	return frappe.cache().hget(
		"chat:thread_reply_count",
		thread_id,
		lambda: frappe.db.count("Chat Message", {"channel_id": thread_id}),
	)


def clear_thread_reply_count_cache(thread_id: str):
	"""
	Clear the thread reply count cache
	"""
	frappe.cache().hdel("chat:thread_reply_count", thread_id)
