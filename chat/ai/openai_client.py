import frappe
from frappe import _
from openai import OpenAI


def get_open_ai_client():
	"""
	Get the OpenAI client
	"""

	chat_settings = frappe.get_cached_doc("Chat Settings")

	if not chat_settings.enable_ai_integration:
		frappe.throw(_("AI Integration is not enabled"))

	openai_api_key = chat_settings.get_password("openai_api_key")

	if chat_settings.openai_project_id:
		client = OpenAI(
			organization=chat_settings.openai_organisation_id,
			project=chat_settings.openai_project_id,
			api_key=openai_api_key,
		)

		return client

	else:
		client = OpenAI(api_key=openai_api_key, organization=chat_settings.openai_organisation_id)

		return client
