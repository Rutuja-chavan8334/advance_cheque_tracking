// Copyright (c) 2026, Rutuja Chavan and contributors
// For license information, please see license.txt

frappe.provide("advance_cheque");

advance_cheque.reminder = {
	init() {
		frappe.realtime.on("advance_cheque_return_pending", (cheque) => {
			cheque.cheque_amount = cheque.amount;
			this.show([cheque], 1);
		});

		const pending = frappe.boot.advance_cheque_pending;
		if (pending && pending.count && !sessionStorage.getItem("advance_cheque_reminded")) {
			sessionStorage.setItem("advance_cheque_reminded", 1);
			this.show(pending.cheques, pending.count);
		}
	},

	show(cheques, total) {
		const rows = cheques
			.map(
				(c) => `<tr>
					<td>${frappe.utils.get_form_link("Advance Cheque", c.name, true)}</td>
					<td>${frappe.utils.escape_html(c.customer || "")}</td>
					<td>${frappe.utils.escape_html(c.sales_order || "")}</td>
					<td>${frappe.utils.escape_html(c.cheque_number || "")}</td>
					<td class="text-right">${format_currency(c.cheque_amount)}</td>
				</tr>`
			)
			.join("");

		let more = "";
		if (total > cheques.length) {
			more = `<p class="text-muted">${__("{0} more pending.", [total - cheques.length])}
				<a href="/app/advance-cheque?cheque_status=Return%20Pending">${__("View all")}</a></p>`;
		}

		frappe.msgprint({
			title: __("Collect Advance Cheque"),
			indicator: "orange",
			message: `
				<p>${__("Please collect the original cheque back for the following.")}</p>
				<table class="table table-bordered">
					<tr>
						<th>${__("Cheque")}</th><th>${__("Customer")}</th><th>${__("Sales Order")}</th>
						<th>${__("Number")}</th><th class="text-right">${__("Amount")}</th>
					</tr>
					${rows}
				</table>
				${more}`,
		});
	},
};

$(document).on("startup", () => advance_cheque.reminder.init());
