# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

"""Fixtures shared by the Advance Cheque tests. Everything is created inside the test transaction."""

import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe.utils import add_days, today

ACCOUNTS_EMAIL = "act-accounts@example.com"
SALES_EMAIL = "act-sales@example.com"
SALES_PERSON = "ACT Test Sales Person"
ITEM = "ACT-TEST-ITEM"


def make_user(email):
	if frappe.db.exists("User", email):
		return email
	user = frappe.get_doc(
		{"doctype": "User", "email": email, "first_name": email.split("@")[0], "send_welcome_email": 0}
	)
	user.insert(ignore_permissions=True)
	return email


def make_sales_person():
	"""A Sales Person whose Employee is linked to a User."""
	make_user(SALES_EMAIL)
	if frappe.db.exists("Sales Person", SALES_PERSON):
		return SALES_PERSON
	employee = frappe.get_doc(
		{
			"doctype": "Employee",
			"first_name": "ACT Test",
			"gender": "Male",
			"date_of_birth": "1990-01-01",
			"date_of_joining": "2024-01-01",
			"company": frappe.db.get_single_value("Global Defaults", "default_company"),
			"user_id": SALES_EMAIL,
		}
	).insert(ignore_permissions=True)
	frappe.get_doc(
		{
			"doctype": "Sales Person",
			"sales_person_name": SALES_PERSON,
			"parent_sales_person": "Sales Team",
			"employee": employee.name,
		}
	).insert(ignore_permissions=True)
	return SALES_PERSON


def make_item():
	if not frappe.db.exists("Item", ITEM):
		frappe.get_doc(
			{"doctype": "Item", "item_code": ITEM, "item_group": "All Item Groups", "is_stock_item": 0, "stock_uom": "Nos"}
		).insert(ignore_permissions=True)
	return ITEM


def make_order(qty=4, rate=1000):
	"""Submitted Sales Order of qty x rate, with the test Sales Person on its team."""
	order = frappe.get_doc(
		{
			"doctype": "Sales Order",
			"company": frappe.db.get_single_value("Global Defaults", "default_company"),
			"customer": frappe.db.get_value("Customer", {}, "name"),
			"transaction_date": today(),
			"delivery_date": add_days(today(), 7),
			"items": [
				{"item_code": make_item(), "qty": qty, "rate": rate, "delivery_date": add_days(today(), 7)}
			],
			"sales_team": [{"sales_person": make_sales_person(), "allocated_percentage": 100}],
		}
	)
	order.insert(ignore_permissions=True)
	order.submit()
	return order


def make_cheque(order, number="900001", amount=1000, **values):
	make_user(ACCOUNTS_EMAIL)
	return frappe.get_doc(
		{
			"doctype": "Advance Cheque",
			"sales_order": order.name,
			"cheque_number": number,
			"cheque_amount": amount,
			"cheque_issue_date": add_days(today(), -5),
			"accounts_responsible_person": ACCOUNTS_EMAIL,
			**values,
		}
	).insert(ignore_permissions=True)


def invoice(order, qty=None):
	doc = make_sales_invoice(order.name)
	if qty:
		doc.items[0].qty = qty
	doc.insert(ignore_permissions=True)
	doc.submit()
	return doc
