// Copyright (c) 2019, Ridhosribumi and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.ui.form.on('Cheque Out', {
	refresh: function(frm) {
		frm.fields_dict['bank_pay'].get_query = function(doc, dt, dn) {
			return{
				filters: [
					 ["Account", "account_type", "in", ["Bank"]]
				]
			}
		}

		if(frm.doc.docstatus == 1 && (frm.doc.cheque_status == 'Draft' || frm.doc.cheque_status == 'Invalid')){

			cur_frm.add_custom_button(__('Rejected'),
				cur_frm.cscript['Rejected Check']);

			cur_frm.add_custom_button(__('Accepted'),
				cur_frm.cscript['Accepted Check']);
		}

		if(frm.doc.docstatus == 1 && frm.doc.cheque_status == 'Accepted'){
			cur_frm.add_custom_button(__('Invalid'),
				cur_frm.cscript['Cancelled Check']);
		}

		if(frm.doc.docstatus == 1 && frm.doc.cheque_status == 'Rejected'){
			cur_frm.add_custom_button(__('Journal Entry'), cur_frm.cscript['Journal Entry'], __("Make"));
				frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
		if(frm.doc.docstatus == 1 && frm.doc.cheque_status == 'Rejected'){
			cur_frm.add_custom_button(__('Rejected Payment Entry'),
			function() {
				frappe.call({
					method: "cheque.cheque.doctype.cheque_out.cheque_out.delete_pe",
					args: {
						pe: frm.doc.payment_entry,
					},
					callback: function(r){
						frm.reload_doc();
						frappe.call({
							method: "cheque.cheque.doctype.cheque_out.cheque_out.status_cancel",
							args: {
								name: frm.doc.name,
							},
							callback: function(r){
								frm.reload_doc();
							}
						});
					}
				});
			})
		}

		if(frm.doc.docstatus == 1 && frm.doc.cheque_status == 'Accepted'){
			frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: frm.doc.posting_date,
					company: frm.doc.company,
					group_by_voucher: false
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}

	}
});

cur_frm.cscript['Journal Entry'] = function() {
	frappe.model.open_mapped_doc({
		method: "cheque.reference.make_journal_entry1",
		frm: cur_frm
	})
}

cur_frm.cscript['Accepted Check'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: __('Cheque Status'),
		fields: [
			  {"fieldtype": "Data", "label": __("Cheque Status"), "fieldname": "cheque_status","reqd":1,"default":"Accepted","read_only":1},
				{"fieldtype": "Date", "label": __("Disbursment Date"), "fieldname": "disbursment_date","reqd":1},
				{"fieldtype": "Link", "label": __("Bank Pay"), "fieldname": "bank_pay","options": "Account","reqd":1,"get_query": function(){return {filters: [["account_type",'=','Bank'],["is_group",'=',0]]};}},
				{"fieldtype": "Data", "label": __("Reference No"), "fieldname": "reference_no","reqd":1},
				{"fieldtype": "Date", "label": __("Reference Date"), "fieldname": "reference_date","reqd":1},
				{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function(){
		var args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "accepted_check",
			doc: cur_frm.doc,
			args: args,
			callback: function(r){
				if(r.exc){
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}

cur_frm.cscript['Rejected Check'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: __('Cheque Status'),
		fields: [
				{"fieldtype": "Data", "label": __("Cheque Status"), "fieldname": "cheque_status","reqd":1,"default":"Rejected","read_only":1},
				{"fieldtype": "Date", "label": __("Rejected Date"), "fieldname": "rejected_date","reqd":1},
				{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function(){
		var args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "rejected_check",
			doc: cur_frm.doc,
			args: args,
			callback: function(r){
				if(r.exc){
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}

cur_frm.cscript['Cancelled Check'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: __('Cheque Status'),
		fields: [
				{"fieldtype": "Data", "label": __("Cheque Status"), "fieldname": "cheque_status","reqd":1,"default":"Invalid","read_only":1},
				{"fieldtype": "Date", "label": __("Invalid Date"), "fieldname": "invalid_date","reqd":1},
				{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function(){
		var args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "cancelled_check",
			doc: cur_frm.doc,
			args: args,
			callback: function(r){
				if(r.exc){
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}
