// Copyright (c) 2026, Rutuja Chavan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Advance Cheque", {
	setup(frm) {
		frm.set_query("sales_order", () => ({ filters: { docstatus: 1 } }));
	},

	refresh(frm) {
		if (frm.is_new() || frm.is_dirty()) return;

		if (frm.doc.cheque_status === "Issued") {
			frm.add_custom_button(__("Return Pending"), () => frm.events.mark_return_pending(frm), __("Mark As"));
		}
		if (frm.doc.cheque_status !== "Returned") {
			frm.add_custom_button(__("Returned"), () => frm.events.mark_returned(frm), __("Mark As"));
		}
	},

	sales_order(frm) {
		if (!frm.doc.sales_order) return;

		frappe.call({
			method: "advance_cheque_tracking.advance_cheque_tracking.doctype.advance_cheque.advance_cheque.get_sales_order_defaults",
			args: { sales_order: frm.doc.sales_order },
			callback: (r) => frm.set_value("sales_person", r.message.sales_person || ""),
		});
	},

	mark_return_pending(frm) {
		frappe.confirm(__("Ask the team to collect this cheque now?"), () => {
			frm.call("mark_return_pending").then(() => frm.reload_doc());
		});
	},

	mark_returned(frm) {
		frappe.prompt(
			[
				{
					fieldname: "return_date",
					label: __("Actual Return Date"),
					fieldtype: "Date",
					default: frappe.datetime.get_today(),
					reqd: 1,
				},
				{ fieldname: "remarks", label: __("Remarks"), fieldtype: "Small Text" },
			],
			(values) => {
				frm.call("mark_returned", { return_date: values.return_date, remarks: values.remarks }).then(() =>
					frm.reload_doc()
				);
			},
			__("Cheque Received Back"),
			__("Confirm")
		);
	},
});
