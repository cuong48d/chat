import frappe


def execute():
	"""Creating Chat Users for existing users with the "Chat User" role."""

	# In Chat v1.2, we introduced the "Chat User" doctype.
	#  Reference: [#427](https://github.com/The-Commit-Company/Chat/issues/427)
	# This doctype is used to store the user's profile picture and full name.
	# However, existing users with the "Chat User" role will not have a corresponding Chat User record.
	# This patch creates Chat Users for all users with the "Chat User" role.
	users = frappe.get_all(
		"User",
		filters=[["name", "not in", ["Guest"]], ["Has Role", "role", "=", "Chat User"]],
	)

	for user in users:
		if not frappe.db.exists("Chat User", {"user": user.name}):
			chat_user = frappe.new_doc("Chat User")
			chat_user.user = user.name
			chat_user.insert()
