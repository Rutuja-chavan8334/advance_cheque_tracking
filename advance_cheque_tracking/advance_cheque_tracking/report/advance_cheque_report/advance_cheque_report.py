# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, flt, today

FILTER_FIELDS = ["customer", "sales_order", "sales_person", "accounts_responsible_person"]


def execute(filters=None):
	filters = frappe._dict(filters or {})
	data = get_data(filters)
	return get_columns(), data, None, None, get_summary(data)


def get_columns():
	return [
		column("name", "Cheque", "Link", 130, "Advance Cheque"),
		column("sales_order", "Sales Order", "Link", 150, "Sales Order"),
		column("customer", "Customer", "Link", 170, "Customer"),
		column("cheque_number", "Cheque Number", "Data", 120),
		column("cheque_amount", "Amount", "Currency", 120),
		column("cheque_issue_date", "Issue Date", "Date", 100),
		column("cheque_status", "Status", "Data", 120),
		column("return_pending_since", "Return Pending Since", "Date", 130),
		column("days_pending", "Days Pending", "Int", 100),
		column("actual_return_date", "Actual Return Date", "Date", 130),
		column("sales_person", "Sales Person", "Link", 130, "Sales Person"),
		column("accounts_responsible_person", "Accounts Person", "Link", 170, "User"),
		column("remarks", "Remarks", "Data", 200),
	]


def column(fieldname, label, fieldtype, width, options=None):
	return {
		"fieldname": fieldname,
		"label": _(label),
		"fieldtype": fieldtype,
		"width": width,
		"options": options,
	}


def get_data(filters):
	rows = frappe.get_list(
		"Advance Cheque",
		filters=get_filters(filters),
		fields=[
			"name",
			"sales_order",
			"customer",
			"cheque_number",
			"cheque_amount",
			"cheque_issue_date",
			"cheque_status",
			"return_pending_since",
			"actual_return_date",
			"sales_person",
			"accounts_responsible_person",
			"remarks",
		],
		order_by="cheque_issue_date desc, creation desc",
	)

	for row in rows:
		if row.cheque_status == "Return Pending" and row.return_pending_since:
			row.days_pending = date_diff(today(), row.return_pending_since)
	return rows


def get_filters(filters):
	conditions = []

	# "Pending" means every cheque that has not come back yet
	if filters.cheque_status == "Pending":
		conditions.append(["cheque_status", "in", ["Issued", "Return Pending"]])
	elif filters.cheque_status:
		conditions.append(["cheque_status", "=", filters.cheque_status])

	for field in FILTER_FIELDS:
		if filters.get(field):
			conditions.append([field, "=", filters[field]])

	if filters.from_date:
		conditions.append(["cheque_issue_date", ">=", filters.from_date])
	if filters.to_date:
		conditions.append(["cheque_issue_date", "<=", filters.to_date])
	if filters.return_from_date:
		conditions.append(["actual_return_date", ">=", filters.return_from_date])
	if filters.return_to_date:
		conditions.append(["actual_return_date", "<=", filters.return_to_date])

	return conditions


def get_summary(data):
	return [
		{"label": _("Cheques"), "value": len(data), "datatype": "Int", "indicator": "blue"},
		{
			"label": _("Total Amount"),
			"value": sum(flt(row.cheque_amount) for row in data),
			"datatype": "Currency",
			"indicator": "green",
		},
	]
