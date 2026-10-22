# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today

from advance_cheque_tracking.tests.utils import SALES_EMAIL, make_cheque, make_order

IGNORE_TEST_RECORD_DEPENDENCIES = ["Sales Order", "User", "Customer", "Sales Person", "Company"]


class TestAdvanceCheque(IntegrationTestCase):
	def setUp(self):
		self.order = make_order()

	def test_defaults_from_sales_order(self):
		cheque = make_cheque(self.order)
		self.assertEqual(cheque.customer, self.order.customer)
		self.assertEqual(cheque.sales_person_user, SALES_EMAIL)
		self.assertEqual(cheque.cheque_status, "Issued")

	def test_amount_must_be_positive(self):
		with self.assertRaises(frappe.ValidationError):
			make_cheque(self.order, amount=0)

	def test_duplicate_cheque_number_is_rejected(self):
		make_cheque(self.order)
		with self.assertRaises(frappe.DuplicateEntryError):
			make_cheque(self.order)

	def test_unsubmitted_sales_order_is_rejected(self):
		draft = make_order()
		draft.cancel()
		with self.assertRaises(frappe.ValidationError):
			make_cheque(draft)

	def test_mark_returned_sets_date_and_clears_alerts(self):
		cheque = make_cheque(self.order)
		cheque.mark_return_pending()
		self.assertEqual(self.unread_alerts(cheque), 2)

		cheque.mark_returned(today(), "Collected")
		cheque.reload()
		self.assertEqual(cheque.cheque_status, "Returned")
		self.assertEqual(str(cheque.actual_return_date), today())
		self.assertEqual(self.unread_alerts(cheque), 0)

	def test_return_date_cannot_precede_issue_date(self):
		cheque = make_cheque(self.order)
		with self.assertRaises(frappe.ValidationError):
			cheque.mark_returned(add_days(today(), -30))

	def unread_alerts(self, cheque):
		return frappe.db.count(
			"Notification Log", {"document_type": "Advance Cheque", "document_name": cheque.name, "read": 0}
		)
