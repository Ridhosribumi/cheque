# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ridhosribumi and contributors
# For license information, please see license.txt
# Ridhosribumi August 2019

from __future__ import unicode_literals
import frappe, math
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.model.naming import make_autoname
from dateutil import parser
from num2words import num2words

def submit_cheque(doc, method):
    chequein_account = frappe.db.sql("""select default_cheque_in_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]
    chequeout_account = frappe.db.sql("""select default_cheque_out_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]

    if (doc.payment_type == 'Receive' and doc.paid_to == chequein_account) :
        cek_list_in = frappe.db.sql_list("""select cheque_no from `tabCheque In`""")
        if doc.cheque_no in cek_list_in:
            frappe.msgprint(_("Cheque No {0} cannot duplicate!").format(doc.cheque_no), raise_exception=1, indicator='red')
        else :
            cheque_add = frappe.get_doc({
              "doctype": "Cheque In",
              "docstatus": 1,
              "cheque_status": "Draft",
              "cheque_no": doc.cheque_no,
              "cheque_date": doc.cheque_date,
              "cheque_bank": doc.cheque_bank,
              "cheque_due_date": doc.cheque_due_date,
              "party_type": doc.party_type,
              "party": doc.party,
              "account_paid_to": doc.paid_to,
              "nominal_cheque": doc.paid_amount,
              "remarks": doc.remarks,
              "payment_entry": doc.name,
              "posting_date": doc.posting_date,
              "mode_of_payment": doc.mode_of_payment,
              "company": doc.company
            })
            cheque_add.insert()

    elif (doc.payment_type == 'Pay' and doc.paid_from == chequeout_account) :
        cek_list_out = frappe.db.sql_list("""select cheque_no from `tabCheque Out`""")
        if doc.cheque_no in cek_list_out:
            frappe.msgprint(_("Cheque No {0} cannot duplicate!").format(doc.cheque_no), raise_exception=1, indicator='red')
        else :
            cheque_add = frappe.get_doc({
              "doctype": "Cheque Out",
              "docstatus": 1,
              "cheque_status": "Draft",
              "cheque_no": doc.cheque_no,
              "cheque_date": doc.cheque_date,
              "cheque_bank": doc.cheque_bank,
              "cheque_due_date": doc.cheque_due_date,
              "party_type": doc.party_type,
              "party": doc.party,
              "account_paid_from": doc.paid_from,
              "nominal_cheque": doc.paid_amount,
              "remarks": doc.remarks,
              "payment_entry": doc.name,
              "posting_date": doc.posting_date,
              "mode_of_payment": doc.mode_of_payment,
              "company": doc.company
            })
            cheque_add.insert()

def cancel_pe(doc,method):
    chequein_account = frappe.db.sql("""select default_cheque_in_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]
    chequeout_account = frappe.db.sql("""select default_cheque_out_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]

    if (doc.payment_type == 'Receive' and doc.paid_to == chequein_account) :
        cek_giro_in = frappe.db.sql("""select cheque_status from `tabCheque In` where payment_entry=%s""",doc.name)[0][0]
        if cek_giro_in == 'Draft' :
            pe = frappe.get_doc("Cheque In", {"payment_entry": doc.name, "company": doc.company})
            pe.flags.ignore_permissions = True
            pe.cancel()
        elif cek_giro_in == 'Rejected' :
            pe = frappe.get_doc("Cheque In", {"payment_entry": doc.name, "company": doc.company})
            pe.flags.ignore_permissions = True
            pe.cancel()
        else :
            frappe.msgprint(_("Cannot cancel because Payment Entry still has Cheque!"), raise_exception=1, indicator='red')
    elif (doc.payment_type == 'Pay' and doc.paid_from == chequeout_account) :
        cek_giro_out = frappe.db.sql("""select cheque_status from `tabCheque Out` where payment_entry=%s""",doc.name)[0][0]
        if cek_giro_out == 'Draft' :
            pe = frappe.get_doc("Cheque Out", {"payment_entry": doc.name, "company": doc.company})
            pe.flags.ignore_permissions = True
            pe.cancel()
        elif cek_giro_out == 'Rejected' :
            pe = frappe.get_doc("Cheque Out", {"payment_entry": doc.name, "company": doc.company})
            pe.flags.ignore_permissions = True
            pe.cancel()
        else :
            frappe.msgprint(_("Cannot cancel because Payment Entry still has Cheque!"), raise_exception=1, indicator='red')

