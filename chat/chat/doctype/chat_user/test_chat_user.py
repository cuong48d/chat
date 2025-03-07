# Copyright (c) 2024, The Commit Company (Algocode Technologies Pvt. Ltd.) and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestChatUser(UnitTestCase):
	"""
	Unit tests for ChatUser.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestChatUser(IntegrationTestCase):
	"""
	Integration tests for ChatUser.
	Use this class for testing interactions between multiple components.
	"""

	def test_user_name(self):
		user = frappe.get_doc("Chat User", "test@example.com")
		self.assertEqual(user.name, "test@example.com")
		self.assertEqual(user.full_name, "_Test")
