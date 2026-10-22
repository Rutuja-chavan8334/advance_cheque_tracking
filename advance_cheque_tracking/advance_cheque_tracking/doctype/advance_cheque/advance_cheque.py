# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, today

from advance_cheque_tracking.notifications import ChequeNotifier, get_sales_person_user


class AdvanceCheque(Document):
	def validate(self):
		if not self.accounts_responsible_person:
			self.accounts_responsible_person = frappe.db.get_single_value(
				"Advance Cheque Settings", "default_accounts_responsible_person"
			)

		self.validate_sales_order()
		self.validate_amount()
		self.validate_duplicate()
		self.validate_return_date()
		self.set_sales_person()
		self.set_return_pending_since()

	def on_update(self):
		if not self.has_value_changed("cheque_status"):
			return

		notifier = ChequeNotifier(self)
		if self.cheque_status == "Return Pending":
			notifier.notify_return_pending()
		else:
			notifier.clear()

	def validate_sales_order(self):
		order = frappe.db.get_value("Sales Order", self.sales_order, ["docstatus", "customer"], as_dict=True)
		if not order:
			return
		if order.docstatus != 1:
			frappe.throw(_("Sales Order {0} is not submitted.").format(self.sales_order))
		if self.customer and self.customer != order.customer:
			frappe.throw(_("Customer does not match Sales Order {0}.").format(self.sales_order))

	def validate_amount(self):
		if flt(self.cheque_amount) <= 0:
			frappe.throw(_("Cheque Amount must be greater than zero."))

	def validate_duplicate(self):
		duplicate = frappe.db.exists(
			"Advance Cheque",
			{"sales_order": self.sales_order, "cheque_number": self.cheque_number, "name": ("!=", self.name)},
		)
		if duplicate:
			frappe.throw(
				_("Cheque {0} is already recorded for {1} in {2}.").format(
					self.cheque_number, self.sales_order, duplicate
				),
				frappe.DuplicateEntryError,
			)

	def validate_return_date(self):
		if self.cheque_status != "Returned":
			self.actual_return_date = None
			return

		if not self.actual_return_date:
			frappe.throw(_("Actual Return Date is required when the cheque is Returned."))
		if getdate(self.actual_return_date) < getdate(self.cheque_issue_date):
			frappe.throw(_("Actual Return Date cannot be before the Cheque Issue Date."))

	def set_sales_person(self):
		if not self.sales_person:
			self.sales_person = frappe.db.get_value(
				"Sales Team", {"parent": self.sales_order, "parenttype": "Sales Order"}, "sales_person"
			)

		self.sales_person_user = get_sales_person_user(self.sales_person)
		if self.sales_person and not self.sales_person_user:
			frappe.msgprint(
				_("Sales Person {0} has no linked User. Only the Accounts person will be notified.").format(
					self.sales_person
				),
				indicator="orange",
				alert=True,
			)

	def set_return_pending_since(self):
		if self.cheque_status == "Return Pending" and not self.return_pending_since:
			self.return_pending_since = today()
		elif self.cheque_status == "Issued":
			self.return_pending_since = None

	@frappe.whitelist()
	def mark_return_pending(self):
		self.cheque_status = "Return Pending"
		self.save()

	@frappe.whitelist()
	def mark_returned(self, return_date=None, remarks=None):
		self.cheque_status = "Returned"
		self.actual_return_date = return_date or today()
		if remarks:
			self.remarks = f"{self.remarks}\n{remarks}" if self.remarks else remarks
		self.save()


@frappe.whitelist()
def get_sales_order_defaults(sales_order):
	sales_person = frappe.db.get_value(
		"Sales Team", {"parent": sales_order, "parenttype": "Sales Order"}, "sales_person"
	)
	return {"sales_person": sales_person}
