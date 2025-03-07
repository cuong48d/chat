# Copyright (c) 2024, The Commit Company (Algocode Technologies Pvt. Ltd.) and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestChatWorkspace(UnitTestCase):
	"""
	Unit tests for ChatWorkspace.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestChatWorkspace(IntegrationTestCase):
	"""
	Integration tests for ChatWorkspace.
	Use this class for testing interactions between multiple components.
	"""

	def test_create_workspace_member_for_owner(self):
		"""
		Test that when a workspace is created, a member is created for the owner.
		"""

		workspace = frappe.get_doc(
			{
				"doctype": "Chat Workspace",
				"workspace_name": "Test Workspace",
				"type": "Public",
			}
		)

		workspace.insert()

		member = frappe.get_doc(
			"Chat Workspace Member", {"workspace": workspace.name, "user": workspace.owner}
		)
		self.assertTrue(member.is_admin)

		workspace.delete()

	def test_delete_workspace(self):
		"""
		Test that when a workspace is deleted, all its members and channels are also deleted.
		"""
		workspace = frappe.get_doc(
			{
				"doctype": "Chat Workspace",
				"workspace_name": "Test Workspace",
				"type": "Public",
			}
		)

		workspace.insert()

		member = frappe.get_doc(
			"Chat Workspace Member", {"workspace": workspace.name, "user": workspace.owner}
		)

		# Create a channel
		channel = frappe.get_doc(
			{
				"doctype": "Chat Channel",
				"channel_name": "Test Channel",
				"workspace": workspace.name,
			}
		)

		channel.insert()

		workspace.delete()

		self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, "Chat Channel", channel.name)
		self.assertRaises(
			frappe.DoesNotExistError, frappe.get_doc, "Chat Workspace Member", member.name
		)
