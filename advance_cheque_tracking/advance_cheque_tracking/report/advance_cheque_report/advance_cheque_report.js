// Copyright (c) 2026, Rutuja Chavan and contributors
// For license information, please see license.txt

frappe.query_reports["Advance Cheque Report"] = {
	filters: [
		{
			fieldname: "cheque_status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Pending", "Issued", "Return Pending", "Returned"],
			default: "Pending",
		},
		{ fieldname: "customer", label: __("Customer"), fieldtype: "Link", options: "Customer" },
		{ fieldname: "sales_order", label: __("Sales Order"), fieldtype: "Link", options: "Sales Order" },
		{ fieldname: "sales_person", label: __("Sales Person"), fieldtype: "Link", options: "Sales Person" },
		{
			fieldname: "accounts_responsible_person",
			label: __("Accounts Person"),
			fieldtype: "Link",
			options: "User",
		},
		{ fieldname: "from_date", label: __("Issued From"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("Issued To"), fieldtype: "Date" },
		{ fieldname: "return_from_date", label: __("Returned From"), fieldtype: "Date" },
		{ fieldname: "return_to_date", label: __("Returned To"), fieldtype: "Date" },
	],

	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname !== "cheque_status" || !data) return value;

		const colors = { Issued: "blue", "Return Pending": "orange", Returned: "green" };
		return `<span class="indicator-pill ${colors[data.cheque_status]}">${value}</span>`;
	},
};
