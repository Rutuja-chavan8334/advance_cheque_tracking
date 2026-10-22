# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import escape_html, fmt_money, get_url_to_form, today


class ChequeNotifier:
	def __init__(self, cheque):
		self.cheque = cheque

	def get_users(self):
		users = [self.cheque.accounts_responsible_person, self.cheque.sales_person_user]
		return get_enabled_users(users)

	def notify_return_pending(self):
		cheque = self.cheque
		subject = _("Collect advance cheque {0} from {1}").format(cheque.cheque_number, cheque.customer)

		for user in self.get_users():
			frappe.get_doc(
				{
					"doctype": "Notification Log",
					"type": "Alert",
					"for_user": user,
					"from_user": frappe.session.user,
					"subject": escape_html(subject),
					"document_type": "Advance Cheque",
					"document_name": cheque.name,
					"email_content": get_cheque_table([cheque.as_dict()]),
				}
			).insert(ignore_permissions=True)

			frappe.publish_realtime(
				"advance_cheque_return_pending",
				{
					"name": cheque.name,
					"cheque_number": cheque.cheque_number,
					"customer": cheque.customer,
					"sales_order": cheque.sales_order,
					"amount": fmt_money(cheque.cheque_amount),
				},
				user=user,
				after_commit=True,
			)

		frappe.db.set_value("Advance Cheque", cheque.name, "last_reminded_on", today(), update_modified=False)

	def clear(self):
		frappe.db.set_value(
			"Notification Log",
			{"document_type": "Advance Cheque", "document_name": self.cheque.name, "read": 0},
			"read",
			1,
			update_modified=False,
		)
		frappe.db.set_value("Advance Cheque", self.cheque.name, "last_reminded_on", None, update_modified=False)


def send_digest(user, cheques):
	frappe.get_doc(
		{
			"doctype": "Notification Log",
			"type": "Alert",
			"for_user": user,
			"subject": _("{0} advance cheque(s) still to be collected").format(len(cheques)),
			"link": frappe.utils.get_url("/app/advance-cheque?cheque_status=Return%20Pending"),
			"email_content": get_cheque_table(cheques),
		}
	).insert(ignore_permissions=True)


def get_sales_person_user(sales_person):
	employee = frappe.db.get_value("Sales Person", sales_person, "employee") if sales_person else None
	return frappe.db.get_value("Employee", employee, "user_id") if employee else None


def get_enabled_users(users):
	users = {user for user in users if user}
	return [user for user in users if frappe.db.get_value("User", user, "enabled")]


def get_cheque_table(cheques):
	rows = ""
	for cheque in cheques:
		link = get_url_to_form("Advance Cheque", cheque["name"])
		rows += (
			f"<tr><td><a href='{link}'>{escape_html(cheque['name'])}</a></td>"
			f"<td>{escape_html(cheque.get('customer') or '')}</td>"
			f"<td>{escape_html(cheque.get('sales_order') or '')}</td>"
			f"<td>{escape_html(cheque.get('cheque_number') or '')}</td>"
			f"<td>{fmt_money(cheque.get('cheque_amount') or 0)}</td></tr>"
		)

	return (
		"<table class='table table-bordered'>"
		"<tr><th>Cheque</th><th>Customer</th><th>Sales Order</th><th>Number</th><th>Amount</th></tr>"
		f"{rows}</table>"
	)
