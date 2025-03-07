import frappe


def after_insert(doc, method):
	"""
	Create a new Channel Member if a channel for the department exists
	"""

	if not doc.department or not doc.user_id:
		return

	if not is_department_sync_on():
		return

	channel_id = get_channel_for_department(doc.department)

	if not channel_id:
		return

	chat_user_id = get_chat_user_for_user(doc.user_id)

	if not chat_user_id:
		return

	create_channel_member(channel_id=channel_id, chat_user_id=chat_user_id, employee_id=doc.name)


def on_update(doc, method):
	# Check if department has changed.
	# If it has, we need to remove the channel member from the existing department channel
	# And add it to the new department's channel

	if not doc.user_id:
		return

	if not is_department_sync_on():
		return

	if doc.has_value_changed("user_id"):
		# TODO: Create a member for this user_id
		pass

	if doc.has_value_changed("department"):

		chat_user_id = get_chat_user_for_user(doc.user_id)

		if not chat_user_id:
			return

		old_doc = doc.get_doc_before_save()

		if old_doc and old_doc.department:
			# Remove the employee as a member from the channel
			old_channel = get_channel_for_department(old_doc.department)

			if old_channel:
				frappe.db.delete("Chat Channel Member", {"channel_id": old_channel, "user_id": chat_user_id})

		# Create a new Chat Channel Member for employee
		new_channel = get_channel_for_department(doc.department)

		if new_channel:
			create_channel_member(channel_id=new_channel, chat_user_id=chat_user_id, employee_id=doc.name)


def on_trash(doc, method):
	frappe.db.delete(
		"Chat Channel Member", {"linked_doctype": "Employee", "linked_document": doc.name}
	)


def create_channel_member(channel_id, chat_user_id, employee_id):
	channel_member = frappe.get_doc(
		{
			"doctype": "Chat Channel Member",
			"channel_id": channel_id,
			"user_id": chat_user_id,
			"is_synced": 1,
			"linked_doctype": "Employee",
			"linked_document": employee_id,
		}
	)

	channel_member.insert(ignore_permissions=True)


def get_channel_for_department(department):
	# Check if channel exists for the department
	channel = frappe.get_all(
		"Chat Channel",
		{"linked_doctype": "Department", "linked_document": department},
		pluck="name",
		limit=1,
	)

	if len(channel) == 0:
		return None

	return channel[0]


def get_chat_user_for_user(user_id):
	# Check if Chat User exists for the user id
	chat_user = frappe.get_all("Chat User", {"user": user_id}, pluck="name", limit=1)

	if len(chat_user) == 0:
		return None

	return chat_user[0]


def is_department_sync_on():

	chat_settings = frappe.get_single("Chat Settings")

	if chat_settings.auto_create_department_channel:
		return True
	else:
		return False