def submit_cheque_jv(doc, method):
    chequein_account = frappe.db.sql("""select default_cheque_in_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]
    chequeout_account = frappe.db.sql("""select default_cheque_out_account  from `tabCheque Settings` where company=%s""",doc.company)[0][0]
    bottle = frappe.db.get_value('Journal Entry Account',{'parent': doc.name,'account_type': 'Bank','debit': ('>',0)},'account');
    ink = frappe.db.get_value('Journal Entry Account',{'parent': doc.name,'account_type': 'Bank','debit': ('>',0)},'debit');
    glass = frappe.db.get_value('Journal Entry Account',{'parent': doc.name,'account_type': 'Bank','credit': ('>',0)},'account');
    wine = frappe.db.get_value('Journal Entry Account',{'parent': doc.name,'account_type': 'Bank','credit': ('>',0)},'credit');

    if (bottle == chequein_account) :
      cheque_add = frappe.get_doc({
        "doctype": "Cheque In",
        "docstatus": 1,
        "cheque_status": "Draft",
        "cheque_no": doc.cheque_no_rss,
        "cheque_date": doc.cheque_date_rss,
        "cheque_bank": doc.cheque_bank,
        "cheque_due_date": doc.cheque_due_date,
        "party_type": doc.party_type,
        "party": doc.party,
        "account_paid_to": bottle,
        "nominal_cheque": ink,
        "remarks": doc.remark,
        "journal_entry": doc.name,
        "posting_date": doc.posting_date,
        "mode_of_payment": doc.mode_of_payment,
        "company": doc.company
      })
      cheque_add.insert()

    elif (glass == chequeout_account) :
      cheque_add = frappe.get_doc({
        "doctype": "Cheque Out",
        "docstatus": 1,
        "cheque_status": "Draft",
        "cheque_no": doc.cheque_no_rss,
        "cheque_date": doc.cheque_date_rss,
        "cheque_bank": doc.cheque_bank,
        "cheque_due_date": doc.cheque_due_date,
        "party_type": doc.party_type,
        "party": doc.party,
        "account_paid_from": glass,
        "nominal_cheque": wine,
        "remarks": doc.remark,
        "journal_entry": doc.name,
        "posting_date": doc.posting_date,
        "mode_of_payment": doc.mode_of_payment,
        "company": doc.company
      })
      cheque_add.insert()

@frappe.whitelist()
def make_journal_entry(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc

    def _update_links(source_doc, target_doc, source_parent):
         target_doc.prevdoc_doctype = source_parent.doctype
         target_doc.prevdoc_docname = source_parent.name

    target_doc = get_mapped_doc("Cheque In", source_name, {
    	"Cheque In": {
    		"doctype": "Journal Entry",
            "field_map": {
                "company": "company",
                "nominal_cheque": "total_credit",
                "party_type": "party_type",
                "party": "party"
            },
            "field_no_map":["cheque_no", "cheque_date", "cheque_due_date", "cheque_bank"],
    	}
    }, target_doc)

    source_doc = frappe.get_doc("Cheque In", source_name)
    table_map = {
        "doctype": "Journal Entry Account",
        "field_map": {
            "account_paid_to": "account",
            "nominal_cheque" : "credit_in_account_currency",
        },
        "add_if_empty": True,
        "postprocess": _update_links
    }
    map_child_doc(source_doc,target_doc,table_map,source_doc)

    return target_doc

@frappe.whitelist()
def make_journal_entry1(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc

    def _update_links(source_doc, target_doc, source_parent):
         target_doc.prevdoc_doctype = source_parent.doctype
         target_doc.prevdoc_docname = source_parent.name

    target_doc = get_mapped_doc("Cheque Out", source_name, {
    	"Cheque Out": {
    		"doctype": "Journal Entry",
            "field_map": {
                "company": "company",
                "nominal_cheque": "total_debit",
                "party_type": "party_type",
                "party": "party"
            },
            "field_no_map":["cheque_no", "cheque_date", "cheque_due_date", "cheque_bank"],
    	}
    }, target_doc)

    source_doc = frappe.get_doc("Cheque Out", source_name)
    table_map = {
        "doctype": "Journal Entry Account",
        "field_map": {
            "account_paid_from": "account",
            "nominal_cheque" : "debit_in_account_currency",
        },
        "add_if_empty": True,
        "postprocess": _update_links
    }
    map_child_doc(source_doc,target_doc,table_map,source_doc)

    return target_doc
