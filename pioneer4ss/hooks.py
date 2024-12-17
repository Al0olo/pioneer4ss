app_name = "pioneer4ss"
app_title = "Pioneer4Ss"
app_publisher = "Abdallah Farag"
app_description = "Backend for Pioneer"
app_email = "info@afarag.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "pioneer4ss",
# 		"logo": "/assets/pioneer4ss/logo.png",
# 		"title": "Pioneer4Ss",
# 		"route": "/pioneer4ss",
# 		"has_permission": "pioneer4ss.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pioneer4ss/css/pioneer4ss.css"
# app_include_js = "/assets/pioneer4ss/js/pioneer4ss.js"

# include js, css files in header of web template
# web_include_css = "/assets/pioneer4ss/css/pioneer4ss.css"
# web_include_js = "/assets/pioneer4ss/js/pioneer4ss.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pioneer4ss/public/scss/website"

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
# app_include_icons = "pioneer4ss/public/icons.svg"

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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "pioneer4ss.utils.jinja_methods",
# 	"filters": "pioneer4ss.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "pioneer4ss.install.before_install"
# after_install = "pioneer4ss.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pioneer4ss.uninstall.before_uninstall"
# after_uninstall = "pioneer4ss.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "pioneer4ss.utils.before_app_install"
# after_app_install = "pioneer4ss.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "pioneer4ss.utils.before_app_uninstall"
# after_app_uninstall = "pioneer4ss.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pioneer4ss.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pioneer4ss.tasks.all"
# 	],
# 	"daily": [
# 		"pioneer4ss.tasks.daily"
# 	],
# 	"hourly": [
# 		"pioneer4ss.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pioneer4ss.tasks.weekly"
# 	],
# 	"monthly": [
# 		"pioneer4ss.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "pioneer4ss.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pioneer4ss.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pioneer4ss.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["pioneer4ss.utils.before_request"]
# after_request = ["pioneer4ss.utils.after_request"]

# Job Events
# ----------
# before_job = ["pioneer4ss.utils.before_job"]
# after_job = ["pioneer4ss.utils.after_job"]

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
# 	"pioneer4ss.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

