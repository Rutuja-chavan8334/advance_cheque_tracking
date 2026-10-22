// Copyright (c) 2026, Rutuja Chavan and contributors
// For license information, please see license.txt

frappe.listview_settings["Advance Cheque"] = {
	get_indicator(doc) {
		const colors = { Issued: "blue", "Return Pending": "orange", Returned: "green" };
		return [__(doc.cheque_status), colors[doc.cheque_status], `cheque_status,=,${doc.cheque_status}`];
	},
};
