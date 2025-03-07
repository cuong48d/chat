import click
import frappe
from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to, make_records


def after_install():
	try:
		print("Setting up Chat...")
		add_all_roles_to("Administrator")
		create_chat_user_for_administrator()
		create_general_channel()

		click.secho("Thank you for installing Chat!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/The-Commit-Company/Chat/issues/new"
		click.secho(
			"Installation for Chat failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e


def create_chat_user_for_administrator():

	if not frappe.db.exists("Chat User", {"user": "Administrator"}):
		frappe.get_doc(
			{
				"doctype": "Chat User",
				"user": "Administrator",
				"full_name": "Administrator",
				"type": "User",
			}
		).insert(ignore_permissions=True)


def create_general_channel():
	default_workspace = frappe.get_doc(
		{
			"doctype": "Chat Workspace",
			"workspace_name": "Chat",
			"type": "Public",
		}
	)
	default_workspace.insert(ignore_permissions=True)

	# Make all users a member of this workspace and set them as admins
	users = frappe.get_all("Chat User")
	for user in users:
		try:
			frappe.get_doc(
				{
					"doctype": "Chat Workspace Member",
					"workspace": default_workspace.name,
					"user": user.name,
					"is_admin": True,
				}
			).insert(ignore_permissions=True)
		except Exception as e:
			pass  # nosemgrep

	channel = [
		{
			"doctype": "Chat Channel",
			"name": "general",
			"type": "Open",
			"channel_name": "General",
			"workspace": default_workspace.name,
		}
	]

	make_records(channel)
