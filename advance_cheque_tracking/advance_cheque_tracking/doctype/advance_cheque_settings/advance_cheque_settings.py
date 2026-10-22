# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AdvanceChequeSettings(Document):
	def validate(self):
		if self.enable_daily_reminder and (self.reminder_interval_days or 0) < 1:
			frappe.throw(_("Remind Every (Days) must be at least 1."))
