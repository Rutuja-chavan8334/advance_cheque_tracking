# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

"""Sample data that walks one cheque through every status.

Run: bench --site <site> execute advance_cheque_tracking.demo.run
Needs submitted Sales Orders with a Sales Team (pass them in ORDERS).
"""

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe.utils import add_days, today

PASSWORD = "Demo@12345"
ACCOUNTS_USER = "demo.accounts@example.com"
SALES_USERS = {"Amit Joshi": "demo.sales1@example.com", "Priya Desai": "demo.sales2@example.com"}

# order: (cheque number, cheque amount, advance received, what happens next)
ORDERS = {
	"SAL-ORD-2026-00011": ("100001", 20000, 20000, "full_invoice"),
	"SAL-ORD-2026-00012": ("100002", 35000, 0, "nothing"),
	"SAL-ORD-2026-00013": ("100003", 25000, 25000, "advance_invoice"),
	"SAL-ORD-2026-00014": ("100004", 15000, 0, "full_invoice_and_return"),
	"SAL-ORD-2026-00015": ("100005", 40000, 0, "nothing"),
}


def run():
	create_users()
	for sales_order, (number, amount, advance, outcome) in ORDERS.items():
		if frappe.db.exists("Advance Cheque", {"sales_order": sales_order}):
			continue
		if advance:
			receive_advance(sales_order, advance)
		cheque = create_cheque(sales_order, number, amount)
		OUTCOMES[outcome](sales_order, cheque)
	frappe.db.commit()


def create_users():
	create_user(ACCOUNTS_USER, "Demo Accounts")
	for sales_person, email in SALES_USERS.items():
		create_user(email, f"Demo {sales_person}")
		link_sales_person(sales_person, email)


def create_user(email, first_name):
	if frappe.db.exists("User", email):
		return
	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": first_name,
			"send_welcome_email": 0,
			"new_password": PASSWORD,
		}
	)
	user.insert(ignore_permissions=True)


def link_sales_person(sales_person, email):
	if frappe.db.get_value("Sales Person", sales_person, "employee"):
		return
	employee = frappe.get_doc(
		{
			"doctype": "Employee",
			"first_name": sales_person,
			"gender": "Male",
			"date_of_birth": "1990-01-01",
			"date_of_joining": "2024-01-01",
			"company": frappe.db.get_single_value("Global Defaults", "default_company"),
			"user_id": email,
		}
	).insert(ignore_permissions=True)
	frappe.db.set_value("Sales Person", sales_person, "employee", employee.name)


def receive_advance(sales_order, amount):
	payment = get_payment_entry("Sales Order", sales_order, party_amount=amount)
	payment.mode_of_payment = "Cheque"
	payment.reference_no = f"ADV-{sales_order[-5:]}"
	payment.reference_date = today()
	payment.insert(ignore_permissions=True)
	payment.submit()


def create_cheque(sales_order, number, amount):
	return frappe.get_doc(
		{
			"doctype": "Advance Cheque",
			"sales_order": sales_order,
			"cheque_number": number,
			"cheque_amount": amount,
			"cheque_issue_date": add_days(today(), -10),
			"accounts_responsible_person": ACCOUNTS_USER,
		}
	).insert(ignore_permissions=True)


def invoice(sales_order, fraction=1):
	"""Invoice the whole order, or a share of it by billing only the first item rows."""
	doc = make_sales_invoice(sales_order)
	if fraction < 1:
		doc.items = doc.items[: max(1, int(len(doc.items) * fraction))]
	doc.allocate_advances_automatically = 1
	doc.insert(ignore_permissions=True)
	doc.submit()
	return doc


def full_invoice(sales_order, cheque):
	invoice(sales_order)


def advance_invoice(sales_order, cheque):
	"""Bill only what the advance covers: the order stays partly unbilled."""
	doc = make_sales_invoice(sales_order)
	advance = frappe.db.get_value("Sales Order", sales_order, "advance_paid")
	item = doc.items[0]
	item.qty = advance / item.rate
	doc.allocate_advances_automatically = 1
	doc.insert(ignore_permissions=True)
	doc.submit()


def full_invoice_and_return(sales_order, cheque):
	invoice(sales_order)
	frappe.get_doc("Advance Cheque", cheque.name).mark_returned(today(), "Collected by hand")


def nothing(sales_order, cheque):
	pass


OUTCOMES = {
	"nothing": nothing,
	"full_invoice": full_invoice,
	"advance_invoice": advance_invoice,
	"full_invoice_and_return": full_invoice_and_return,
}
