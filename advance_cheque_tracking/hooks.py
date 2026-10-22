app_name = "advance_cheque_tracking"
app_title = "Advance Cheque Tracking"
app_publisher = "Rutuja Chavan"
app_description = "Track advance cheques against Sales Orders and remind users to collect them back"
app_email = "chavanrutu2@gmail.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "advance_cheque_tracking",
# 		"logo": "/assets/advance_cheque_tracking/logo.png",
# 		"title": "advance_cheque_tracking",
# 		"route": "/advance_cheque_tracking",
# 		"has_permission": "advance_cheque_tracking.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/advance_cheque_tracking/css/advance_cheque_tracking.css"
app_include_js = "/assets/advance_cheque_tracking/js/cheque_reminder.js"

# include js, css files in header of web template
# web_include_css = "/assets/advance_cheque_tracking/css/advance_cheque_tracking.css"
# web_include_js = "/assets/advance_cheque_tracking/js/advance_cheque_tracking.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "advance_cheque_tracking/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "advance_cheque_tracking/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "advance_cheque_tracking.utils.jinja_methods",
# 	"filters": "advance_cheque_tracking.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "advance_cheque_tracking.install.before_install"
# after_install = "advance_cheque_tracking.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "advance_cheque_tracking.uninstall.before_uninstall"
# after_uninstall = "advance_cheque_tracking.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "advance_cheque_tracking.utils.before_app_install"
# after_app_install = "advance_cheque_tracking.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "advance_cheque_tracking.utils.before_app_uninstall"
# after_app_uninstall = "advance_cheque_tracking.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "advance_cheque_tracking.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "advance_cheque_tracking.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["advance_cheque_tracking.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Session
# -------

boot_session = "advance_cheque_tracking.boot.boot_session"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"on_submit": "advance_cheque_tracking.advance_cheque_tracking.custom_script.sales_invoice.sales_invoice.on_submit",
		"on_cancel": "advance_cheque_tracking.advance_cheque_tracking.custom_script.sales_invoice.sales_invoice.on_cancel",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"advance_cheque_tracking.tasks.send_pending_return_reminders"
	],
}

# Testing
# -------

# before_tests = "advance_cheque_tracking.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "advance_cheque_tracking.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "advance_cheque_tracking.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "advance_cheque_tracking.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["advance_cheque_tracking.utils.before_request"]
# after_request = ["advance_cheque_tracking.utils.after_request"]

# Job Events
# ----------
# before_job = ["advance_cheque_tracking.utils.before_job"]
# after_job = ["advance_cheque_tracking.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"advance_cheque_tracking.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

