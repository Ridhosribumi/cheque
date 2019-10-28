# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ridhosribumi and contributors
# For license information, please see license.txt
# Ridhosribumi August 2019

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Cheque In",
					"onboard": 1,
					"description": _("Cheque In"),
				},
                {
					"type": "doctype",
					"name": "Cheque Out",
					"onboard": 1,
					"description": _("Cheque Out"),
				},
                {
					"type": "doctype",
					"name": "Cheque Bank",
					"onboard": 1,
					"description": _("Cheque Bank"),
				},
                {
					"type": "doctype",
					"name": "Cheque Settings",
					"onboard": 1,
					"description": _("Cheque Settings"),
				},
			]
		},

	]
