// Copyright (c) 2019, Ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cheque Settings', {
	refresh: function(frm) {
		frm.fields_dict['default_cheque_in_account'].get_query = function(doc, dt, dn) {
			return{
				filters: [
					 ["Account", "account_type", "in", ["Bank"]]
				]
			}
		}

		frm.fields_dict['default_cheque_out_account'].get_query = function(doc, dt, dn) {
			return{
				filters: [
					 ["Account", "account_type", "in", ["Bank"]]
				]
			}
		}
	}
});
