import frappe


def execute():
	# Add rows to Chat Settings for the default workspace mapping for all companies
	chat_settings = frappe.get_doc("Chat Settings")

	if not chat_settings.auto_create_department_channel:
		return

	# Get all companies if they exist - check if ERPNext is installed
	if "erpnext" in frappe.get_installed_apps():
		companies = frappe.get_all("Company", pluck="name")

	for company in companies:
		chat_settings.append(
			"company_workspace_mapping", {"company": company, "chat_workspace": "Chat"}
		)

	chat_settings.save()
