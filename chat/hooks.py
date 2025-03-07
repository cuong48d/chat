from . import __version__ as app_version

app_name = "chat"
app_title = "Chat"
app_publisher = "The Commit Company (Algocode Technologies Pvt. Ltd.)"
app_description = "Messaging Application"
app_email = "support@thecommit.company"
app_license = "AGPLv3"
source_link = "https://github.com/The-Commit-Company/Chat"
app_logo = "/assets/chat/chat-logo.png"
app_logo_url = "/assets/chat/chat-logo.png"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "chat.bundle.css"
# app_include_css = "/assets/chat/css/chat.css"
# app_include_js = "/assets/chat/js/chat.js"                 ]
app_include_js = "chat.bundle.js"

add_to_apps_screen = [
	{
		"name": "chat",
		"logo": "/assets/chat/chat-logo.png",
		"title": "Chat",
		"route": "/chat",
		"has_permission": "chat.permissions.check_app_permission",
	}
]


sounds = [
	{
		"name": "chat_notification",
		"src": "/assets/chat/sounds/chat_notification.mp3",
		"volume": 0.2,
	},
]

extend_bootinfo = "chat.boot.boot_session"
# include js, css files in header of web template
# web_include_css = "/assets/chat/css/chat.css"
# web_include_js = "/assets/chat/js/chat.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "chat/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# "methods": "chat.utils.jinja_methods",
# "filters": "chat.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "chat.install.before_install"
after_install = "chat.install.after_install"
# after_sync = ""

# Uninstallation
# ------------

# before_uninstall = "chat.uninstall.before_uninstall"
after_uninstall = "chat.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "chat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		"after_insert": "chat.chat_integrations.doctype.chat_document_notification.chat_document_notification.run_document_notification",
		"on_update": "chat.chat_integrations.doctype.chat_document_notification.chat_document_notification.run_document_notification",
		"on_trash": "chat.chat_integrations.doctype.chat_document_notification.chat_document_notification.run_document_notification",
		"on_cancel": "chat.chat_integrations.doctype.chat_document_notification.chat_document_notification.run_document_notification",
		"on_submit": "chat.chat_integrations.doctype.chat_document_notification.chat_document_notification.run_document_notification",
	},
	"User": {
		"after_insert": "chat.chat.doctype.chat_user.chat_user.add_user_to_chat",
		"on_update": "chat.chat.doctype.chat_user.chat_user.add_user_to_chat",
		"on_trash": "chat.chat.doctype.chat_user.chat_user.remove_user_from_chat",
	},
	"Department": {
		"after_insert": "chat.chat_integrations.controllers.department.after_insert",
		"on_update": "chat.chat_integrations.controllers.department.on_update",
		"on_trash": "chat.chat_integrations.controllers.department.on_trash",
	},
	"Employee": {
		"after_insert": "chat.chat_integrations.controllers.employee.after_insert",
		"on_update": "chat.chat_integrations.controllers.employee.on_update",
		"on_trash": "chat.chat_integrations.controllers.employee.on_trash",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# "all": [
# "chat.tasks.all"
# ],
# "daily": [
# "chat.tasks.daily"
# ],
# "hourly": [
# "chat.tasks.hourly"
# ],
# "weekly": [
# "chat.tasks.weekly"
# ],
# "monthly": [
# "chat.tasks.monthly"
# ],
# }

# Testing
# -------

# before_tests = "chat.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# "frappe.desk.doctype.event.event.get_events": "chat.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "chat.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Chat Message"]


# User Data Protection
# --------------------

# user_data_fields = [
# {
# "doctype": "{doctype_1}",
# "filter_by": "{filter_by}",
# "redact_fields": ["{field_1}", "{field_2}"],
# "partial": 1,
# },
# {
# "doctype": "{doctype_2}",
# "filter_by": "{filter_by}",
# "partial": 1,
# },
# {
# "doctype": "{doctype_3}",
# "strict": False,
# },
# {
# "doctype": "{doctype_4}"
# }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "chat.auth.validate"
# ]

additional_timeline_content = {"*": ["chat.api.chat_message.get_timeline_message_content"]}

website_route_rules = [
	{"from_route": "/chat/<path:app_path>", "to_route": "chat"},
	{"from_route": "/chat_mobile/<path:app_path>", "to_route": "chat"},
]

permission_query_conditions = {
	"Chat Channel": "chat.permissions.chat_channel_query",
	"Chat Message": "chat.permissions.chat_message_query",
	"Chat Poll": "chat.permissions.chat_poll_query",
	"Chat Poll Vote": "chat.permissions.chat_poll_vote_query",
}

has_permission = {
	"Chat Channel": "chat.permissions.channel_has_permission",
	"Chat Channel Member": "chat.permissions.channel_member_has_permission",
	"Chat Message": "chat.permissions.message_has_permission",
	"Chat Poll Vote": "chat.permissions.chat_poll_vote_has_permission",
	"Chat Poll": "chat.permissions.chat_poll_has_permission",
	"Chat User": "chat.permissions.chat_user_has_permission",
	"Chat Workspace Member": "chat.permissions.workspace_member_has_permission",
	"Chat Workspace": "chat.permissions.workspace_has_permission",
}

on_session_creation = "chat.api.user_availability.set_user_active"
on_logout = "chat.api.user_availability.set_user_inactive"

export_python_type_annotations = True

chat_document_link_override = "chat.api.document_link.get_new_app_document_links"
