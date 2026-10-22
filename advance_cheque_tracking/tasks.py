# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, today

from advance_cheque_tracking.notifications import get_enabled_users, send_digest


def send_pending_return_reminders():
	settings = frappe.get_cached_doc("Advance Cheque Settings")
	if not settings.enable_daily_reminder:
		return

	cheques = frappe.get_all(
		"Advance Cheque",
		filters={"cheque_status": "Return Pending"},
		fields=[
			"name",
			"customer",
			"sales_order",
			"cheque_number",
			"cheque_amount",
			"accounts_responsible_person",
			"sales_person_user",
			"last_reminded_on",
		],
	)
	due = [c for c in cheques if is_due(c, settings.reminder_interval_days)]

	by_user = {}
	for cheque in due:
		users = get_enabled_users([cheque.accounts_responsible_person, cheque.sales_person_user])
		for user in users:
			by_user.setdefault(user, []).append(cheque)

	for user, user_cheques in by_user.items():
		send_digest(user, user_cheques)

	for cheque in due:
		frappe.db.set_value("Advance Cheque", cheque.name, "last_reminded_on", today(), update_modified=False)


def is_due(cheque, interval_days):
	if not cheque.last_reminded_on:
		return True
	return date_diff(today(), cheque.last_reminded_on) >= (interval_days or 1)
