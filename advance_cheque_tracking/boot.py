# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe


def boot_session(bootinfo):
	user = frappe.session.user
	if user == "Guest":
		return

	cheques = frappe.get_all(
		"Advance Cheque",
		filters={"cheque_status": "Return Pending"},
		or_filters={"accounts_responsible_person": user, "sales_person_user": user},
		fields=["name", "cheque_number", "customer", "sales_order", "cheque_amount"],
		order_by="return_pending_since",
	)
	bootinfo.advance_cheque_pending = {"count": len(cheques), "cheques": cheques[:10]}
