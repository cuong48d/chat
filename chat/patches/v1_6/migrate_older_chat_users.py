import frappe


def execute():
	"""
	Migrate Chat User to have the "type" field set for older Chat Users
	"""

	users = frappe.get_all("Chat User", filters={"type": ["in", ["", None]]}, pluck="name", limit=5)

	for user in users:
		frappe.db.set_value("Chat User", user, "type", "User")

	frappe.db.commit()
