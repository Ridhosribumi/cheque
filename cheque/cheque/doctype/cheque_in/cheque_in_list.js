// Copyright (c) 2019, Ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.listview_settings['Cheque In'] = {
	add_fields: ["cheque_status","posting_date","company", "remarks"],
	get_indicator: function(doc) {
		if(doc.cheque_status == 'Accepted') {
      return [__(doc.cheque_status), "green", "cheque_status,=," + doc.cheque_status]
		} else if(doc.cheque_status=='Invalid') {
			return [__(doc.cheque_status), "purple", "cheque_status,=," + doc.cheque_status]
		} else if(doc.cheque_status=='Rejected') {
			return [__(doc.cheque_status), "orange", "cheque_status,=," + doc.cheque_status]
    } else if(doc.cheque_status=='Draft') {
      return [__(doc.cheque_status), "blue ", "cheque_status,=," + doc.cheque_status]
    }

    if(doc.docstatus==0) {
			return [__("Draft", "blue", "docstatus,=,0")]
		} else if(doc.docstatus==2) {
			return [__("Cancelled", "red", "docstatus,=,2")]
		}
	}
};
