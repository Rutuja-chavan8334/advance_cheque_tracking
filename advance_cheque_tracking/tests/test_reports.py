# Copyright (c) 2026, Rutuja Chavan and contributors
# For license information, please see license.txt

from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today

from advance_cheque_tracking.advance_cheque_tracking.report.advance_cheque_report.advance_cheque_report import (
	execute,
)
from advance_cheque_tracking.tests.utils import make_cheque, make_order


class TestAdvanceChequeReport(IntegrationTestCase):
	def setUp(self):
		self.open_order, self.done_order = make_order(), make_order()
		self.open = make_cheque(self.open_order, number="910001")
		self.done = make_cheque(self.done_order, number="910002")
		self.done.mark_returned(today(), "Collected")

	def names(self, **filters):
		return [row.name for row in execute(filters)[1]]

	def test_all_statuses_when_no_status_filter(self):
		names = self.names()
		self.assertIn(self.open.name, names)
		self.assertIn(self.done.name, names)

	def test_pending_excludes_returned(self):
		names = self.names(cheque_status="Pending")
		self.assertIn(self.open.name, names)
		self.assertNotIn(self.done.name, names)

	def test_returned_shows_return_date(self):
		data = execute({"cheque_status": "Returned", "sales_order": self.done_order.name})[1]
		self.assertEqual([row.name for row in data], [self.done.name])
		self.assertEqual(str(data[0].actual_return_date), today())

	def test_single_status_filter(self):
		self.open.mark_return_pending()
		order = self.open_order.name
		self.assertEqual(self.names(sales_order=order, cheque_status="Issued"), [])
		self.assertEqual(self.names(sales_order=order, cheque_status="Return Pending"), [self.open.name])

	def test_days_pending_only_for_return_pending(self):
		self.assertIsNone(execute({"sales_order": self.open_order.name})[1][0].days_pending)
		self.open.mark_return_pending()
		self.assertEqual(execute({"sales_order": self.open_order.name})[1][0].days_pending, 0)

	def test_sales_order_filter(self):
		self.assertEqual(self.names(sales_order=self.open_order.name), [self.open.name])

	def test_issue_date_range_filter(self):
		self.assertEqual(self.names(sales_order=self.open_order.name, to_date=add_days(today(), -30)), [])

	def test_return_date_range_filter(self):
		order = self.done_order.name
		self.assertEqual(
			self.names(sales_order=order, return_from_date=today(), return_to_date=today()), [self.done.name]
		)
		self.assertEqual(self.names(sales_order=order, return_to_date=add_days(today(), -1)), [])

	def test_customer_and_sales_person_filters(self):
		self.assertIn(self.open.name, self.names(customer=self.open.customer))
		self.assertIn(self.open.name, self.names(sales_person=self.open.sales_person))
		self.assertEqual(self.names(sales_person="nobody"), [])
