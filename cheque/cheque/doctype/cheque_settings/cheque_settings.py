# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe import throw, _
from frappe.model.document import Document

class ChequeSettings(Document):
	def validate(self):
		company = frappe.db.sql_list("""select company from `tabCheque Settings` where name !=%s""",self.name)
		if self.company in company :
			frappe.msgprint(_("Cheque Settings untuk Company {0} sudah ada!").format(self.company),raise_exception=1, indicator='red')
