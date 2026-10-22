# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase

from advance_cheque_tracking.tests.utils import ACCOUNTS_EMAIL, SALES_EMAIL, invoice, make_cheque, make_order


class TestSalesInvoiceEvents(IntegrationTestCase):
	def setUp(self):
		self.order = make_order(qty=4, rate=1000)
		self.cheque = make_cheque(self.order)

	def status(self):
		return frappe.db.get_value("Advance Cheque", self.cheque.name, "cheque_status")

	def test_partial_invoice_keeps_cheque_issued(self):
		invoice(self.order, qty=1)
		self.assertEqual(self.status(), "Issued")

	def test_final_invoice_moves_cheque_to_return_pending(self):
		invoice(self.order)
		self.assertEqual(self.status(), "Return Pending")
		self.assertIsNotNone(
			frappe.db.get_value("Advance Cheque", self.cheque.name, "return_pending_since")
		)

	def test_responsible_users_get_alert(self):
		invoice(self.order)
		users = frappe.get_all(
			"Notification Log",
			filters={"document_type": "Advance Cheque", "document_name": self.cheque.name},
			pluck="for_user",
		)
		self.assertCountEqual(users, [ACCOUNTS_EMAIL, SALES_EMAIL])

	def test_two_invoices_settle_order(self):
		invoice(self.order, qty=1)
		self.assertEqual(self.status(), "Issued")
		invoice(self.order, qty=3)
		self.assertEqual(self.status(), "Return Pending")

	def test_cancelling_final_invoice_reverts_cheque(self):
		final = invoice(self.order)
		final.cancel()
		self.assertEqual(self.status(), "Issued")

	def test_returned_cheque_is_not_touched_again(self):
		final = invoice(self.order)
		self.cheque.reload()
		self.cheque.mark_returned()
		final.cancel()
		self.assertEqual(self.status(), "Returned")
