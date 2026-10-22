# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from frappe.utils import flt


def on_submit(doc, method=None):
	for sales_order in get_sales_orders(doc):
		if is_settled(sales_order):
			change_status(sales_order, "Issued", "Return Pending", doc.name)


def on_cancel(doc, method=None):
	for sales_order in get_sales_orders(doc):
		if not is_settled(sales_order):
			change_status(sales_order, "Return Pending", "Issued", doc.name)


def get_sales_orders(invoice):
	return {item.sales_order for item in invoice.items if item.sales_order}


def is_settled(sales_order):
	order = frappe.db.get_value("Sales Order", sales_order, ["per_billed", "advance_paid"], as_dict=True)
	if flt(order.per_billed) >= 100:
		return True

	advance_paid = flt(order.advance_paid)
	return advance_paid > 0 and get_allocated_advance(sales_order) >= advance_paid


def get_allocated_advance(sales_order):
	advance = frappe.qb.DocType("Sales Invoice Advance")
	invoice = frappe.qb.DocType("Sales Invoice")
	item = frappe.qb.DocType("Sales Invoice Item")

	order_invoices = frappe.qb.from_(item).select(item.parent).where(item.sales_order == sales_order)
	total = (
		frappe.qb.from_(advance)
		.join(invoice)
		.on(invoice.name == advance.parent)
		.select(Sum(advance.allocated_amount))
		.where((invoice.docstatus == 1) & invoice.name.isin(order_invoices))
		.run()
	)
	return flt(total[0][0])


def change_status(sales_order, from_status, to_status, invoice_name):
	cheques = frappe.get_all(
		"Advance Cheque", filters={"sales_order": sales_order, "cheque_status": from_status}, pluck="name"
	)
	for name in cheques:
		try:
			cheque = frappe.get_doc("Advance Cheque", name)
			cheque.cheque_status = to_status
			cheque.save(ignore_permissions=True)
			cheque.add_comment(
				"Info", _("Status changed to {0} by Sales Invoice {1}.").format(to_status, invoice_name)
			)
		except Exception:
			frappe.log_error(title=f"Advance Cheque {name}: status change failed")
